from src.bonus.Http import Http
from src.note.Note import Note
import time, logging

class Bonus:
    def __init__(self):
        self.__http = Http()
        self.__note = Note()
        self.__log = logging.getLogger("bot.Bonus")
        self.__log.setLevel(logging.DEBUG)

    def get_daily_login_bonus(self):
        bonus_data = self.__http.read_user_data()
        for day, bonus in bonus_data['data']['rewards'].items():
            if 'done' in bonus:
                continue

            if any(_ in bonus for _ in ('money', 'products')):
                self.__http.get_daily_login_bonus(day)
                time.sleep(3) #TODO: why?

            if 'plant' in bonus:
                plant_id = self.__note.get_bonus_plant_id()
                if plant_id and plant_id in bonus_data['products']:
                    self.__http.set_daily_login_bonus_plant(plant_id)
                    self.__log.info(f"Set daily login bonus plant to ID: {plant_id}")
                else:
                    self.__log.error(f"Plant-ID '{plant_id}' not selectable for bonus plant!")
                time.sleep(3) #TODO: why?

    def collect_bonus_item_points(self):
        self.__http.init_garden_shed()
        self.__http.open_trophy_case()
        content = self.__http.collect_bonus_items()
        claim_msg = content['msg'].replace('<br>', '')
        already_claimed_msg = content['message']
        self.__log.info(f"{claim_msg}{already_claimed_msg}")

    def collect_lucky_mole(self):
        content = self.__http.init_guild()
        guild_id = content['data']['id']
        lucky = content['data']['lucky']
        msg = "Lucky mole not available! Try next day."

        if lucky == 1:
            content = self.__http.collect_lucky_mole(guild_id)
            msg = content['message']

        self.__log.info(f"{msg}")

