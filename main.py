#!/usr/binenv python
# -*- coding: utf-8 -*-

import os
import time

from record_manager import comments_state
from spiders import itunes_config

def runSpider():
    while(True):
        print('Start Spider!')
        os.system('scrapy crawl CommentsXmlSpider')
        os.system('scrapy crawl AppInfoSpider')
        print('End Spider!')
        print("Record Count:", comments_state.recordCount())
        time.sleep(60 * 60 * itunes_config.delay()) #下一次拉取间隔


if '__main__' == __name__:
    runSpider()
