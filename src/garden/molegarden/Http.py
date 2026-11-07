#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection
from src.logger.Logger import Logger

class Http:
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def init_garden(self, garden_id):
        try:
            address = f'ajax/ajax.php?do=changeGarden&garden={garden_id}&token={self.__http.token()}'
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            jContent = self.__http.get_json_and_check_for_ok(content)
            return jContent
        except Exception:
            Logger().print_exception('Failed to open molegarden')
            return None
        
    def entry_quest_item(self, pid, amount):
        try:
            address = f'ajax/ajax.php?do=molegarden_entry_quest&pid={pid}&amount={amount}&token={self.__http.token()}'
            print('➡ src/garden/molegarden/Http.py:27 address:', address)
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            jContent = self.__http.get_json_and_check_for_ok(content)
            return jContent
        except Exception:
            Logger().print_exception('Failed to entry quest items in molegarden')
            return None