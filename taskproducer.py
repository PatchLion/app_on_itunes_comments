#!/usr/binenv python
# -*- coding: utf-8 -*-
import time, os
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import use_connection, Queue
from myworker import conn, update_comments, start_send_new_comments_email, start_translate_task
from scrapy.utils.project import get_project_settings
from mylogging import mylogger

mysettings = get_project_settings();
scheduler = BlockingScheduler()

use_connection(conn)
q = Queue()

@scheduler.scheduled_job("interval", seconds=mysettings.get("UPDATE_COMMENTS_INTERVAL", 1 * 60 * 60))
def update_comments_scheduler():
    result = q.enqueue(update_comments)
    mylogger.info('push update_comments task')

@scheduler.scheduled_job("interval", seconds=mysettings.get("NEW_ITEMS_CHECK_INTERVAL", 1 * 60 * 60))
def start_send_new_comments_email_scheduler():
    result = q.enqueue(start_send_new_comments_email)
    mylogger.info('push start_send_new_comments_email task')

@scheduler.scheduled_job("interval", seconds=mysettings.get("TRANSLATE_CHECK_INTERVAL", 1 * 60 * 60))
def start_translate_task_scheduler():
    result = q.enqueue(start_translate_task)
    mylogger.info('push start_translate_task task')

if __name__ == '__main__':
    try:
        mylogger.info("Run scheduler......")
        mylogger.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        #update_comments_scheduler()
        #start_send_new_comments_email_scheduler()
        #start_translate_task_scheduler()
        scheduler.start()
    except Exception as e:
        mylogger.error(e)
        scheduler.shutdown()
