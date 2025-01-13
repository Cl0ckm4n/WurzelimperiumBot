#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import math
from collections import Counter
from src.core.User import User
from src.biogas.Http import Http
from src.biogas.Products import STOCKS
from src.product.Product import Product
from src.product.ProductData import ProductData

class Stocks:
    RUBBISH = "rubbish"


class Biogas:
    """All important information for the recycling center."""

    def __init__(self):
        self.__http = Http()
        self.__user = User()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.DEBUG)
        self.__data = None
        self.__bonus = 0
        self.update()

    def update(self):
        self.__set_data(self.__http.get_recycling_center_info())
        self.__bonus = int(self.__data['data']["lastquest"])*0.15 #+15% bonus for each finished quest
        print('➡ src/biogas/Biogas.py:31 self.__bonus:', self.__bonus)

    def sell_to_wimp(self, slot):
        data = self.__http.sell_to_wimp(slot)
        wimp_rubbish = self.__get_wimps_data().get("1").get("data").get("rubbish")
        self.__log.info(f"Sold {wimp_rubbish} rubbish.")
        self.__set_data(data)

    def calculate_rubbish(self, plants: Counter):
        # formula: 4 / Anz. Gärten / 24 x Felder x Wachstumsdauer (Original in Std.) x 1+Bonus 
        # Wenn mehrere verschiedene Pflanzen gleichzeitig geerntet werden, wird die Berechnung für jede Pflanze separat durchgeführt und dann gerundet.
#         Am Ende werden die gerundeten Werte addiert.
        rubbish = 0

        # sum of harvestable plants as input
        for plant, plant_count in plants.items():
            print('➡ src/biogas/Biogas.py:38 plant:', plant)
            print('➡ src/biogas/Biogas.py:38 plant_count:', plant_count)
            product: Product = ProductData().get_product_by_id(plant)
            rubbish += 4/self.__user.get_number_of_gardens()/24*product.get_sx()*product.get_sy()*int(plant_count)*product.get_growing_time()/3600*(1+self.__bonus)
            print('➡ src/biogas/Biogas.py:40 rubbish_biogas:', rubbish)
        rubbish_rounded = math.floor(rubbish + 0.5) / 1 # round_half_up
        print('➡ src/biogas/Biogas.py:59 rubbish_rounded:', rubbish_rounded)
        rubbish_rounded_py = round(rubbish)
        print('➡ src/biogas/Biogas.py:59 rubbish_rounded_py:', rubbish_rounded_py)
        return rubbish_rounded

    def check_rubbish_capacity(self, rubbish_to_add) -> bool:
        self.update()
        rubbish_stock = float(self.__get_stock().get("rubbish"))
        print('➡ src/biogas/Biogas.py:65 rubbish_stock:', rubbish_stock)
        return rubbish_to_add + rubbish_stock < self.__get_stock_capacity(STOCKS.RUBBISH)
    # Internal helper functions

    def __set_data(self, j_content):
        self.__data = j_content['data']

    def __get_wimps_data(self):
        return self.__data['data']["customers"]

    def __get_stock(self) -> dict:
        return self.__data['data']["stock"]
    def __get_stock_capacity(self, stock: STOCKS):
        config = self.__data["config"]["stock_level"][stock.value]
        stock_level = self.__data["data"]["stock_level"][stock.value]
        return config.get(str(stock_level)).get("capacity")
