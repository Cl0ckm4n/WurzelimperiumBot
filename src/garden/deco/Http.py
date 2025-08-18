#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from src.core.HTTPCommunication import HTTPConnection

class Http(object):
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def init_decogarden_1(self):        
        address = f'ajax/decogardenajax.php?do=getGarden'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def collect_decogarden_1(self):
        address = f'ajax/decogardenajax.php?do=premiumCollector'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            jContent = json.loads(content)
            return jContent
        except:
            raise

    def init_decogarden_2(self):
        address = f'ajax/ajax.php?do=decogarden2_init&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def collect_decogarden_2(self):
        address = f'ajax/ajax.php?do=decogarden2_collect_all_items&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise