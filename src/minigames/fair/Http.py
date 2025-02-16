#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection

class Http(object):
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def fair_init(self):
        address = f"ajax/ajax.php?do=fair_init&init=1&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise

    def fair_craft_ticket(self):
        address = f"ajax/ajax.php?do=fair_craftticket&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise
    
    def fair_pay_ticket(self, type):
        """
        @param: type = wetgnome, thimblerig
        """
        address = f"ajax/ajax.php?do=fair_payticket&type={type}&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise
    
    # Thimblerig, Hütchenspieler
    def fair_thimblerig_start(self):
        address = f"ajax/ajax.php?do=thimblerig_start&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise
    
    def fair_thimblerig_select(self, mug: int):
        """
        @param: mug = 1, 2, 3
        """
        address = f"ajax/ajax.php?do=thimblerig_select&mug={mug}&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise
    
    # Wetgnome, Nasser Zwerg
    def fair_wetgnome_start(self):
        address = f"ajax/ajax.php?do=wetgnome_start&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise
    
    def fair_wetgnome_select(self, x, y):
        """
        @param: x = game_id + position, y = game_id + position
        """
        address = f"ajax/ajax.php?do=wetgnome_select&x={x}&y={y}&token={self.__http.token()}"
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise