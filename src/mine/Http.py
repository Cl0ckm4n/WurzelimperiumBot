#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection
from src.logger.Logger import Logger

class Http(object):
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def init(self):
        address = f'ajax/ajax.php?do=mine_init&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def finish_worker(self, layer, position):
        address = f'ajax/ajax.php?do=mine_finish&level={layer}&position={position}&token={self.__http.token()}'
        print('➡ src/mine/Http.py:22 address:', address)
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def refill_worker_energy(self, slot, pid, amount):
        address = f'ajax/ajax.php?do=mine_refill&slot={slot}&pid={pid}&amount={amount}&token={self.__http.token()}'
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def start_worker(self, setup):
        """{"level":6,"pos":3,"favdino":"dino2","worker":{"1":3,"2":6},"items":{"1":171447,"2":171450},"dinos":{"1":171451,"2":171452}}"""
        address = f'ajax/ajax.php?do=mine_harvest&setup={{{setup}}}&token={self.__http.token()}'
        #https://s8.wurzelimperium.de/ajax/ajax.php?do=mine_harvest&setup={"level":6,"pos":2,"favdino":"dino2","worker":{"1":6,"2":5},"items":{"1":171447,"2":171448},"dinos":{"1":171451,"2":171452}}&token=1519d43fb9e364c0657ccf99613d0b21
        print('➡ src/mine/Http.py:42 address:', address)
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise

    def craft_item(self, name):
        address = f'ajax/ajax.php?do=mine_buy_shop_item&name={name}&harvesterslot&dinoslot&token={self.__http.token()}'
        print('➡ src/mine/Http.py:51 address:', address)
        try:
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except:
            raise