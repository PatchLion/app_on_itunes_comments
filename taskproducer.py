#!/usr/binenv python
# -*- coding: utf-8 -*-
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import use_connection, Queue
from myworker import conn, update_comments, start_send_new_comments_email
from scrapy.utils.project import get_project_settings

mysettings = get_project_settings();
scheduler = BlockingScheduler()
HOUR = 60 * 60

use_connection(conn)
q = Queue()

@scheduler.scheduled_job("interval", seconds=mysettings.get("UPDATE_COMMENTS_INTERVAL", 1)*HOUR)
def update_comments_scheduler():
    result = q.enqueue(update_comments)
    print(time.asctime(time.localtime(time.time())), ': push update_comments task:', result)

@scheduler.scheduled_job("interval", seconds=mysettings.get("NEW_ITEMS_CHECK_INTERVAL", 2)*HOUR)
def start_send_new_comments_email_scheduler():
    result = q.enqueue(start_send_new_comments_email)
    print(time.asctime(time.localtime(time.time())), ': push start_send_new_comments_email task:', result)

if __name__ == '__main__':
    try:
        print("Run scheduler......")
        update_comments_scheduler()
        start_send_new_comments_email_scheduler()
        scheduler.start()
    except Exception as e:
        print(e)
        scheduler.shutdown()
