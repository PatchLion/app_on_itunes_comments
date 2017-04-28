# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItunescommentsspiderItem(scrapy.Item):
    id = scrapy.Field()
    author = scrapy.Field()
    version = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    contenttype = scrapy.Field()
    createtimestamp = scrapy.Field()