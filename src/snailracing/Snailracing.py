#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import os, json

from src.core.User import User
from src.shop.Shop import Shop
from src.snailracing.Http import Http
from src.stock.Stock import Stock

RACE_DURATION = 172800 #seconds; 48h
RACE_TERRAIN_ADVANTAGE = 0.2
RACE_TERRAIN_DISADVANTAGE = 0.2
RACE_EQUIPMENT = 0.1


SADDLE_1 = ["grass", "dirt"]
SADDLE_3 = ["gravel", "asphalt"]
BRIDLE_1 = ["sand", "forest"]
BRIDLE_3 = ["dirt", "mud"]

JOCKEY1 = "jockey1" #wT
JOCKEY2 = "jockey2" #Coins

class Snail:
    def __init__(self, data, slot = 0, type = 0): # type: for theoretical calculation
        # print('➡ src/snailracing/Snailracing.py:19 data:', data)
        print('➡ src/snailracing/Snailracing.py:19 type:', type)
        print('➡ src/snailracing/Snailracing.py:19 slot:', slot)
        self.__type = type # 1-6
        self.__name = None
        self.__slot = slot # 1-6
        self.__in_race = False
        self.__energy_max = 0
        self.__loved = []
        self.__hated = []
        self.__speed = 0
        self.__sliminess = 0
        self.__daytime = None
        self.__cooldown_remain = 0
        self.__level = 0
        self.__data = data
        if type:
            self.__set_dummy_data()
        if slot:
            self.__set_snailslot_data()
        self.__set_config_data(self.__type)


    def __set_dummy_data(self):
        self.__level = 10
        self.__in_race = False
        self.__cooldown_remain = 0

    def __set_snailslot_data(self):
        self.__level = self.__data["data"]["snails"][f"{self.__slot}"]["level"]["level"] #.get("data").get("snails").get(self.__slot).get("level").get("level")
        print('➡ src/snailracing/Snailracing.py:57 self.__level:', self.__level)
        self.__type = self.__data.get("data").get("snails").get(f"{self.__slot}").get("type")
        print('➡ src/snailracing/Snailracing.py:59 self.__type:', self.__type)
        self.__in_race = self.__data.get("data").get("snails").get(f"{self.__slot}").get("race")
        self.__cooldown_remain = self.__data.get("data").get("snails").get(f"{self.__slot}").get("cooldown_remain")

    def __set_config_data(self, type):
        self.__name = self.__data.get("config").get("snail").get(f"{type}").get("name")
        print('➡ src/snailracing/Snailracing.py:63 self.__name:', self.__name)
        self.__energy_max = self.__data.get("config").get("snail_attributes").get(f"{type}").get(f"{self.__level}").get("energy")
        print('➡ src/snailracing/Snailracing.py:65 self.__energy_max:', self.__energy_max)
        self.__loved = self.__data.get("config").get("snail").get(f"{type}").get("loved")
        print('➡ src/snailracing/Snailracing.py:67 self.__loved:', self.__loved)
        self.__hated = self.__data.get("config").get("snail").get(f"{type}").get("hated")
        print('➡ src/snailracing/Snailracing.py:69 self.__hated:', self.__hated)
        self.__speed = round(0.72 * self.__data.get("config").get("snail_attributes").get(f"{type}").get(f"{self.__level}").get("speed"), 2)
        print('➡ src/snailracing/Snailracing.py:71 self.__speed:', self.__speed)
        self.__sliminess = self.__data.get("config").get("snail_attributes").get(f"{type}").get(f"{self.__level}").get("sliminess")
        print('➡ src/snailracing/Snailracing.py:73 self.__sliminess:', self.__sliminess)
        self.__daytime = self.__data.get("config").get("snail").get(f"{type}").get("daytime")
        print('➡ src/snailracing/Snailracing.py:75 self.__daytime:', self.__daytime)

    def get_loved(self):
        return self.__loved

    def get_hated(self):
        return self.__hated

    def get_speed(self):
        return self.__speed

    def get_sliminess(self):
        return self.__sliminess
    
    def get_daytime(self):
        return self.__daytime

    def get_slot(self):
        return self.__slot
    
    def get_type(self):
        return self.__type
    
    def get_in_race(self):
        return self.__in_race
    
    def get_cooldown_remain(self):
        return self.__cooldown_remain

class Snailracing:
    """All important information for the snailracing."""

    def __init__(self, json = 0): #TEMP ,json
        if not json:
            self.__http = Http()
            self.__user = User()
            self.__shop = Shop()
            self.__stock = Stock()
        self.__log = logging.getLogger(f'bot.{self.__class__.__name__}')
        self.__log.setLevel(logging.INFO)
        if json:
            self.__data = json["data"]
        else:
            self.__data = None #TEMP: json
        print(self.__data)
        self.__productions_slots_unlocked = []
        self.__race_energy = 0 #TEMP int(self.__data["data"]["data"]["race"]["energy"])
        if not json:
            self.update()

    def update(self):
        self.__set_data(self.__http.get_snailracing_info())
        

    def __set_data(self, j_content):
        self.__data = j_content['data']
        self.__race_energy = int(self.__data["data"]["race"]["energy"])
        print('➡ src/snailracing/Snailracing.py:141 self.__race_energy:', self.__race_energy)
        self.__race_remain = int(self.__data["data"]["race"].get("remain", 999999999))
        print('➡ src/snailracing/Snailracing.py:149 self.__race_remain:', self.__race_remain)

        # BARS
        self.__productions_slots_unlocked = self.__get_production_slots_unlocked()

    def __get_production_slots_unlocked(self) -> list:
        productions_slots_unlocked = []
        slots = self.__data["data"]["productionslots"]
        productions_slots_unlocked.append("1")
        del slots["1"]
        for slot, data in slots.items():
            if not data.get("block", 0) == 1:
                productions_slots_unlocked.append(slot)

        return productions_slots_unlocked

    def __get_production_slots_free(self) -> list:
        slots_occupied = []
        slots_free = []
        productions = self.__data.get("data", 0).get("productions", 0)
        print('➡ src/snailracing/Snailracing.py:145 productions:', productions)
        if productions:
            for slot, data in productions.items():
                slots_occupied.append(slot)
            print('➡ src/snailracing/Snailracing.py:209 slots_occupied:', slots_occupied)
        slots_free = [x for x in self.__productions_slots_unlocked if x not in slots_occupied]
        print('➡ src/snailracing/Snailracing.py:209 slots_free:', slots_free)
            
        return slots_free
    
    def start_bar_production(self, bar_pid=473) -> None:
        slots_free = self.__get_production_slots_free()
        print('➡ src/snailracing/Snailracing.py:205 slots_free:', slots_free)
        for slot in slots_free:
            if self.__check_bar_products_availability(bar_pid):
                data = self.__http.start_bar_production(slot, bar_pid)
                self.__set_data(data)
                self.__stock.update()

    def __check_bar_products_availability(self, bar_pid, buy_from_shop = True):
        bar_products = self.__get_bar_products(bar_pid)
        for pid, amount in bar_products.items():
            if self.__stock.get_stock_by_product_id(pid) < amount:
                if buy_from_shop:
                    self.__shop.buy(product_name=int(pid), amount=amount)
                else:
                    return False
        return True

    def __get_bar_products(self, bar_pid) -> dict:
        return self.__data.get("config", {}).get("products", {}).get(str(bar_pid), {}).get("products", {})

    def collect_bar_production(self) -> None:
        productions = self.__data.get("data", 0).get("productions", 0)
        if not productions: return

        for slot, data in productions.items():
            if data.get("remain", None) <= 0:
                print('➡ src/snailracing/Snailracing.py:216 data.get("remain":', data.get("remain"))
                print(f"\n\nslot {slot} finished")
                data = self.__http.harvest_bar_production(slot)
                self.__set_data(data)

    def calculate_track_segments(self, json) -> list: #WORKS
        track_data = json["data"]["race"]["track"]
        obstacles = track_data["obstacles"]
        obstacles_px = []
        for obstacle in obstacles:
            obstacles_px.append(obstacle.get("px")) 
        self.__log.debug('➡ src/snailracing/Snailracing.py:75 obstacles_px:', obstacles_px)
        del track_data["obstacles"]
        self.__log.debug('➡ src/snailracing/Snailracing.py:67 track:', track_data)

        track_segments = []
        px = 0 # length of calculated segments
        px_segment = 0 # actual segment
        length_check = 0
        # for obstacle in obstacles:

        #     # if obstacle.get("px") in range(1, track_data[])
        #     #     track_segments
        #     # else:
        #     track_segments.append({"start": px+1, "end": px+100000, "length": 100000, "terrain": track_data.get(int(px/100000)), "obstacle": 0})
        #     print('➡ src/snailracing/Snailracing.py:85 track_segments:', track_segments)
        #     px += 100000



        # segment: 1 - 100.000, 100.001 - 200.000, ...
        # obstacle: width_px = 15.000; middle_px = 7.500; length to left = 7.499; length to right = 7.500
        for segment, terrain in track_data.items():
            self.__log.debug("----------------------------------------")
            self.__log.debug(segment)
            self.__log.debug(terrain["terrain"])
            if segment != "30":
                next_terrain = track_data[str(int(segment)+1)]
                self.__log.debug('➡ src/snailracing/Snailracing.py:97 next_terrain:', next_terrain["terrain"])

            if any(px_segment+1 <= obstacle_px <= px_segment+107499 for obstacle_px in obstacles_px): #obstacle in segment --> segment border + 0.5*obstacle_width = x*100.000 + 7.499
                for obstacle_px in obstacles_px: # check for all obstacles
                    if px_segment+1+7499 <= obstacle_px <= px_segment+92500: #obstacle within segment borders 75000 - 92500
                        self.__log.debug("---WITHIN SEGMENT---")
                        # print('➡ src/snailracing/Snailracing.py:98 px+1:', px_segment+1)
                        # print('➡ src/snailracing/Snailracing.py:98 px+92500:', px_segment+92500)
                        self.__log.debug('➡ src/snailracing/Snailracing.py:98 obstacle_px:', obstacle_px)
                        px_before_obstacle = obstacle_px - 7500
                        self.__log.debug('➡ src/snailracing/Snailracing.py:102 px_before_obstacle:', px_before_obstacle)
                        length_before = px_before_obstacle - px # length until start of obstacle
                        self.__log.debug('➡ src/snailracing/Snailracing.py:104 length_before:', length_before)
                        px_after_obstacle = obstacle_px + 7501
                        self.__log.debug('➡ src/snailracing/Snailracing.py:106 px_after_obstacle:', px_after_obstacle)
                        if length_before > 0: # segment area before obstacle starts
                            track_segments.append({"start": px+1, "end": px_before_obstacle, "length": length_before, "terrain": terrain["terrain"], "obstacle": 0})
                            length_check += length_before
                            track_segments.append({"start": px_before_obstacle+1, "end": px_after_obstacle-1, "length": 15000, "terrain": terrain["terrain"], "obstacle": 1})
                            length_check += 15000
                        else: # obstacle overlapping; length_before negative
                            track_segments.append({"start": px+1, "end": px_after_obstacle-1, "length": 15000+length_before+1, "terrain": terrain["terrain"], "obstacle": 1})
                            length_check += 15000+length_before+1
                        px += length_before + 15000
                        self.__log.debug('➡ src/snailracing/Snailracing.py:114 px1:', px)
                    
                    if px_segment + 107500 > obstacle_px > px_segment+92500: #zur nächste Segmentgrenzen
                        self.__log.debug("---SEGMENT BORDER---")
                        px_before_obstacle = obstacle_px - 7500
                        self.__log.debug('➡ src/snailracing/Snailracing.py:102 px_before_obstacle:', px_before_obstacle)
                        obstacle_length_before_segment_border = px_segment + 100000 - px_before_obstacle
                        self.__log.debug('➡ src/snailracing/Snailracing.py:123 obstacle_px_before_segment_border:', obstacle_length_before_segment_border)
                        length_before = px_before_obstacle - px
                        px_after_obstacle = obstacle_px + 7501
                        self.__log.debug('➡ src/snailracing/Snailracing.py:106 px_after_obstacle:', px_after_obstacle)
                        obstacle_length_after_segment_border = 15000 - obstacle_length_before_segment_border
                        self.__log.debug('➡ src/snailracing/Snailracing.py:125 obstacle_length_after_segment_border:', obstacle_length_after_segment_border)
                        
                        # print('➡ src/snailracing/Snailracing.py:98 px+92500:', px_segment+92500)
                        self.__log.debug('➡ src/snailracing/Snailracing.py:98 obstacle_px:', obstacle_px)
                        ###
                        track_segments.append({"start": px+1, "end": px_before_obstacle, "length": length_before, "terrain": terrain["terrain"], "obstacle": 0})
                        length_check += length_before
                        track_segments.append({"start": px_before_obstacle + 1, "end": px_before_obstacle + 1 + obstacle_length_before_segment_border - 1, "length": obstacle_length_before_segment_border, "terrain": terrain["terrain"], "obstacle": 1})
                        length_check += obstacle_length_before_segment_border
                        track_segments.append({"start": px_segment + 100000 + 1, "end": px_after_obstacle - 1, "length": obstacle_length_after_segment_border, "terrain": next_terrain["terrain"], "obstacle": 1})
                        length_check += obstacle_length_after_segment_border

                        px += obstacle_length_before_segment_border + length_before + obstacle_length_after_segment_border
                        length_before + 15000 + 1
                        self.__log.debug('➡ src/snailracing/Snailracing.py:114 px2:', px)

                if px < px_segment + 100000: # rest of segment without obstacles
                    self.__log.debug("---REST OF SEGMENT---")
                    length = px_segment + 100000 - px
                    self.__log.debug('➡ src/snailracing/Snailracing.py:118 length:', length)
                    track_segments.append({"start": px+1, "end": px_segment+100000, "length": length, "terrain": terrain["terrain"], "obstacle": 0})
                    length_check += length
                    px += length
                    self.__log.debug('➡ src/snailracing/Snailracing.py:152 px3:', px)
            else: # no obstacle within segment
                self.__log.debug("---NO OBSTACLE---")
                length = px_segment + 100000 - px
                self.__log.debug('➡ src/snailracing/Snailracing.py:118 length:', length)
                track_segments.append({"start": px+1, "end": px_segment+100000, "length": length, "terrain": terrain["terrain"], "obstacle": 0})
                length_check += length
                px += length
                self.__log.debug('➡ src/snailracing/Snailracing.py:121 px4:', px)

            # track_segments.append({"start": px+1, "end": px+100000, "length": 100000, "terrain": track_data.get(int(px/100000)), "obstacle": 0})
            self.__log.debug("---SEGMENT SUMMARY---")
            px_segment += 100000
            self.__log.debug('➡ src/snailracing/Snailracing.py:121 px_segment:', px_segment)
            self.__log.debug('➡ src/snailracing/Snailracing.py:112 px:', px)
            self.__log.debug('➡ src/snailracing/Snailracing.py:85 track_segments:', track_segments)
            self.__log.debug('➡ src/snailracing/Snailracing.py:167 length_check:', length_check)
            # if px_segment > 499999: # end execution earlier
            #     break
        return track_segments

    def calculate_race_distance(self, track_segments, snail: Snail, saddle, bridle): # TODO:
        snail_speed = snail.get_speed()
        print('➡ src/snailracing/Snailracing.py:284 snail_speed:', snail_speed)
        self.__log.debug('➡ src/snailracing/Snailracing.py:255 snail_speed:', snail_speed)
        sliminess = snail.get_sliminess()
        print('➡ src/snailracing/Snailracing.py:257 sliminess:', sliminess)
        race_distance = 0.0
        race_time = 0

        # EQUIPMENT
        day_night_bonus = 1.1 #1 + 0.1(helmet)
        # self.__log.debug('➡ src/snailracing/Snailracing.py:255 self.__data["race"]["daytime"]:', self.__data["data"]["data"]["race"]["daytime"])
        # self.__log.debug('➡ src/snailracing/Snailracing.py:255 snail.get_daytime():', snail.get_daytime())
        if snail.get_daytime() == self.__data["data"]["race"]["daytime"]:
            day_night_bonus += 0.1
        else:
            day_night_bonus = day_night_bonus - 0.1
        self.__log.info('➡ src/snailracing/Snailracing.py:258 day_night_bonus:', day_night_bonus)

        # self.__log.debug('➡ src/snailracing/Snailracing.py:66 duration:', RACE_DURATION)
        # self.__log.debug('➡ src/snailracing/Snailracing.py:105 race_distance:', race_distance)
        for segment in track_segments:
            self.__log.debug("----------------------------------------")
            self.__log.debug(segment)
            terrain = segment.get("terrain")
            self.__log.debug(terrain)

            terrain_speed = self.__calculate_terrain_speed(terrain, snail, saddle, bridle)
            print(race_distance)
            
            race_speed = snail_speed * terrain_speed * day_night_bonus #m/h
            print('➡ src/snailracing/Snailracing.py:314 snail_speed:', snail_speed)
            print('➡ src/snailracing/Snailracing.py:314 terrain_speed:', terrain_speed)
            print('➡ src/snailracing/Snailracing.py:314 day_night_bonus:', day_night_bonus)
            print('➡ src/snailracing/Snailracing.py:314 race_speed:', race_speed)
            
            # print('➡ src/snailracing/Snailracing.py:279 race_speed_1:', race_speed)
            if segment.get("obstacle"):
                race_speed = race_speed * (sliminess/10)
                # print('➡ src/snailracing/Snailracing.py:286 sliminess:', sliminess)
                # print('➡ src/snailracing/Snailracing.py:105 race_speed_2:', race_speed)
            
                print('➡ src/snailracing/Snailracing.py:312 race_speed OBSTACLE:', race_speed)
            # ----- 20m == 100.000px
            race_time_segment = ((segment.get("length")/100000*20) / race_speed) * 3600
            # self.__log.debug('➡ src/snailracing/Snailracing.py:212 race_time_segment:', race_time_segment)
            if not race_time_segment <= RACE_DURATION - race_time:
                race_time_remaining = RACE_DURATION - race_time
                # self.__log.debug('➡ src/snailracing/Snailracing.py:215 race_time_remaining:', race_time_remaining)
                race_time_remaining_h = race_time_remaining/60/60
                # self.__log.debug('➡ src/snailracing/Snailracing.py:217 race_time_remaining_h:', race_time_remaining_h)
                self.__log.debug(race_time_remaining_h+race_time_h)

                race_distance += race_time_remaining * (race_speed / 3600)
                # self.__log.debug('➡ src/snailracing/Snailracing.py:221 race_distance:', race_distance)

                break
            
            race_time += race_time_segment
            print('➡ src/snailracing/Snailracing.py:340 race_time:', race_time/3600)
            
            # self.__log.debug('➡ src/snailracing/Snailracing.py:215 race_time:', race_time)
            race_time_min = race_time / 60
            # self.__log.debug('➡ src/snailracing/Snailracing.py:217 race_time_min:', race_time_min)
            race_time_h = race_time_min / 60
            # self.__log.debug('➡ src/snailracing/Snailracing.py:219 race_time_h:', race_time_h)

            race_distance += race_time_segment * (race_speed / 3600)
            # self.__log.debug('➡ src/snailracing/Snailracing.py:228 race_distance:', race_distance)
        return race_distance

    def __calculate_terrain_speed(self, terrain, snail: Snail, saddle, bridle):
        snail_loved = snail.get_loved()
        print('➡ src/snailracing/Snailracing.py:355 snail_loved:', snail_loved)
        snail_hated = snail.get_hated()
        print('➡ src/snailracing/Snailracing.py:357 snail_hated:', snail_hated)
        print('➡ src/snailracing/Snailracing.py:360 terrain:', terrain)
        terrain_speed = 1
        if terrain in snail_loved:
            terrain_speed += RACE_TERRAIN_ADVANTAGE
            print('➡ src/snailracing/Snailracing.py:362 terrain_speed:', terrain_speed)
        if terrain in snail_hated:
            terrain_speed -= RACE_TERRAIN_DISADVANTAGE
            print('➡ src/snailracing/Snailracing.py:365 terrain_speed:', terrain_speed)
        if terrain in saddle:
            terrain_speed += RACE_EQUIPMENT
            print('➡ src/snailracing/Snailracing.py:368 terrain_speed:', terrain_speed)
        if terrain in bridle:
            terrain_speed += RACE_EQUIPMENT
            print('➡ src/snailracing/Snailracing.py:371 terrain_speed:', terrain_speed)

        return terrain_speed
        
    def calculate_optimal_snail(self):
        track_segments = self.calculate_track_segments(self.__data)
        
        snails = []
        for slot in range(1,5): # slots 1-4
            # if available: #snail available
            snail = Snail(self.__data, slot)
            in_race = snail.get_in_race()
            print('➡ src/snailracing/Snailracing.py:354 in_race:', in_race)
            cooldown = snail.get_cooldown_remain()
            print('➡ src/snailracing/Snailracing.py:359 cooldown:', cooldown)
            print('➡ src/snailracing/Snailracing.py:359 cooldown:', type(cooldown))
            if not (int(in_race) or cooldown > 0):
                snails.append(snail)

        snails_max = []
        for slot in range(1,7): # theoretical snail 1-6 Lvl.10
            snails_max.append(Snail(self.__data, type=slot))

        snail_distance = {}
        snail: Snail
        for snail in snails:
            slot = snail.get_slot()
            temp_distance = {}
            temp_distance.update({11: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_1, bridle=BRIDLE_1)})
            temp_distance.update({13: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_1, bridle=BRIDLE_3)})
            temp_distance.update({31: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_3, bridle=BRIDLE_1)})
            temp_distance.update({33: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_3, bridle=BRIDLE_3)})
            # print('➡ src/snailracing/Snailracing.py:333 temp_distance:', temp_distance)
            
            best = [key for key in temp_distance if temp_distance[key] == max(temp_distance.values())]
            snail_distance.update({max(temp_distance.values()): {"best": best[-1], "slot": slot}})
            
            # for snail, item in temp_distance.items():
            #     print('➡ src/snailracing/Snailracing.py:356 item:', item)
            #     print('➡ src/snailracing/Snailracing.py:356 snail:', snail)
            #     if temp_distance[snail.get("distance")] == max(temp_distance.values().get("distance")):
            #         snail_distance.update(
            #         {"snail": [key for key in temp_distance if temp_distance[key] == max(temp_distance.values())], "distance": max(temp_distance.values())}
            #         )
        # print('➡ src/snailracing/Snailracing.py:352 snail_distance:', snail_distance)
        snail_distance_max = {}
        for snail in snails_max:
            slot = snail.get_type()
            temp_distance = {}
            temp_distance.update({11: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_1, bridle=BRIDLE_1)})
            temp_distance.update({13: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_1, bridle=BRIDLE_3)})
            temp_distance.update({31: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_3, bridle=BRIDLE_1)})
            temp_distance.update({33: self.calculate_race_distance(track_segments, snail, saddle=SADDLE_3, bridle=BRIDLE_3)})
            # print('➡ src/snailracing/Snailracing.py:333 temp_distance:', temp_distance)
            best = [key for key in temp_distance if temp_distance[key] == max(temp_distance.values())]
            snail_distance_max.update({max(temp_distance.values()): {"best": best[-1], "slot": slot}})
        
        # print('➡ src/snailracing/Snailracing.py:335 snail_distance_max:', snail_distance_max)
        print('➡ src/snailracing/Snailracing.py:433 snail_distance_max:', snail_distance_max)
        print('➡ src/snailracing/Snailracing.py:433 snail_distance:', snail_distance)
        return snail_distance #list with best snail(s)

    def setup_optimal_snail(self, snail_distances: dict): #TODO: fertig, adapt for HTTP-use
        print("-----------------------")
        print('➡ src/snailracing/Snailracing.py:384 snail_distances:', snail_distances)
        print("-------------")

        max_distance= max(snail_distances.keys())
        slot = snail_distances.get(max_distance).get("slot")
        print('➡ src/snailracing/Snailracing.py:391 slot:', slot)

        best_items = snail_distances.get(max_distance).get("best")
        print('➡ src/snailracing/Snailracing.py:394 best_items:', best_items)
        best_saddle = str(best_items)[0]
        best_headgear = str(best_items)[1]
        print('➡ src/snailracing/Snailracing.py:395 best_headgear:', best_headgear)
        print('➡ src/snailracing/Snailracing.py:395 best_saddle:', best_saddle)
        best_snail = Snail(self.__data, slot)
        # test if available, else remove
        #TODO:
        jockey = f"jockey{1}"

        saddle = f"saddle{best_saddle}"
        print('➡ src/snailracing/Snailracing.py:405 saddle:', saddle)

        makeup = "makeup1" #Wimpel

        if self.__data["data"]["race"]["daytime"] == "day":
            helmet = f"helmet1" #day-night
        if self.__data["data"]["race"]["daytime"] == "night":
            helmet = f"helmet3"
        print('➡ src/snailracing/Snailracing.py:432 helmet:', helmet)

        headgear = f"headgear{best_headgear}" #Zaumzeug
        print('➡ src/snailracing/Snailracing.py:411 headgear:', headgear)

        """setup={"slot":"1","jockey":"jockey1","saddle":"saddle1","makeup":"makeup1","helmet":"helmet1","headgear":"headgear3"}"""
        setup = f'"slot":"{slot}","jockey":"{jockey}","saddle":"{saddle}","makeup":"{makeup}","helmet":"{helmet}","headgear":"{headgear}"'
        print('➡ src/snailracing/Http.py:43 setup:', setup)

        return setup




        ## print all snail slots
        # for slot, items in snail_distances.items():
            
        #     print('➡ src/snailracing/Snailracing.py:386 items:', items)
        #     print('➡ src/snailracing/Snailracing.py:386 slot:', slot)
        #     print(max(items.values()))

    def check_race_feeding(self, pid=473, amount=1):
        print('➡ src/snailracing/Snailracing.py:434 self.__race_energy:', self.__race_energy)
        if self.__race_energy < 150000 and self.__race_remain >= 10000: 
            print("FEEEEEEEEEEEEEEEEEEEEEEED")
            content = self.__http.feed_snail(pid, amount) # feed snail with energy bar
            self.__set_data(content)

    def check_race_start(self):
        if self.__race_remain == 999999999:
            print("STAAAAART")
            dis = self.calculate_optimal_snail()
            setup = self.setup_optimal_snail(dis)
            content = self.__http.start_race(setup)
            self.__set_data(content)

    def check_race_finish(self):
        if self.__race_remain < 0:
            print("FIIIIINISH!")
            content = self.__http.finish_race()
            self.__set_data(content)
            reward = self.__data.get("reward", "not found")
            print('➡ src/snailracing/Snailracing.py:477 reward:', reward)
