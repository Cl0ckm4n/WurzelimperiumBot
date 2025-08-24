#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.product.Product import Product
from src.product.ProductData import ProductData
from src.shop.Shop import Shop
from src.stock.Stock import Stock
from src.birds.Http import Http


class Birds:
    """Wrapper for the Birds"""

    def __init__(self):
        self.__http = Http()
        self.__shop = Shop()
        self.__stock = Stock()
        self.__data = None
        self.update()

    def update(self):
        self.__set_data(self.__http.get_info())

    def __set_data(self, content):
        self.__data = content.get("data", None)
        self.__houses = self.__data["data"]["houses"]
        self.__jobs = self.__data["data"]["jobs"]

    def __get_house_bird_endurance(self, house):
        return self.__houses.get(house, {}).get("bird", {}).get("endurance", 0)
    
    def __get_house_bird_load_max(self, house):
        return self.__houses.get(house, {}).get("bird", {}).get("load_max", 0)

    def __get_available_houses(self) -> list:
        return list(self.__houses.keys())

    def __get_occupied_houses(self) -> list:
        occupied_houses = []
        for job_id, job_data in self.__jobs.items():
            house = job_data.get("house", None)
            if not job_data.get("house", None) == "0":
                occupied_houses.append(house)
        print('➡ src/birds/Birds.py:46 occupied_houses:', occupied_houses)
        return occupied_houses
    
    def __get_free_jobs(self) -> list:
        free_jobs = []
        for job_id, job_data in self.__jobs.items():
            if job_data.get("house", None) == "0" and job_data.get("remove_remain", 0) <= 0:
                free_jobs.append(job_id)
        print('➡ src/birds/Birds.py:55 free_jobs:', free_jobs)
        return free_jobs

    #Job nicht zugeteilt
    """
    id	"692158"
    unr	"1458480"
    slot	"5"
    size	"1"
    distance	"3"
    endurance	"3"
    products	{ 2: 2286, 59: 1 }
    rewards	{ money: 1362, points: 1010, feather: 23, … }
    house	"0"
    duration	"0"
    remove_cooldown	"0"
    createdate	"1755676482"
    startdate	"0"
    finishdate	"0"
    """

    # Job fertig
    """
    id	"649411"
    unr	"1458480"
    slot	"2"
    size	"2"
    distance	"2"
    endurance	"3"
    products	{ 11: 32, 409: 1, 410: 3 }
    rewards	{ money: 1356, points: 520, feather: 13, … }
    house	"4"
    duration	"14400"
    remove_cooldown	"0"
    createdate	"1740912679"
    startdate	"1740912752"
    finishdate	"0"
        remain	-14750096
    """

    #Job running
    """
    id	"692159"
    unr	"1458480"
    slot	"6"
    size	"2"
    distance	"3"
    endurance	"4"
    products	{ 12: 1073, 36: 77, 410: 2 }
    rewards	{ money: 2117, points: 1020, feather: 24, … }
    house	"3"
    duration	"28800"
    remove_cooldown	"0"
    createdate	"1755676602"
    startdate	"1755677541"
    finishdate	"0"
        remain	28800
    """


    def finish_jobs(self) -> None:
        for job, data in self.__jobs.items():
            remain = data.get("remain", 0)
            slot = data.get("slot", 0)
            if remain < 0 and slot:
                print(f"\n\n ###FINISH job: {job} in slot: {slot}###")
                content = self.__http.finish_job(slot=slot)
                self.__set_data(content)

    def feed_and_renew_birds(self, buy_from_shop: bool = True, bird_nr = 3) -> None:
        for house, data in self.__houses.items():
            print('➡ src/birds/Birds.py:138 house:', house)

            if house in self.__get_occupied_houses():
                continue
            bird = data.get("bird", 0)
            print('➡ src/birds/Birds.py:150 bird:', bird)
            if bird: #bird in house, check if feeding necessary
                feed_products = bird.get("feed", {})
                print('➡ src/birds/Birds.py:155 feed_products:', feed_products)
                endurance = bird.get("endurance", 0)
                print('➡ src/birds/Birds.py:157 endurance:', endurance)
                endurance_max = bird.get("endurance_max", 0)
                print('➡ src/birds/Birds.py:159 endurance_max:', endurance_max)
                if endurance < endurance_max:
                    if self.__check_feed_products(feed_products, buy_from_shop):
                        print(f"\n\n ###FEED house: {house}###")
                        content = self.__http.feed_bird(slot=house)
                        self.__set_data(content)
            else: #no bird in house --> buy a new one #TODO: not tested
                print(f"\n\n ###BUY bird: {bird_nr} for house {house}###")
                content = self.__http.buy_bird(house=house, bird_nr=bird_nr)
                self.__set_data(content)

    def __check_feed_products(self, feed_products: dict, buy_from_shop: bool) -> bool:
        for pid, amount in feed_products.items():
            product: Product = ProductData().get_product_by_id(pid)
            if product:
                if self.__stock.get_stock_by_product_id(pid) < amount:
                    if buy_from_shop:
                        buy = self.__shop.buy(product_name=pid, amount=amount)
                        if not buy:
                            return False
                    else: 
                        print("ERROR1 - buying disabled")
                        return False
                else: print("ERROR2 - no buy needed")
            else: 
                print("ERROR3 - no product found")
                return False
        return True

    def start_birds(self, buy_from_shop: bool = True):
        free_houses = [x for x in self.__get_available_houses() if x not in self.__get_occupied_houses()]
        print('➡ src/birds/Birds.py:195 free_houses:', free_houses)

        impossible_jobs=[]

        for house in free_houses:
            print('\n\n➡ src/birds/Birds.py:204 house:', house)
            house_bird_endurance = self.__get_house_bird_endurance(house)
            print('➡ src/birds/Birds.py:205 house_bird_endurance:', house_bird_endurance)
            house_bird_load_max = self.__get_house_bird_load_max(house)
            print('➡ src/birds/Birds.py:207 house_bird_load_max:', house_bird_load_max)
            
            possible_jobs={}
            #TODO: get best job (maximize rewards?!)
            for job in self.__get_free_jobs():
                print('\n➡ src/birds/Birds.py:242 impossible_jobs:', impossible_jobs)
                print('➡ src/birds/Birds.py:192 job:', job)
                job_data = self.__jobs.get(job, 0)
                if not job_data:
                    if job not in impossible_jobs:
                        impossible_jobs.append(job)
                    continue
                print('➡ src/birds/Birds.py:195 job_data:', job_data)
                job_size = job_data.get("size", 0) #str; size --> load --> load_max of bird
                print('➡ src/birds/Birds.py:216 job_size:', job_size)
                print('➡ src/birds/Birds.py:234 self.__get_house_bird_load_max():', self.__get_house_bird_load_max(house))
                if not self.__get_house_bird_load_max(house) >= int(job_size):
                    if job not in impossible_jobs:
                        impossible_jobs.append(job)
                    continue
                print("load ok")

                job_distance = job_data.get("distance", 0) #not relevant (je höher, desto mehr rewards)
                print('➡ src/birds/Birds.py:220 job_distance:', job_distance)

                job_endurance = job_data.get("endurance", 0)#str; compare with bird_endurance
                print('➡ src/birds/Birds.py:222 job_endurance:', job_endurance)
                if not self.__get_house_bird_endurance(house) >= int(job_endurance):
                    if job not in impossible_jobs:
                        impossible_jobs.append(job)
                    continue
                print("endurance ok")

                if job in impossible_jobs:
                    impossible_jobs.remove(job)

                job_products = job_data.get("products", 0)#dict; check Stock if available; if not buy
                print('➡ src/birds/Birds.py:236 job_products:', job_products)
                for pid, amount in job_products.items():
                    print('➡ src/birds/Birds.py:247 pid:', pid)
                    print('➡ src/birds/Birds.py:247 amount:', amount)
                    if self.__stock.get_stock_by_product_id(pid) < amount:
                        if buy_from_shop:
                            self.__shop.buy(product_name=pid, amount=amount)
                        else:
                            return #TODO: log error

                job_rewards = job_data.get("rewards", 0)#TODO: for future, maybe calc best combination...?!
                print('➡ src/birds/Birds.py:238 job_rewards:', job_rewards)

                possible_jobs.update({job: job_rewards.get("xp", 0)})
            print('➡ src/birds/Birds.py:264 possible_jobs:', possible_jobs)
            if possible_jobs:
                best_job = max(possible_jobs, key=possible_jobs.get)
            else:
                print(f"\n\n ### NO JOB for house {house} available ###")
                continue
            print('\n➡ src/birds/Birds.py:265 best_job:', best_job)
            print("\n\n\n ### START JOB ###")
            content = self.__http.start_job(jobslot=best_job, house_nr=house)
            self.__set_data(content)

        for job in impossible_jobs:
            print(f"\n\n\n ### REMOVE JOB {job} ###")
            content = self.__http.remove_job(slot=job)
            self.__set_data(content)