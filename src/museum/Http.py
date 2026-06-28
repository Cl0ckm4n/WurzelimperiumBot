#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection
from src.logger.Logger import Logger

class Http(object):
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def init(self):
        address = f'ajax/ajax.php?do=museum_init&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            print('➡ src/museum/Http.py:17 content:', content)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def collect_points(self):
        address = f'ajax/ajax.php?do=museum_get_bonus&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def activate_plant_booster(self):
        address = f'ajax/ajax.php?do=museum_buy_booster&type=plant&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def activate_megafruit_booster(self):
        address = f'ajax/ajax.php?do=museum_buy_booster&type=megafruit&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise