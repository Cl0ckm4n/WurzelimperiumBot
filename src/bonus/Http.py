#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection
from src.core.HttpUser import Http as HttpUser
from src.logger.Logger import Logger

class Http:
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()
        self.__httpUser = HttpUser()

    def get_daily_login_bonus(self, day):
        """@param day: string (day of daily bonus)"""
        try:
            address = f'ajax/ajax.php?do=dailyloginbonus_getreward&day={str(day)}&token={self.__http.token()}'
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except Exception:
            Logger().print_exception("Failed to get daily login bonus")
            return None

    def set_daily_login_bonus_plant(self, plant_id):
        try:
            address = f'ajax/ajax.php?do=dailyloginbonus_setplant&pid={plant_id}&token={self.__http.token()}'
            response, content = self.__http.send(address)
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except Exception:
            Logger().print_exception("Failed to set daily login bonus plant on day 7")
            return None

    def read_user_data(self):
        return self.__httpUser.load_data("dailyloginbonus")['dailyloginbonus']

    def init_garden_shed(self) -> bool:
        try:
            response, content = self.__http.send(f'ajax/ajax.php?do=houseInit&token={self.__http.token()}')
            self.__http.check_http_state_ok(response)
            self.__http.get_json_and_check_for_ok(content)
            return True
        except Exception:
            Logger().print_exception("Failed to init garden shed")
            return False

    def open_trophy_case(self, category) -> bool:
        """category: giver, paymentitemcollection"""
        try:
            response, content = self.__http.send(f'ajax/gettrophies.php?category={category}')
            self.__http.check_http_state_ok(response)
            content = self.__http.get_json_and_check_for_ok(content)
            if category == "paymentitemcollection":
                bonustoday = content.get("paymentcollection", {}).get("data", {}).get("bonustoday", 0)
                if not bonustoday:
                    return False
            return True
        except Exception:
            Logger().print_exception("Failed to open trophy case")
            return False

    def collect_bonus_items(self):
        try:
            response, content = self.__http.send(f'ajax/presentclick.php', 'POST')
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except Exception:
            Logger().print_exception("Failed to collect bonus items")

    def collect_figurines(self):
        try:
            response, content = self.__http.send(f'ajax/ajax.php?do=paymentcollection_collect&token={self.__http.token()}')
            self.__http.check_http_state_ok(response)
            return self.__http.get_json_and_check_for_ok(content)
        except Exception:
            Logger().print_exception("Failed to collect figurines")
            return False
