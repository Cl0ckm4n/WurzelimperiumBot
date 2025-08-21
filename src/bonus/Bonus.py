#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.bonus.Http import Http
from src.guild.Http import Http as HttpGuild
from src.logger.Logger import Logger
from src.note.Note import Note
import time

class Bonus:
    def __init__(self):
        self.__http = Http()
        self.__httpGuild = HttpGuild()
        self.__note = Note()

    def get_daily_login_bonus(self):
        bonus_data = self.__http.read_user_data()
        for day, bonus in bonus_data['data']['rewards'].items():
            if 'done' in bonus:
                continue

            if any(_ in bonus for _ in ('money', 'products')):
                self.__http.get_daily_login_bonus(day)
                time.sleep(3)

            if 'plant' in bonus:
                plant_id = self.__note.get_bonus_plant_id()
                if plant_id and plant_id in bonus_data['products']:
                    self.__http.set_daily_login_bonus_plant(plant_id)
                    Logger().info(f"Set daily login bonus plant to ID: {plant_id}")
                else:
                    Logger().error(f"Plant-ID '{plant_id}' not selectable for bonus plant!")
                time.sleep(3)

    def collect_bonus_item_points(self) -> bool:
        if not self.__http.init_garden_shed():
            return False
        if not self.__http.open_trophy_case():
            return False
        content = self.__http.collect_bonus_items()
        if content is None:
            return False
        claim_msg = content['msg'].replace('<br>', '')
        already_claimed_msg = content['message']
        Logger().print(f"{claim_msg}{already_claimed_msg}")
        return True

    def collect_lucky_mole(self) -> bool:
        content = self.__httpGuild.init_guild()
        if content is None:
            return False
        guild_id = content['data']['id']
        lucky = content['data']['lucky']
        msg = "Lucky mole not available! Try next day."

        if lucky == 1:
            content = self.__httpGuild.collect_lucky_mole(guild_id)
            if content is None:
                return False
            msg = content['message']

        Logger().print(f"{msg}")
        return True

