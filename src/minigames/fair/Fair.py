#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import time
from src.minigames.fair.Http import Http

REWARD_MAX = 300

class Fair:
    def __init__(self):
        self._httpConn = Http()
        self._logFair = logging.getLogger('bot.Fair')
        self._logFair.setLevel(logging.DEBUG)
        data = self._httpConn.fair_init()
        self.__set_data(data)
        self.__thimblerig = Thimblerig(data)
        self.__wetgnome = Wetgnome(data)

    def __set_data(self, data):
        self.__data = data["data"]
        self.__remain = self.__data['remain']
        self.__points = self.__data['data']['points']
        self.__tickets = self.__data['data']['tickets']
        self.__ticketcost = self.__data['config']['ticketcost']
        self.__thimblerig_round = self.__data['thimblerig']['data']['round']
        self.__thimblerig_points = self.__data['thimblerig']['data']['points']
        self.__thimblerig_maxrounds = self.__data['thimblerig']['config']['maxrounds']
        self.__wetgnome_round = self.__data['wetgnome']['data']['round']
        self.__wetgnome_points = self.__data['wetgnome']['data']['points']
        self.__wetgnome_maxrounds = self.__data['wetgnome']['config']['maxrounds']

    def craft_tickets(self) -> None:
        msg = f"{self.__points} points available. A ticket costs {self.__ticketcost} points."
        if self.__points >= self.__ticketcost:
            data = self._httpConn.fair_craft_ticket()
            self.__set_data(data)
            msg = f"Crafted {int(self.__points/self.__ticketcost)} tickets."
        msg += f"\nYou have {self.__tickets}x tickets in stock."
        self._logFair.info(msg)

    def __pay_ticket_thimblerig(self):
        if self.__thimblerig_round == 0:
            content = self._httpConn.fair_pay_ticket("thimblerig")
            self.__set_data(content)

    def __pay_ticket_wetgnome(self):
        if self.__wetgnome_round == 0:
            content = self._httpConn.fair_pay_ticket("wetgnome")
            self.__set_data(content)

    def play_thimblerig(self):
        self._logFair.info(f"Thimblerig: {self.__thimblerig.get_points()}/300 balloons.")
        while self.__tickets > 0:
            if not self.__data["thimblerig"]["data"].get("wait", 0):
                self.__pay_ticket_thimblerig()
            if not self.__thimblerig_points < REWARD_MAX:
                self._logFair.info("Thimblerig already finished!")
                break
            while 1 <= self.__thimblerig_round <= self.__thimblerig_maxrounds:
                if not self.__data["thimblerig"]["data"].get("wait", 0):
                    self.__thimblerig_round = self.__thimblerig.game_start(self.__thimblerig_round)
                time.sleep(2) # wait for animation
                self.__thimblerig_round = self.__thimblerig.game_select()
            self._logFair.info(f"Thimblerig: {self.__thimblerig.get_points()}/300 balloons.")
        else:
            self._logFair.error("No tickets for playing!")

    def play_wetgnome(self):
        self._logFair.info(f"Reached: {self.__wetgnome.get_points()}/300 airsnakes.")
        while self.__tickets > 0:
            if not self.__data["wetgnome"]["data"].get("wait", 0):
                self.__pay_ticket_wetgnome()
            if not self.__wetgnome_points < REWARD_MAX:
                self._logFair.info("Wetgnome already finished!")
                break
            while 1 <= self.__wetgnome_round <= self.__wetgnome_maxrounds:
                if not self.__data["wetgnome"]["data"].get("wait", 0):
                    self.__wetgnome_round, game_id = self.__wetgnome.game_start(self.__wetgnome_round)
                time.sleep(2) # wait for animation
                self.__wetgnome_round = self.__wetgnome.game_select(game_id)
            self._logFair.info(f"Reached: {self.__wetgnome.get_points()}/300 airsnakes.")
        else:
            self._logFair.error("No tickets for playing!")

class Thimblerig():
    def __init__(self, data):
        self._httpConn = Http()
        self.round = 0
        self.mug = 0
        self.__set_data(data["data"]["thimblerig"])
        
    def __set_data(self, data):
        self.__data = data
        self.__points = self.__data['data']['points']
        self.round = self.__data['data']['round']
        if "game" in data["data"]:
            self.mug = self.__data["data"]["game"]["mug"]

    def game_start(self, round):
        if 1 <= round <= 3:
            content = self._httpConn.fair_thimblerig_start()
            self.__set_data(content["data"])
        return self.round

    def game_select(self):
        if 1 <= self.mug <= 3:
            content = self._httpConn.fair_thimblerig_select(self.mug)
            self.__set_data(content["data"])
        return self.round
    
    def get_points(self):
        return self.__points
        
class Wetgnome():
    def __init__(self, data):
        self._httpConn = Http()
        self.round = 0
        self.game = 0
        self.__set_data(data["data"]["wetgnome"])
        
    def __set_data(self, data):
        self.__data = data
        self.__points = self.__data['data']['points']
        self.round = self.__data['data']['round']
        if "game" in data["data"]:
            self.game = self.__data["data"]["game"]

    def game_start(self, round):
        if 1 <= round <= 3:
            content = self._httpConn.fair_wetgnome_start()
            self.__set_data(content["data"])
        return self.round, self.game

    def game_select(self, game_id):
        x = 48 + random.randint(25, 75) # middle=51 --> full range von 0-102
        x = x + int(game_id[0])

        y = 49 + random.randint(25, 75) # middle=51 --> full range von 0-102
        y = y + int(game_id[0])

        content = self._httpConn.fair_wetgnome_select(x, y)
        self.__set_data(content["data"])
        return self.round
    
    def get_points(self):
        return self.__points