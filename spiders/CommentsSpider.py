# -*- coding: utf-8 -*-
import scrapy
import json
import os

from items import ItunescommentsspiderItem
import time
from database_manager import Comments
from record_manager import comments_state

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
    return 'https://itunes.apple.com/' + country + '/rss/customerreviews/id=' + appid + '/json'

class CommentsspiderSpider(scrapy.Spider):
    name = "CommentsSpider"
    allowed_domains = ["itunes.apple.com"]
    start_urls = []


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
        json_dict = json.loads(replaceChar(response.body.decode()), encoding='utf-8')
        url = str(response.url)

        print("json_dict:", json_dict)
        print("url", url)

        countryorarea = url[len('https://itunes.apple.com/'):len('https://itunes.apple.com/') + 2]
        appid = url.split('=')[1].split('/')[0]

        if not os.path.exists("jsons"):
            os.mkdir('jsons')

        with open( "jsons/" + appid+"_"+countryorarea+".json", 'wb') as f:
            f.write(response.body)

        entries = json_dict.get('feed', None).get('entry', None)
        if None == entries:
            print("Failed resolve json dict! ", countryorarea, appid)
        else:
            entries = entries[1:]
            items = []
            for data in entries:
                c = Comments()
                c.id = data["id"]["label"]
                c.author = data["author"]["name"]["label"]
                c.version = data["im:version"]["label"]
                c.rating = data["im:rating"]["label"]
                c.title = data["title"]["label"]
                c.content = data["content"]["label"]
                c.countryorarea = countryorarea
                c.appid = appid
                c.contenttype = data["content"]["attributes"]["type"]
                c.createtimestamp = str(time.time())
                c.updatetimestamp = str(time.time())
                items.append(c)

                #print("))))))))))))))))))))", c.appid)

            comments_state.addComments(items)