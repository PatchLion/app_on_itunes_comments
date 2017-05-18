#!/usr/binenv python
# -*- coding: utf-8 -*-

import time
import os
import redis
from rq_win import WindowsWorker
from rq import Queue, Connection, Worker
from db_tables import Comments
from comments_html_builder import comments_html_builder
from operator import attrgetter
from email_config import email_config
from send_email import send_mail
from mylogging import config_logging
import logging
listen = ['high', 'default', 'low']
LASTTIMESTAMP_KEY = "comments:lasttimestamp"
redis_url = "redis://localhost:6379"


conn = redis.from_url(redis_url)

def update_comments():
    os.system('scrapy crawl commentsspider')

def start_send_new_comments_email():
    current_dt = time.time()
    logging.info('Do start_send_new_comments_email(RQ)')
    last_timestamp = round(float(conn.get(LASTTIMESTAMP_KEY)))
    logging.info('Last TimeStamp:', last_timestamp, type(last_timestamp))
    results = Comments.requry_record_after_timestamp(last_timestamp)
    logging.info("TotalCount:", len(results))

    result_map = {}
    for result in results:
        if result.app_id not in result_map.keys():
            result_map[result.app_id] = [result]
        else:
            result_map[result.app_id].append(result)

    try:
        for key, value in result_map.items():
            list_comment = result_map[key]
            list_comment.sort(key=attrgetter('version'), reverse=True)
            logging.info('有新的评论的App:', key, '新评论数:', len(list_comment), '条')
            appid_config = email_config["dest_emails"].get(key, None)

            if appid_config is None:
                logging.error("没有找到App:", key, "相关的邮箱配置!")
            else:
                content = comments_html_builder(appid_config["app_name"], list_comment)

                app_name_with_line = appid_config["app_name"].replace(' ', "_")
                temp_html_file_nam = 'comments_'+ app_name_with_line + '_' + key +'.html'
                with open(temp_html_file_nam, 'w', encoding='utf-8') as f:
                    f.write(content)

                logging.info("开始发送App", key, "的通知邮件(From:", email_config["from"], ":" , str(email_config["port"]), ' To: ', appid_config["emails"], ")")

                server = {}
                server['name'] = email_config["smtp_server"]
                server['user'] = email_config["username"]
                server['passwd'] = email_config["password"]
                logging.debug("Email server:", server)
                send_result = send_mail(server, email_config["port"],
                                     email_config["from"],
                                     appid_config["emails"],
                                     "[" + appid_config["app_name"] + "] 有了" + str(len(list_comment)) + "条新评论",
                                     "见附件", [temp_html_file_nam])

                logging.info("发送邮件完毕!", send_result)
        conn.set(LASTTIMESTAMP_KEY, current_dt)
    except Exception as e:
        logging.error("发送邮件过程中，发生异常:", e)

if __name__ == '__main__':
    with Connection(conn):
        worker = None
        if os.name == "nt":
            worker = WindowsWorker(map(Queue, listen))
        else:
            worker = Worker(map(Queue, listen))
        worker.work()
