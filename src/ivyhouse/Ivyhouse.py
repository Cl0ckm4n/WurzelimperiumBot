#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from src.core.User import User
from src.ivyhouse.Http import Http
from src.ivyhouse.ShopProduct import *

class Ivyhouse():
    """Wrapper for the ivyhouse"""

    def __init__(self):
        self.__http = Http()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.DEBUG)

        #TODO:
        self.__update(self.__http.init())

    def __update(self, jContent):
        self.__data = jContent['data']['data']
        print('➡ src/ivyhouse/Ivyhouse.py:22 self.__data:', self.__data)
        self.__breed = self.__data["breed"]
        print('➡ src/ivyhouse/Ivyhouse.py:24 self.__breed:', self.__breed)
        print('➡ src/ivyhouse/Ivyhouse.py:24 self.__breed:', type(self.__breed))

    def __remove_pest(self):
        if self.__breed["pest"]:
            print('➡ src/ivyhouse/Ivyhouse.py:29 self.__breed["pest"]:', self.__breed["pest"])
            for pest in self.__breed["pest"].keys():
                print('➡ src/ivyhouse/Ivyhouse.py:26 pest:', pest)
                self.__http.remove_pest(name=pest, pos=1)

    def __check_weather(self):
        weather = self.__breed["weather"].get("name", None)
        print('➡ src/ivyhouse/Ivyhouse.py:36 weather:', weather)
        weather_id = WEATHER.get(weather, 999)
        print('➡ src/ivyhouse/Ivyhouse.py:42 weather_id:', weather_id)
        weather_remain = self.__breed["weather"].get("remain", -1)
        print('➡ src/ivyhouse/Ivyhouse.py:38 weather_remain:', weather_remain)
        weather_item = self.__breed["weather"].get("item", 999)
        print('➡ src/ivyhouse/Ivyhouse.py:40 weather_item:', weather_item)
        weather_item_name = WEATHER.get(weather_item, 0)
        print('➡ src/ivyhouse/Ivyhouse.py:46 weather_item_name:', weather_item_name)
        weather_item_remain = self.__breed["weather"].get("itemremain", -1)
        print('➡ src/ivyhouse/Ivyhouse.py:42 weather_item_remain:', weather_item_remain)
        
        if weather_item_name and not weather == weather_item_name:
            print("remove Weather")
            self.__http.remove_weather()

        if weather_item_remain < 0:
            print(f"set weather id to {weather_id}")
            self.__http.set_weather(id=weather_id)

    def __check_deco(self):
        pass

    def check_breed(self, slot=GOLDCHILD):
        
        
        if self.__breed == 0:
            print("### START")
            content = self.__http.start_breed(slot)
            self.__update(content)
            # weather
            # deco

        self.__breed.get("remain", 0)
        print('➡ src/ivyhouse/Ivyhouse.py:32 self.__breed.get("remain":', self.__breed.get("remain"))
        print('➡ src/ivyhouse/Ivyhouse.py:32 self.__breed.get("remain":', type(self.__breed.get("remain")))
        if not self.__breed.get("remain", 0) > 0:
            print("### FINISHED")
            content = self.__http.finish_breed()
            self.__update(content)
        
        #remain > 0
        self.__remove_pest()
        self.__check_weather()
           


