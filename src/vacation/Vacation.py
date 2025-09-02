#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from src.logger.Logger import Logger
from src.product.Product import Product
from src.product.ProductData import ProductData
from src.shop.Shop import Shop
from src.stock.Stock import Stock
from src.vacation.Http import Http

CUSTOMER_INTEREST_MATCH_BONUS = 0.65
CUSTOMER_BASE_REWARD_MONEY = 850
CUSTOMER_BASE_REWARD_POINTS = 1200
CUSTOMER_BASE_REWARD_VACATION_POINTS= 10

class Vacation:
    """Wrapper for the Vacation"""

    def __init__(self):
        self.__http = Http()
        self.__shop = Shop()
        self.__stock = Stock()
        self.__data = None
        self.update()

    def update(self):
        self.__set_data(self.__http.get_info())
        self.__get_available_locations()

    def __set_data(self, content):
        self.__data = content.get("data", None)
        self.__locations = self.__data["data"]["locations"]

        self.__items = self.__data["data"]["items"] 

        self.__customers = self.__data["data"]["customers"]
        self.__customers = dict(sorted(self.__customers.items(), key=lambda item: len(item[1].get('interests', []))))

    def __get_available_locations(self) -> None:
        self.__available_locations = []
        for location in self.__locations.keys():
            slots = self.__get_location_slots(location)
            print('➡ src/vacation/Vacation.py:52 slots:', slots)
            slots_available = []
            if not slots:
                continue
            for slot, slotdata in slots.items():
                remain = slotdata.get("remain", 999)
                if remain > 0: continue
                slots_available.append(slot)
            print('➡ src/vacation/Vacation.py:62 slots_available:', slots_available)

            if slots_available:
                self.__available_locations.append(location)
                print('➡ src/vacation/Vacation.py:97 self.__available_locations:', self.__available_locations)
            else:
                Logger().error("No location available")

    def __get_location_energy(self, location_level) -> int:
        return int(self.__data.get("config",{}).get("location_level",{}).get(str(location_level),{}).get("energy",9999))
    
    def __get_location_slots(self, location_id) -> dict:
        slots = self.__data.get("data",{}).get("locations",{}).get(location_id,{}).get("slots",{})
        print('➡ src/vacation/Vacation.py:78 slots:', slots)
        level = self.__get_location_level(location_id)
        print('➡ src/vacation/Vacation.py:79 level:', level)
        if slots == None: slots = {}
        slots_count = len(slots.keys())
        print('➡ src/vacation/Vacation.py:80 slots_count:', slots_count)

        if level == 1 and slots_count == 0:
            slots.update({1: {"remain": -1}})

        if level == 2 and slots_count == 0:
            slots.update({1: {"remain": -1}})
            slots.update({2: {"remain": -1}})
        if level == 2 and slots_count == 1:
            slots.update({2: {"remain": -1}})

        if level >= 3 and slots_count == 0:
            slots.update({1: {"remain": -1}})
            slots.update({2: {"remain": -1}})
            slots.update({3: {"remain": -1}})
        if level >= 3 and slots_count == 1:
            slots.update({2: {"remain": -1}})
            slots.update({3: {"remain": -1}})
        if level >= 3 and slots_count == 2:
            slots.update({3: {"remain": -1}})

        print('➡ src/vacation/Vacation.py:102 slots:', slots)
        return slots
        
    
    def __get_location_products(self, location_id) -> dict:
        return self.__data.get("config",{}).get("location",{}).get(location_id,{}).get("products",{})
    
    def __get_location_interests(self, location_id) -> list:
        interests = self.__data.get("config",{}).get("location",{}).get(location_id,{}).get("interests",[])
        return interests
    
    def __get_location_reward_multi(self, location_id) -> dict:
        return self.__data.get("config",{}).get("location",{}).get(location_id,{}).get("reward_multi",{})
    
    def __get_location_name(self, location_id) -> str:
        return self.__data.get("config",{}).get("location",{}).get(location_id,{}).get("name",{})
    
    def __get_location_level(self, location_id) -> int:
        return self.__data.get("data",{}).get("locations",{}).get(location_id,{}).get("level",{}).get("level",0)

    def harvest_locations(self) -> None:
        for location_id in self.__locations.keys():
            print('➡ src/vacation/Vacation.py:82 location_id:', location_id)
            slots = self.__get_location_slots(location_id)
            for slot, slotdata in slots.items():
                remain = slotdata.get("remain", 999)
                print('➡ src/vacation/Vacation.py:136 remain:', remain)
                customerid = slotdata.get("customerid", 0)
                print('➡ src/vacation/Vacation.py:129 customerid:', customerid)
                if remain < 0 and customerid:
                    print(f"\n\n ###HARVEST location_id: {location_id} slot: {slot}###")
                    content = self.__http.harvest_location_slot(id = location_id, slot = slot)
                    self.__set_data(content)

    def refill_locations(self, refill_energy_level = 1000, buy_from_shop: bool = True) -> None:
        for location, data in self.__locations.items():
            energy = int(data.get("energy", 0))
            if energy < refill_energy_level:
                pid, amount = self.__calc_cheapest_product(location, data, energy, self.__get_location_products(location))
                if pid:
                    if self.__stock.get_stock_by_product_id(pid) < amount:
                        if buy_from_shop:
                            self.__shop.buy(product_name=pid, amount=amount)
                        else:
                            return
                    print(f"\n\n ###REFILL location_id: {location} pid: {pid} amount: {amount}###")
                    content = self.__http.refill_location(id = location, pid = pid, amount = amount)
                    self.__set_data(content)

    def __calc_cheapest_product(self, location, data, energy, location_pids: dict):
        costs = {}
        amounts = {}
        
        location_level = data.get("level",{}).get("level",0)
        location_energy_max = self.__get_location_energy(location_level)
        for pid, pid_energy in location_pids.items():
            product: Product = ProductData().get_product_by_id(pid)
            pid_price = product.get_price_npc()
            amount = math.floor((location_energy_max-energy)/pid_energy)
            cost = amount * pid_price
            costs.update({pid: cost})
            amounts.update({pid: amount})

        if not costs:
            return False
        best_pid = min(costs, key=costs.get)
        return best_pid, amounts[best_pid]


    def check_customers(self, item_name="toiletry_bag"):
        print(f"PROCESS CUSTOMERS: {self.__customers}")
        for customer_id, customer_data in self.__customers.items():
            print('➡ src/vacation/Vacation.py:176 customer_id:', customer_id)
            print('➡ src/vacation/Vacation.py:176 customer_data:', customer_data)
            location = customer_data["location"] # location where customer is
            print('➡ src/vacation/Vacation.py:135 location:', location)
            if location != "0":
                Logger().info(f"Skip customer {customer_id} (already in location {location})")
                continue #customer already on vacation

            # check interests mit locations aus config, if location free
            possible_locations = []
            interests = customer_data["interests"]
            print('➡ src/vacation/Vacation.py:188 self.__available_locations:', self.__available_locations)
            for location in self.__available_locations:
                print('➡ src/vacation/Vacation.py:146 location:', location)
                location_interests = self.__get_location_interests(location)
                print('➡ src/vacation/Vacation.py:147 location_interests:', location_interests)
                if any(item in interests for item in location_interests):
                    possible_locations.append(location)
                    print('➡ src/vacation/Vacation.py:195 possible_locations:', possible_locations)

            # calc dict(location:vac-points), # location mit höchsten rewards finden
            locations_rewards = {}
            for location in possible_locations:
                location_multi = self.__get_location_reward_multi(location)
                location_multi_vac = float(location_multi.get("vacation_points", 0))
                interest_match = sum(interest in interests for interest in location_interests)
                print('➡ src/vacation/Vacation.py:214 interest_match:', interest_match)
                print('➡ src/vacation/Vacation.py:214 interest_match:', type(interest_match))
                reward = CUSTOMER_BASE_REWARD_VACATION_POINTS * location_multi_vac * (1+0.4+interest_match*CUSTOMER_INTEREST_MATCH_BONUS+0.3) #0.4= location lvl5 bonus; 0.3 3xitem toiletry bag
                reward = math.ceil(reward)
                locations_rewards.update({location: reward})
            print('➡ src/vacation/Vacation.py:201 locations_rewards:', locations_rewards)

            best_locations = [key for key in locations_rewards if locations_rewards[key] == max(locations_rewards.values())]
            print('➡ src/vacation/Vacation.py:204 best_locations:', best_locations)
            if not len(best_locations) > 0:
                print("Error: no locations available")
                continue
            
            best_location = best_locations[0]

            # check items
            requested_items = []
            items = self.__items
            for item_id, data in items.items():
                if data.get("name", "") == item_name and data.get("instock", "") == "1":
                    requested_items.append(item_id) 

            ## buy items
            if len(requested_items) < 3:
                content = self.__http.buy_item(name = item_name, amount = 10)
                self.__set_data(content)

            ## check items after buying
            requested_items = []
            items = self.__items
            for item_id, data in items.items():
                if data.get("name", "") == item_name and data.get("instock", "") == "1":
                    requested_items.append(item_id)

            item1_id = requested_items[0]
            print('➡ src/vacation/Vacation.py:252 item1_id:', item1_id)
            item2_id = requested_items[1]
            print('➡ src/vacation/Vacation.py:254 item2_id:', item2_id)
            item3_id = requested_items[2]
            print('➡ src/vacation/Vacation.py:256 item3_id:', item3_id)

            ## get free slots of location
            book_slot = 0
            slots = self.__get_location_slots(best_location)
            for slot, slotdata in slots.items():
                print('➡ src/vacation/Vacation.py:116 slotdata:', slotdata)
                print('➡ src/vacation/Vacation.py:86 slot:', slot)
                remain = slotdata.get("remain", 999)
                print('➡ src/vacation/Vacation.py:136 remain:', remain)
                if remain < 0 and not slotdata.get("customerid", 0):
                    book_slot = slot
                    break

            # setup: {"customerid":31485,"slot":"1","items":{"1":15141,"2":15144,"3":15143}}
            if book_slot:
                setup=f'{{"customerid":{customer_id},"slot":"{book_slot}","items":{{"1":{item1_id},"2":{item2_id},"3":{item3_id}}}}}'
                if self.__get_location_level(best_location) == 1:
                    setup=f'{{"customerid":{customer_id},"slot":"{book_slot}","items":{{"1":{item1_id}}}}}'
                if self.__get_location_level(best_location) == 2:
                    setup=f'{{"customerid":{customer_id},"slot":"{book_slot}","items":{{"1":{item1_id},"2":{item2_id}}}}}'
                print('➡ src/vacation/Vacation.py:279 setup:', setup)
                
                # book location
                print(f"\n\n ###BOOK location_id: {best_location}###")
                content = self.__http.book_location(best_location, setup = setup)
                self.__set_data(content)
                self.__get_available_locations()
            else:
                print("ERROR: could book customer")
