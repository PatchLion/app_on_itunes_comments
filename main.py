#!/usr/binenv python
# -*- coding: utf-8 -*-

import os
import time

from record_manager import comments_state

def runSpider():
    while(True):
        print('Start Spider!')
        os.system('scrapy crawl CommentsXmlSpider')
        print('End Spider!')
        print("Record Count:", comments_state.recordCount())
        with open('lasttime.record', 'w') as f:
            f.write(str(time.time()))
        time.sleep(60 * 60 * 3) #三小时拉取一次


if '__main__' == __name__:
    runSpider()
