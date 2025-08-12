#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.core.HTTPCommunication import HTTPConnection

class Http(object):
    def __init__(self):
        self.__http: HTTPConnection = HTTPConnection()

    def get_megafruit_info(self):
        address = f'ajax/ajax.php?do=megafruit_init&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise

    def megafruit_start(self, pid):
        address = f'ajax/ajax.php?do=megafruit_start&pid={pid}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise
            """
                "status": "error",
                "message": "Du hast leider nicht genug auf Lager.",
                "errorcode": 0,
                "trace": ""
            """

    def megafruit_care(self, oid):
        address = f'ajax/ajax.php?do=megafruit_set_object&oid={oid}&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise

    def megafruit_finish(self):
        pass
        address = f'ajax/ajax.php?do=megafruit_harvest&token={self.__http.token()}'
        try:
            response, content = self.__http.sendRequest(address)
            self.__http.checkIfHTTPStateIsOK(response)
            return self.__http.generateJSONContentAndCheckForOK(content)
        except:
            raise