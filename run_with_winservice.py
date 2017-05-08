#!/usr/binenv python
# -*- coding: utf-8 -*-

#参考来源：http://www.cnblogs.com/dcb3688/p/4496934.html
#         http://blog.csdn.net/kmust20093211/article/details/42169323

import win32serviceutil
import win32service
import win32event
import winerror
import servicemanager
import os, sys, time

#from runmain import runSpider
#from record_manager import comments_state
from spiders import itunes_config

class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ItunesCommentsSpider"
    _svc_display_name_ = "Itunes评论抓取"
    _svc_description_ = "自动抓取Itunes评论，并发送最新评论到指定邮箱"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcDoRun(self):
        # 把自己的代码放到这里，就OK
        # 等待服务被停止
        while self.running:
            os.system('scrapy crawl CommentsXmlSpider')
            os.system('scrapy crawl AppInfoSpider')
            time.sleep(60 * 60 * itunes_config.delay())  # 下一次拉取间隔
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        # 先告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
        self.running = False

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(PythonService)