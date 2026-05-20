#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.minigames.bingo.Http import Http
from datetime import date

class Bingo:
    def __init__(self):
        self.__http = Http()
        self.__content = None

    def is_available(self, page_content: str) -> bool:
        if not self.__check_time_span():
            return False
        return True
        # if 'id="calendar" class="birthday long"' not in page_content:
        #     return False

    def play(self) -> bool:
        self.__content = self.__http.init_game()
        if self.__content is None:
            return False
        if self.__content.get("data", {}).get("data", {}).get("freespin_remain", 99999) <= 0:
            self.__content = self.__http.collect_spin()
        spins = self.__content.get("data", {}).get("data", {}).get("spins", 0)
        print('➡ src/minigames/bingo/Bingo.py:26 spins:', spins)
        #TODO: free joker, color joker
        # for spin in range(0, spins):
        #     self.__http.play_bingo()
        #     print(f"spin: {spin}")
        return True
    
    def __check_time_span(self) -> bool:
        today = date.today()
        start_date = date(today.year, 5, 19)
        end_date = date(today.year, 5, 26)
        return start_date <= today <= end_date