#!/usr/binenv python
# -*- coding: utf-8 -*-

import logging
mylogger = logging.getLogger()
mylogger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler(filename='log.log', encoding="utf-8")
filehandler.setLevel(logging.WARN)
streamhanler = logging.StreamHandler()
streamhanler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
filehandler.setFormatter(formatter)
streamhanler.setFormatter(formatter)
mylogger.addHandler(filehandler)
mylogger.addHandler(streamhanler)
mylogger.info("Config logging!")
