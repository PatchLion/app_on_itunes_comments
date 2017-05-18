#!/usr/binenv python
# -*- coding: utf-8 -*-

import logging
from scrapy.utils.log import configure_logging
def config_logging():
    #print("Config logging!")
    configure_logging(install_root_handler=False)
    filehandler = logging.FileHandler(filename='log.log', encoding="utf-8")
    filehandler.setLevel(logging.WARN)
    streamhanler = logging.StreamHandler()
    streamhanler.setLevel(logging.INFO)
    logging.basicConfig(handlers=[filehandler, streamhanler],
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.WARN)
