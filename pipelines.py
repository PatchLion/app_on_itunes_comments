# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time

from DataManager.DataManager import Comments, DataManager



class ItunescommentsspiderPipeline(object):
    def process_item(self, item, spider):
        c = Comments()
        c.id = item['id']
        c.author = item['author']
        c.version = item['version']
        c.rating = int(item['rating'])
        c.title = item['title']
        c.content = item['content']
        c.contenttype = item['contenttype']
        c.createtimestamp = item['createtimestamp']
        c.updatetimestamp = str(time.time())

        print("------------", type(item), c.id, c.title)


        return item
