#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.garden.Garden import Garden
from src.garden.molegarden.Http import Http
from src.shop.Shop import Shop
from src.stock.Stock import Stock

class Molegarden(Garden):
    def __init__(self):
        Garden.__init__(self, 111)
        self.http_mole = Http()
        self.__shop = Shop()
        self.__stock = Stock()
        self.__data = None
        self.__set_data(self.http_mole.init_garden(self._id))

    def __set_data(self, content):
        self.__data = content

    def __get_lastmole_remain(self) -> int: #Zeit bis nächster Maulwurfhügel kommt
        return self.__data.get("molegarden", {}).get("data", {}).get("lastmole_remain", 999999)

    def __get_quest_remain(self) -> int: #Zeit bis nächster Maulwurfhügel entfernt werden kann
        return self.__data.get("molegarden", {}).get("data", {}).get("quest", {}).get("remain", 999999)

    def __get_quest_data(self): #Questinhalt
        return self.__data.get("molegarden", {}).get("data", {}).get("quest", {}).get("data", {})

    def do_quest(self, buy_from_shop = True):
        if self.__get_quest_remain() > 0:
            print("\n\nNext quest not ready!")
            return False

        for pid, amount in self.__get_quest_data().items():
            print('➡ src/garden/molegarden/Molegarden.py:47 pid:', pid)
            need = amount.get("need", 0)
            print('➡ src/garden/molegarden/Molegarden.py:49 need:', need)
            have = amount.get("have", 0)
            print('➡ src/garden/molegarden/Molegarden.py:51 have:', have)
            to_submit = need-have
            print('➡ src/garden/molegarden/Molegarden.py:54 to_submit:', to_submit)
            if not to_submit > 0:
                return False

            if self.__stock.get_stock_by_product_id(pid) < to_submit:
                if buy_from_shop:
                    buy = self.__shop.buy(product_name=int(pid), amount=to_submit)
                    if not buy:
                        print("ERROR0 - buying failed")
                        return False
                else: 
                    print("ERROR1 - buying disabled")
                    return False
            else: print("ERROR2 - no buy needed")

            content = self.http_mole.entry_quest_item(pid, to_submit)
            self.__set_data(content)
