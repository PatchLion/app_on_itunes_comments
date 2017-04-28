#!/usr/binenv python
# -*- coding: utf-8 -*-

import os
import time

#from DataManager.DataBaseTables import BaseModel
from spiders.CommentsSpider import datamanager

def runSpider():
    while(True):
        print('Start Spider!')
        os.system('scrapy crawl CommentsSpider')
        print('End Spider!')
        print("Record Count:", datamanager.recordCount())
        time.sleep(600)


if '__main__' == __name__:
    runSpider()
