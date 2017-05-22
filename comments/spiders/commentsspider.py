# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
from scrapy.spiders import XMLFeedSpider
from bs4 import *
from comments.items import CommentsItem
import time

mysettings = get_project_settings()

def build_url(country, appid):
    return 'https://itunes.apple.com/' + country + '/rss/customerreviews/id=' + appid + '/xml'


class CommentsspiderSpider(XMLFeedSpider):
    name = "commentsspider"
    allowed_domains = ["itunes.apple.com"]
    start_urls = []
    iterator = 'xml'
    itertag = 'feed'

    def __init__(self):
        self.start_urls = [build_url(c, a) for c in mysettings.get("ITUNES_AREAS") for a in mysettings.get("ITUNES_APPIDS")]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        url = str(response.url)
        countryorarea = url[len('https://itunes.apple.com/'):len('https://itunes.apple.com/') + 2]
        appid = url.split('=')[1].split('/')[0]

        items = []
        for tag in soup.find_all('entry')[1:]:
            c = CommentsItem()
            c["id"] = tag.find('id').string
            c["author"] = tag.find('author').find('name').string
            c["version"] = tag.find('im:version').string
            c["rating"] = tag.find('im:rating').string
            c["title"] = tag.find('title').string
            c["content"] = tag.find('content').string
            c["country_or_area"] = countryorarea
            c["content_trans_cn"] = ""
            c["content_trans_en"] = ""
            c["app_id"] = appid
            c["content_type"] = tag.find('content')["type"]
            dt = tag.find('updated').string[:-6]
            timeArray = time.strptime(dt, "%Y-%m-%dT%H:%M:%S")
            timeStamp = time.mktime(timeArray)
            c["create_timestamp"] = timeStamp
            c["update_timestamp"] = time.time()
            items.append(c)
        return items
