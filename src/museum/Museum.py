#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.museum.Http import Http
from src.megafruit.Megafruit import Megafruit

class Museum:
    """Wrapper for the Museum"""

    def __init__(self):
        self.__http = Http()
        self.__data = None
        self.update()

    def update(self):
        self.__set_data(self.__http.init())

    def __set_data(self, content):
        self.__data = content.get("data", {}).get("data", None)

    def collect_points(self):
        if self.__data.get("lastclick_remain", 999999) > 0:
            print("No points to collect!")
            return False
        content = self.__http.collect_points()
        print(f"Collected {content.get("rewards", {}).get("points", "n/a")} points.")

    def check_booster(self):
        megafruit_booster = self.__data.get("booster", {}).get("megafruit", {}).get("remain", 999999)
        if Megafruit().action_needed():
            if not megafruit_booster > 0:
                self.__http.activate_megafruit_booster()

        plant_booster = self.__data.get("booster", {}).get("plant", {}).get("remain", 999999)
        #if garden_harvest_needed(): #TODO: jeden einzelnen Garten checken, ob etwas fertig ist --> andere Lösung?
        if not plant_booster > 0:
            self.__http.activate_plant_booster()