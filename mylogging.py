#!/usr/binenv python
# -*- coding: utf-8 -*-

import logging
from scrapy.utils.log import configure_logging
def config_logging():
    print("Config logging!")
    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='log.log',
                        format='%(levelname)s: %(message)s',
                        level=logging.WARN)
