# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CommentsItem(scrapy.Item):
    id = scrapy.Field()
    author = scrapy.Field()
    version = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    country_or_area = scrapy.Field()
    content_trans_cn = scrapy.Field()
    content_trans_en = scrapy.Field()
    app_id = scrapy.Field()
    content_type = scrapy.Field()
    create_timestamp = scrapy.Field()
    update_timestamp = scrapy.Field()
