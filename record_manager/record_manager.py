#!/usr/binenv python
# -*- coding: utf-8 -*-

import json
from database_manager import data_manager, RecordOpratorType
from email_manager import send_email
import time


class CommentsStateManager(object):
    def __init__(self):
        self._newcomments = {}          #新增的评论
        with open('email_template.html', 'r', encoding='utf-8') as f:
            self._email_template = f.read()
            print("网页模板加载完毕")
        with open('row_template.html', 'r', encoding='utf-8') as f:
            self._email_row_template = f.read()
            print("行模板加载完毕")
        with open('email.config', 'r') as f:
            self._emil_config = json.load(f, encoding='utf-8')
        print("加载邮件配置:", self._emil_config)

    def addComments(self, comments):
        for comment in comments:
            self.addComment(comment)

    def addComment(self, comment):
        opr_type = data_manager.addOrUpdateComment(comment)

        #记录新增评论
        if RecordOpratorType.Insert == opr_type:
            if not comment.appid in self._newcomments.keys():
                self._newcomments[comment.appid] = [comment]
            else:
                self._newcomments[comment.appid].append(comment)

    def buildEmailContent(self, appname, comments):
        html = self._email_template
        html = html.replace('%AppName%', appname)
        rows = ""
        for c in comments:
            row_temp = self._email_row_template
            row_temp = row_temp.replace('%Author%', c.author)
            rating_sting = ''
            for i in range(int(c.rating)):
                rating_sting += "☆"
            row_temp = row_temp.replace('%Star%', rating_sting)
            timeArray = time.localtime(float(c.createtimestamp))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            row_temp = row_temp.replace('%DateTime%', otherStyleTime)
            row_temp = row_temp.replace('%Title%', c.title)
            row_temp = row_temp.replace('%Content%', c.content)
            row_temp = row_temp.replace('%Area%',c.countryorarea)
            row_temp = row_temp.replace('%Version%',c.version)
            rows = rows + row_temp
        html = html.replace('%Rows%', rows)
        return html

    def afterSpiderFinished(self):
        if len(self._newcomments) > 0:
            for key, value in self._newcomments.items():
                print('有新的评论的App:', key, '新评论数:', len(self._newcomments[key]), '条')

                appid_config = self._emil_config["dest_emails"].get(key, None)
                if appid_config is None:
                    print("没有找到App:", key, "相关的邮箱配置!")
                else:
                    content = self.buildEmailContent(appid_config["app_name"], self._newcomments[key])

                    temp_html_file_nam = 'comments.html'
                    with open(temp_html_file_nam, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print("开始发送App", key, "的通知邮件(From:", self._emil_config["email"], ' To: ', appid_config["emails"], ")")
                    #发送通知邮件
                    server = {}
                    server['name'] = self._emil_config["smtp_server"]
                    server['user'] = self._emil_config["email"]
                    server['passwd'] = self._emil_config["password"]
                    send_email.send_mail(server,
                                         self._emil_config["email"],
                                         appid_config["emails"],
                                         "App[" + appid_config["app_name"] + "] 有了" + str(len(self._newcomments[key]))+ "条新评论",
                                         "见附件", [temp_html_file_nam])
                    print("发送邮件完毕!")
            self._newcomments.clear()

    def recordCount(self):
        return data_manager.recordCount()

