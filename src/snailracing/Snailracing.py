#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import os, json

from src.core.User import User
from src.snailracing.Http import Http

RACE_DURATION = 172800 #seconds; 48h
RACE_TERRAIN_ADVANTAGE = 0.2
RACE_TERRAIN_DISADVANTAGE = 0.2


SADDLE_1 = ["grass", "dirt"]
SADDLE_3 = ["gravel", "asphalt"]
BRIDLE_1 = ["sand", "forest"]
BRIDLE_3 = ["dirt", "mud"]

JOCKEY1 = "jockey1" #wT
JOCKEY2 = "jockey2" #Coins

class Snailracing:
    """All important information for the snailracing."""

    

    def __init__(self): #TEMP ,json
        self.__http = Http()
        self.__user = User()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.INFO)
        self.__data = None #TEMP: json
        self.__productions_slots_available = {}
        self.__race_energy = 0 #TEMP int(self.__data["data"]["data"]["race"]["energy"])
        self.update()

    def update(self):
        self.__set_data(self.__http.get_snailracing_info())
    def __set_data(self, j_content):
        self.__data = j_content['data']
        print('➡ src/snailracing/Snailracing.py:139 self.__data:', self.__data)
        self.__race_energy = int(self.__data["data"]["race"]["energy"])
        print('➡ src/snailracing/Snailracing.py:141 self.__race_energy:', self.__race_energy)
        self.__race_remain = int(self.__data["data"]["race"].get("remain", "idle"))
        print('➡ src/snailracing/Snailracing.py:143 self.__race_remain:', self.__race_remain)
    def check_race_feeding(self, pid=473, amount=1):
        print('➡ src/snailracing/Snailracing.py:434 self.__race_energy:', self.__race_energy)
        if self.__race_energy < 100000 and self.__race_remain >= 10000: 
            print("FEEEEEEEEEEEEEEEEEEEEEEED")
            content = self.__http.feed_snail(pid, amount) # feed snail with energy bar
            self.__set_data(content)
