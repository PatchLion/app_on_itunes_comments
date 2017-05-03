# -*- coding: utf-8 -*-
import scrapy
import json
import os
from scrapy.spiders import XMLFeedSpider
from items import ItunescommentsspiderItem
import time
from database_manager import Comments
from record_manager import comments_state
from bs4 import *

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


countries = ['cn', 'us', 'jp',
             'de', 'fr', 'tw',
             'hk', 'pt', 'en',
             'ar', 'be', 'el',
             'es', 'fi', 'fr',
             'hr', 'hu', 'is',
             'it', 'iw', 'ko',
             'lt', 'lv', 'mk',
             'nl', 'no', 'pl',
             'pt', 'ro', 'ru',
             'sh', 'sk', 'sl',
             'sq', 'sr', 'sv',
             'th', 'tr', 'uk',
             'gb', 'ie', 'ca',
             'au', 'nz', 'za']

appids = ['503039729']

replace_chars = [u'\xa9']

def replaceChar(s):
    for c in replace_chars:
        s = s.replace(c, '')
    return s

def buildUrl(country, appid):
    return 'https://itunes.apple.com/' + country + '/rss/customerreviews/id=' + appid + '/xml'

class CommentsXMLSpider(XMLFeedSpider):
    name = "CommentsXmlSpider"
    allowed_domains = ["itunes.apple.com"]
    namespaces = [("xmlns","http://www.w3.org/2005/Atom")]
    start_urls = []
    iterator = 'xml'
    itertag = 'feed'

    def __init__(self):
        self.start_urls = [buildUrl(c, a) for c in countries for a in appids]
        #spider启动信号和spider_opened函数绑定
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        #spider关闭信号和spider_spider_closed函数绑定
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        for url in self.start_urls:
            print('url--->', url)

    def spider_opened(self):
        print("Spider Opended!")

    def spider_closed(self):
        comments_state.afterSpiderFinished()

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        url = str(response.url)

        countryorarea = url[len('https://itunes.apple.com/'):len('https://itunes.apple.com/') + 2]
        appid = url.split('=')[1].split('/')[0]

        if not os.path.exists("xmls"):
            os.mkdir('xmls')

        with open("xmls/" + appid + "_" + countryorarea + ".xml", 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        items = []
        for tag in soup.find_all('entry')[1:]:
            c = Comments()
            c.id = tag.find('id').string
            c.author = tag.find('author').find('name').string
            c.version = tag.find('im:version').string
            c.rating = tag.find('im:rating').string
            c.title = tag.find('title').string
            c.content = tag.find('content').string
            c.countryorarea = countryorarea
            c.appid = appid
            c.contenttype = tag.find('content')["type"]
            dt = tag.find('updated').string[:-6]
            timeArray = time.strptime(dt, "%Y-%m-%dT%H:%M:%S")
            timeStamp = time.mktime(timeArray)
            c.createtimestamp = timeStamp
            c.updatetimestamp = str(time.time())
            items.append(c)
            #print(c)
        comments_state.addComments(items)
    #def parse_node(self, response, node):
        #print('parse_node')