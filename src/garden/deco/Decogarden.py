#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from src.garden.deco.Http import Http

class Decogarden1():
    """Wrapper for the Decogarden 1"""

    def __init__(self):
        self.__http = Http()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.DEBUG)
        self.__http.init_decogarden_1()

    def collect(self):
        content = self.__http.collect_decogarden_1()
        print('➡ src/garden/deco/Decogarden.py:18 content:', content)
        collected = content.get("message", "Collected nothing!")
        self.__log.info(collected)

class Decogarden2():
    """Wrapper for the Decogarden 2"""

    def __init__(self):
        self.__http = Http()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.DEBUG)
        self.__http.init_decogarden_2()

    def collect(self):
        content = self.__http.collect_decogarden_2()
        collected = content.get("data", "None").get("reward", "None")
        self.__log.info(collected)