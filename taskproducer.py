#!/usr/binenv python
# -*- coding: utf-8 -*-
import time, os
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import use_connection, Queue
from myworker import conn, update_comments, start_send_new_comments_email
from scrapy.utils.project import get_project_settings
from mylogging import config_logging
import logging
mysettings = get_project_settings();
scheduler = BlockingScheduler()
HOUR = 60 * 60

use_connection(conn)
q = Queue()

@scheduler.scheduled_job("interval", seconds=mysettings.get("UPDATE_COMMENTS_INTERVAL", 1)*HOUR)
def update_comments_scheduler():
    result = q.enqueue(update_comments)
    logging.info(time.asctime(time.localtime(time.time())), ': push update_comments task')

@scheduler.scheduled_job("interval", seconds=mysettings.get("NEW_ITEMS_CHECK_INTERVAL", 2)*HOUR)
def start_send_new_comments_email_scheduler():
    result = q.enqueue(start_send_new_comments_email)
    logging.info(time.asctime(time.localtime(time.time())), ': push start_send_new_comments_email task')

if __name__ == '__main__':
    try:
        logging.info("Run scheduler......")
        logging.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        update_comments_scheduler()
        scheduler.start()
    except Exception as e:
        logging.error(e)
        scheduler.shutdown()
