# -*- coding: utf-8 -*-

import time
import os
import redis
import json
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
LIMIT_COMMENT_SIZE = 8
redis_url = "redis://localhost:6379"


conn = redis.from_url(redis_url)



def update_comments():
    os.system('scrapy crawl commentsspider')

def start_send_new_comments_email():
    current_dt = time.time()
    mylogger.info('Do start_send_new_comments_email(RQ)')

    appids = email_config["dest_emails"].keys()

    for appid in appids:
        if len(appid) == 0:
            continue

        redis_key = LASTTIMESTAMP_KEY + ":" + appid
        last = conn.get(redis_key)
        last_timestamp = 0
        if last is not None:
            last_timestamp = round(float(last))


        results = Comments.requry_record_after_timestamp(appid, last_timestamp)
        mylogger.info('{0} Last TimeStamp: {1}, Record count: {2}'.format(appid, last_timestamp, len(results)))

        result_map = {}
        for result in results:
            if result.app_id not in result_map.keys():
                result_map[result.app_id] = [result]
            else:
                result_map[result.app_id].append(result)

        try:
            for key, value in result_map.items():
                #print("Wait seconds......")
                #time.sleep(5) #休眠几秒
                list_comment = result_map[key]
                list_comment.sort(key=attrgetter('version', 'create_timestamp'), reverse=True)
                mylogger.info('有新的评论的App: {0} 数量:{1}条'.format(key, len(list_comment)))
                appid_config = email_config["dest_emails"].get(key, None)

                if appid_config is None:
                    mylogger.error("没有找到App:{0} 相关的邮箱配置!".format(key))
                else:
                    content = comments_html_builder(appid_config["app_name"], list_comment, limit = LIMIT_COMMENT_SIZE)

                    app_name_with_line = appid_config["app_name"].replace(' ', "_")
                    temp_html_file_nam = 'comments_' + app_name_with_line + '_' + key + '.html'
                    with open(temp_html_file_nam, 'w', encoding='utf-8') as f:
                        f.write(content)

                    server = {}
                    server['name'] = email_config["smtp_server"]
                    server['user'] = email_config["username"]
                    server['passwd'] = email_config["password"]

                    mylogger.info("开始发送App: {0}的通知邮件(From: {1}:{2} To {3})".format(key, email_config["from"], str(email_config["port"]), appid_config["emails"]))

                    #如果大于了限制的评论，则将多余的放入附件发送
                    file_list = []
                    if len(list_comment) > LIMIT_COMMENT_SIZE:
                        file_list.append(temp_html_file_nam)

                        tip = "<p style='color:#000000'>评论数已超出了显示限制，请下载附件查看全部评论</p>"
                        content = tip + "</p></p></p>" + content
                        content = content + "</p></p></p>" + tip

                    mylogger.info("Email server: {0}".format(server))
                    send_result = send_mail(server, email_config["port"],
                                         email_config["from"],
                                         appid_config["emails"],
                                         "App [ " + appid_config["app_name"] + " ] 有了" + str(len(list_comment)) + "条新评论",
                                            content, file_list)



                    mylogger.info("发送邮件完毕! {0}".format(send_result))
            conn.set(redis_key, current_dt)
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
