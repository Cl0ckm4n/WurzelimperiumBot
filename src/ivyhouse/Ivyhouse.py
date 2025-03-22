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
        self.__items = self.__data["items"]
        print('➡ src/ivyhouse/Ivyhouse.py:26 self.__items:', self.__items)

    def __remove_pest(self):
        if self.__breed and self.__breed["pest"]:
            print('➡ src/ivyhouse/Ivyhouse.py:29 self.__breed["pest"]:', self.__breed["pest"])
            for name, occurrence in self.__breed["pest"].items():
                print('➡ src/ivyhouse/Ivyhouse.py:31 occurrence:', occurrence)
                if occurrence:
                    print('➡ src/ivyhouse/Ivyhouse.py:26 pest:', name)
                    self.__http.remove_pest(name=name, pos=1) #TODO: pos anhängig von list?!

    def __check_weather(self):
        weather = self.__breed["weather"].get("name", None)
        print('➡ src/ivyhouse/Ivyhouse.py:36 weather:', weather)
        weather_name = WEATHER.get(weather, 0)
        print('➡ src/ivyhouse/Ivyhouse.py:36 weather_name:', weather_name)
        weather_remain = self.__breed["weather"].get("remain", -1)
        print('➡ src/ivyhouse/Ivyhouse.py:38 weather_remain:', weather_remain)
        weather_item = self.__breed["weather"].get("item", 0)
        print('➡ src/ivyhouse/Ivyhouse.py:40 weather_item:', weather_item)
        weather_item_name = self.__search_item_name(weather_item)
        print('➡ src/ivyhouse/Ivyhouse.py:46 weather_item_name:', weather_item_name)
        weather_item_remain = self.__breed["weather"].get("itemremain", -1)
        print('➡ src/ivyhouse/Ivyhouse.py:42 weather_item_remain:', weather_item_remain)
        
        if weather_item and not weather_name == weather_item_name:
            print("remove Weather")
            self.__http.remove_weather()

        if weather_item_remain < 0:
            item_id = self.__search_item(weather_name)
            if not item_id:
                print("BUY")
                if weather_name:
                    print(f"would buy: {weather_name}")
                    content = self.__http.buy_item(name=weather_name, slot=1, amount=1)
                    self.__update(content)
                    item_id = self.__search_item(weather)
            print("###SET WEATHER###")
            print('➡ src/ivyhouse/Ivyhouse.py:59 item_id:', item_id)
            weather_id = item_id
            content = self.__http.set_weather(id=weather_id)
            print('➡ src/ivyhouse/Ivyhouse.py:66 content:', content)
            self.__update(content)

    def __search_item(self, name):
        id = 0
        values = self.__items.values()

        for listitem in values:
            item_name = listitem.get("name", 0)
            id = listitem.get("id", 0)
            if item_name == name:
                print('➡ src/ivyhouse/Ivyhouse.py:72 id:', id)
                return id
            
    def __search_item_name(self, id):
        item_name = ""
        values = self.__items.values()
        print('➡ src/ivyhouse/Ivyhouse.py:72 values:', values)

        for listitem in values:
            item_name = listitem.get("name", 0)
            item_id = listitem.get("id", 0)
            if item_id == id:
                print('➡ src/ivyhouse/Ivyhouse.py:72 item_name:', item_name)
                return item_name

    def __check_deco(self):
        pass

    def check_breed(self, slot):
        if self.__breed == 0:
            print("### START")
            if slot:
                content = self.__http.start_breed(slot)
                self.__update(content)
            else:
                print("No ivy type specified!")
                return
            # weather
            # deco

        self.__breed.get("remain", 0)
        print('➡ src/ivyhouse/Ivyhouse.py:32 self.__breed.get("remain":', self.__breed.get("remain"))
        print('➡ src/ivyhouse/Ivyhouse.py:32 self.__breed.get("remain":', type(self.__breed.get("remain")))
        if not self.__breed.get("remain", 0) > 0:
            print("### FINISHED")
            content = self.__http.finish_breed()
            rewards = content["data"]["rewards"]
            print('➡ src/ivyhouse/Ivyhouse.py:99 rewards:', rewards)
            self.__update(content)
        
        #remain > 0
        self.__remove_pest()
        self.__check_weather()
           


