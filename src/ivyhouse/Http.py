#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection

class Http(object):
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def init(self):
        """Selects ivyhouse returns JSON content"""
        address = f'ajax/ajax.php?do=ivyhouse_init&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def start_breed(self, slot):
        #slot == type of ivy 1,2,...,7
        """Start ivy and returns JSON content"""
        address = f'ajax/ajax.php?do=ivyhouse_start_breed&slot={slot}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def finish_breed(self):
        """Finishes ivy and returns JSON content"""
        address = f'ajax/ajax.php?do=ivyhouse_finish_breed&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def remove_pest(self, name, pos):
        #name = pest (Schnecke), water (Wassertropfen)
        #pos = 1, weitere?
        address = f'ajax/ajax.php?do=ivyhouse_remove_pest&name={name}&pos={pos}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def set_deco(self, slot, id):
        #slot = 1,2,3,4
        #id = 143 (Vogel)
        address = f'ajax/ajax.php?do=ivyhouse_set_deco&slot={slot}&id={id}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def set_deco(self, slot):
        #slot = 1,2,3,4
        address = f'ajax/ajax.php?do=ivyhouse_remove_deco&slot={slot}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def set_weather(self, id):
        #id = 145(???)
        address = f'ajax/ajax.php?do=ivyhouse_set_weather_item&id={id}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def remove_weather(self):
        address = f'ajax/ajax.php?do=ivyhouse_remove_weather_item&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise

    def buy_item(self, name, slot, amount):
        #name = deco5
        #slot = 1
        #amount = 2
        address = f'ajax/ajax.php?do=ivyhouse_buy_shop_item&name={name}&slot={slot}&amount={amount}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            jContent = self.__http.generateJSONContentAndCheckForOK(content)
            return jContent
        except:
            raise
