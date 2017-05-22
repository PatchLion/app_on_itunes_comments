#!/usr/binenv python
# -*- coding: utf-8 -*-

from comments import template_row_data, template_table_data, template_translate_data
import time

def comments_html_builder(appname, list_comment):
    html = template_table_data
    html = html.replace('%AppName%', appname)
    rows = ""
    for c in list_comment:
        translate_data = template_translate_data
        row_temp = template_row_data
        row_temp = row_temp.replace('%Author%', c.author)
        rating_sting = ''
        for i in range(int(c.rating)):
            rating_sting += "☆"
        row_temp = row_temp.replace('%Star%', rating_sting)
        timeArray = time.localtime(float(c.create_timestamp))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        row_temp = row_temp.replace('%DateTime%', otherStyleTime)
        row_temp = row_temp.replace('%Title%', c.title)
        row_temp = row_temp.replace('%Content%', c.content)
        row_temp = row_temp.replace('%Area%', c.country_or_area)
        row_temp = row_temp.replace('%Version%', c.version)
        if len(c.content_trans_cn) > 0:
            translate_data = translate_data.replace('%Text%', c.content_trans_cn)
            row_temp = row_temp.replace('%Translate%', translate_data)
        else:
            row_temp = row_temp.replace('%Translate%', "")
        rows = rows + row_temp
    html = html.replace('%Rows%', rows)
    return html