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

from mylogging import mylogger

listen = ['high', 'default', 'low']
LASTTIMESTAMP_KEY = "comments:lasttimestamp"
redis_url = "redis://localhost:6379"


conn = redis.from_url(redis_url)

def update_comments():
    os.system('scrapy crawl commentsspider')

def start_send_new_comments_email():
    current_dt = time.time()
    mylogger.info('Do start_send_new_comments_email(RQ)')
    last = conn.get(LASTTIMESTAMP_KEY)
    last_timestamp = 0
    if last is not None:
        last_timestamp = round(float(last))

    mylogger.info('Last TimeStamp: {0} {1}'.format(last_timestamp, type(last_timestamp)))
    results = Comments.requry_record_after_timestamp(last_timestamp)
    mylogger.info("TotalCount: {0}".format(len(results)))

    result_map = {}
    for result in results:
        if result.app_id not in result_map.keys():
            result_map[result.app_id] = [result]
        else:
            result_map[result.app_id].append(result)

    try:
        for key, value in result_map.items():
            list_comment = result_map[key]
            list_comment.sort(key=attrgetter('version', 'create_timestamp'), reverse=True)
            mylogger.info('有新的评论的App: {0} 数量:{1}条'.format(key, len(list_comment)))
            appid_config = email_config["dest_emails"].get(key, None)

            if appid_config is None:
                mylogger.error("没有找到App:{0} 相关的邮箱配置!".format(key))
            else:
                content = comments_html_builder(appid_config["app_name"], list_comment)

                app_name_with_line = appid_config["app_name"].replace(' ', "_")
                temp_html_file_nam = 'comments_'+ app_name_with_line + '_' + key +'.html'
                with open(temp_html_file_nam, 'w', encoding='utf-8') as f:
                    f.write(content)

                mylogger.info("开始发送App: {0}的通知邮件(From: {1}:{2} To {3})".format(key, email_config["from"], str(email_config["port"]), appid_config["emails"]))

                server = {}
                server['name'] = email_config["smtp_server"]
                server['user'] = email_config["username"]
                server['passwd'] = email_config["password"]
                mylogger.debug("Email server: {0}".format(server))
                send_result = send_mail(server, email_config["port"],
                                     email_config["from"],
                                     appid_config["emails"],
                                     "[" + appid_config["app_name"] + "] 有了" + str(len(list_comment)) + "条新评论",
                                     "见附件", [temp_html_file_nam])

                mylogger.info("发送邮件完毕! {0}".format(send_result))
        conn.set(LASTTIMESTAMP_KEY, current_dt)
    except Exception as e:
        mylogger.error("发送邮件过程中，发生异常: {0}".format(e))

if __name__ == '__main__':
    with Connection(conn):
        worker = None
        mylogger.info("Start worker...")
        if os.name == "nt":
            worker = WindowsWorker(map(Queue, listen))
        else:
            worker = Worker(map(Queue, listen))
        worker.work()
