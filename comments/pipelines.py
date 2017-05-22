# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db_tables import Comments
from scrapy.exceptions import DropItem
from comments import RecordExistType


class CommentsPipeline(object):
    def process_item(self, item, spider):
        result = Comments.is_comments_exist(item["id"])
        if RecordExistType.Exist == result:
            raise DropItem("Duplicate item found: %s" % item["id"])
        elif RecordExistType.NotExist == result:
            Comments.add_comments(item)
            return item
        elif RecordExistType.Error == result:
            return item
