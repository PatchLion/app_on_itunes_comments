#!/usr/binenv python
# -*- coding: utf-8 -*-

import json

class ItunesConfig(object):
    def _config(self):
        with open("itunes.config", 'r', encoding='utf-8') as f:
            json_dict = json.loads(f.read(), encoding='utf-8')
            return json_dict
        return {}

    def areas(self):
        return self._config.get('areas', [])

    def appids(self):
        return self._config().get('appids', [])

    def delay(self):
        d = int(self._config().get('delay', 1))
        if d <= 0:
            d = 1
        return d
