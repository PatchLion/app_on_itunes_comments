# -*- coding: utf-8 -*-

import json, time
from googletrans import Translator
from db_tables import *
from mylogging import mylogger

skips = [] #TODO: googletrans的Bug, 某些带表情的评论出错

def start_translate_task():
    list_comments = Comments.requery_not_translate_comments(skips)
    mylogger.info("Total need translate count: %d" % len(list_comments))
    #LENTH = 1
    #list_comments = [list_comments[i:i+LENTH] for i in range(0, len(list_comments), LENTH)]

    index = 1
    for cs in list_comments:
        #list_ori_string = [c.content for c in cs]
        mylogger.info("开始请求翻译：{0} {1}/{2}".format(cs.content, index, len(list_comments)))
        index += 1
        try:
            translator = Translator()
            translations = translator.translate(cs.content, dest="zh-CN")
            datamap = {}

            '''
            for tran in translations:
                mylogger.info("{0} -> {1}".format(tran.origin, tran.text))
                datamap[tran.origin] = tran.text
            '''
            mylogger.info("{0} -> {1}".format(translations.origin, translations.text))
            datamap[translations.origin] = translations.text

            Comments.update_translate_comments(datamap)
        except json.decoder.JSONDecodeError as e:
            mylogger.warning("Json error: {0}".format(e))
            skips.append(cs.content)
            mylogger.info("Skips: {0}".format(skips))
        except Exception as e:
            mylogger.warning("translate: {0}".format(e))

if "__main__" == __name__:
    while True:
        start_translate_task()
        time.sleep(5)