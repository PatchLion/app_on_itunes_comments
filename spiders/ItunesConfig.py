#!/usr/binenv python
# -*- coding: utf-8 -*-

import json

class ItunesConfig(object):
    def __init__(self):
        with open("itunes.config", 'r', encoding='utf-8') as f:
            json_dict = json.loads(f.read(), encoding='utf-8')
            self._areas = json_dict['areas']
            self._appids = json_dict['appids']
            self._delay = int(json_dict['delay'])

    def areas(self):
        return self._areas

    def appids(self):
        return self._appids

    def delay(self):
        return self._delay