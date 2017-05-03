# -*- coding: utf-8 -*-
import scrapy
import json
from spiders import itunes_config
from database_manager import AppInfo
from record_manager import comments_state

class AppinfospiderSpider(scrapy.Spider):
    name = "AppInfoSpider"
    allowed_domains = ["itunes.apple.com"]
    start_urls = []

    def __init__(self):
        self.start_urls = ["https://itunes.apple.com/cn/lookup?id="+appid for appid in itunes_config.appids()]

    def parse(self, response):
        #print(response.body)
        json_dir = json.loads(response.body.decode(), encoding='utf-8')
        #print(json_dir)
        appInfo = AppInfo()
        appInfo.id = json_dir["results"][0]["trackId"]
        appInfo.name = json_dir["results"][0]["trackCensoredName"]
        appInfo.rights = json_dir["results"][0]["sellerName"]
        appInfo.imageurl = json_dir["results"][0]["artworkUrl60"]
        appInfo.artist = json_dir["results"][0]["artistName"]
        appInfo.title = json_dir["results"][0]["trackName"]
        appInfo.newestversion = json_dir["results"][0]["version"]
        appInfo.averageUserRating = json_dir["results"][0]["trackContentRating"]
        appInfo.type = json_dir["results"][0]["kind"]

        comments_state.addOrUpdateAppInfo(appInfo)
        #print(json_dir)
