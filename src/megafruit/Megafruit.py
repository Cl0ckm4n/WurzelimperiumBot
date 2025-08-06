#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from enum import Enum

from src.megafruit.Http import Http


class Mushroom(Enum):
    Champignon = 69
    Steinpilz = 268
    Pfifferlig = 269
    Speisemorchel = 270
    Kräuter_Seitling = 271
    Riesenträuchling = 272
    Goldener_Flauschling = 999

class Care(Enum):
    Water = "water"
    Light = "light"
    Fertilize = "fertilize"

class Care_OID(Enum):
    """
    {
	"objects": {
		"water": [
			{
				"oid": 1,
				"level": 1,
				"money": 200,
				"points": 83,
				"duration": 28800,
				"unlock": 0
			},
			{
				"oid": 2,
				"level": 5,
				"coins": 1,
				"points": 1310,
				"duration": 201600,
				"unlock": 100
			},
			{
				"oid": 3,
				"level": 9,
				"money": 500,
				"points": 187,
				"duration": 28800,
				"unlock": 160
			},
			{
				"oid": 4,
				"level": 13,
				"coins": 2,
				"points": 3494,
				"duration": 201600,
				"unlock": 250
			},
			{
				"oid": 5,
				"level": 17,
				"fruits": 30,
				"points": 416,
				"duration": 28800,
				"unlock": 400
			},
			{
				"oid": 16,
				"level": 21,
				"coins": 3,
				"points": 3640,
				"duration": 201600,
				"unlock": 1000
			}
		],
		"light": [
			{
				"oid": 6,
				"level": 2,
				"money": 200,
				"points": 94,
				"duration": 28800,
				"unlock": 20
			},
			{
				"oid": 7,
				"level": 6,
				"coins": 1,
				"points": 1310,
				"duration": 201600,
				"unlock": 120
			},
			{
				"oid": 8,
				"level": 10,
				"money": 550,
				"points": 198,
				"duration": 28800,
				"unlock": 180
			},
			{
				"oid": 9,
				"level": 14,
				"coins": 2,
				"points": 3494,
				"duration": 201600,
				"unlock": 300
			},
			{
				"oid": 10,
				"level": 18,
				"fruits": 35,
				"points": 437,
				"duration": 28800,
				"unlock": 450
			},
			{
				"oid": 17,
				"level": 22,
				"coins": 3,
				"points": 3713,
				"duration": 201600,
				"unlock": 1200
			}
		],
		"fertilize": [
			{
				"oid": 11,
				"level": 3,
				"money": 200,
				"points": 104,
				"duration": 28800,
				"unlock": 50
			},
			{
				"oid": 12,
				"level": 7,
				"coins": 1,
				"points": 1310,
				"duration": 201600,
				"unlock": 140
			},
			{
				"oid": 13,
				"level": 11,
				"money": 600,
				"points": 208,
				"duration": 28800,
				"unlock": 200
			},
			{
				"oid": 14,
				"level": 15,
				"coins": 2,
				"points": 3494,
				"duration": 201600,
				"unlock": 350
			},
			{
				"oid": 15,
				"level": 19,
				"fruits": 40,
				"points": 458,
				"duration": 28800,
				"unlock": 500
			},
			{
				"oid": 18,
				"level": 23,
				"coins": 3,
				"points": 3786,
				"duration": 201600,
				"unlock": 1500
			}
		]
	}
}
    """
    Water3 = 3
    Light3 = 8
    Fertilize3 = 13

class Megafruit:
    """All important information for the megafruit."""

    def __init__(self): #TEMP ,json
        self.__http = Http()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.INFO)
        self.__data = None
        self.update()

    def update(self):
        print(self.__http.get_megafruit_info())
        self.__set_data(self.__http.get_megafruit_info())

    def __set_data(self, j_content):
        self.__data = j_content.get("data", None)

    def megafruit_start(self, plant: Mushroom = 0):
        if plant and not self.__data.get("entry", 0):
            pid = plant.value
            print(f"\n\n START Megafruit")
            print('➡ src/megafruit/Megafruit.py:201 plant.value:', plant.value)
            print('➡ src/megafruit/Megafruit.py:203 plant.name:', plant.name)
            data = self.__http.megafruit_start(pid)
            self.__set_data(data)

    def megafruit_finish(self):
        if self.__data.get("remain", 0) < 0:
            data = self.__http.megafruit_finish()
            self.__set_data(data)

    def megafruit_care(self, oid: Care_OID) -> None:
        oid=oid.value

        if oid in range(1,6) or oid == 16:
            print("\n\n CARE WATER")
            self.care(Care.Water, oid)
        if oid in range(6,11) or oid == 17:
            print("\n\n CARE LIGHT")
            self.care(Care.Light, oid)
        if oid in range(11,16) or oid == 18:
            print("\n\n CARE FERTILIZE")
            self.care(Care.Fertilize, oid)

    def care(self, care_name: Care, oid):
        data = self.__data.get("entry", 0).get("data", 0)
        print('➡ src/megafruit/Megafruit.py:214 data:', data)
        print('➡ src/megafruit/Megafruit.py:214 data:', type(data))

        if data == "": #Zucht neu, kein Careitem vorhanden
            print("KEIN CAREITEM 1")
            data = self.__http.megafruit_care(oid = oid)
            self.__set_data(data)
            return
        
        if not data.get("used", 0).get(care_name.value, 0): #kein Careitem vorhanden
            print("KEIN CAREITEM 2")
            data = self.__http.megafruit_care(oid = oid)
            self.__set_data(data)
            return
        
        if data.get("used", 0).get(care_name.value, 0).get("remain", 0) < 0: #Careitem abgelaufen
            print("KEIN CAREITEM 3")
            data = self.__http.megafruit_care(oid = oid)
            self.__set_data(data)
            return
"""
        "entry": {
			"pid": "272",
			"points": "244",
			"data": {
				"used": {
					"water": {
						"oid": 3,
						"time": 1705427331,
						"duration": 28800,
						"remain": 28800
					}
				}
			},
			"createdate": "1705427210"
		},
		"fruit_percent": 10,
		"remain": 604679,
"""