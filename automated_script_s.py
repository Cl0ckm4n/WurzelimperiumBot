#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import i18n
from src.core.Config import Config
from src.logger.Logger import Logger
from src.megafruit.Megafruit import Mushroom
from src.WurzelBot import WurzelBot

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server', type=int, help='server number')
    parser.add_argument('user', type=str, help='username for login')
    parser.add_argument('password', type=str, help='password for login', default=False)
    parser.add_argument('-p', '--portal', help="If -p or --portal Argument is passed, Portal Account Login will be used.", action='store_true', default=False, required=False, dest="portalacc")
    parser.add_argument('-l', '--log', help="If -l or --log Argument is passed, logging will be enabled.", action='store_true', default=False, required=False, dest="log")
    parser.add_argument('lang', help="Set Language and Region for the Game and Bot", type=str, nargs='?', default=None, const='en')
    args = parser.parse_args()

    i18n.load_path.append('lang')
    i18n.set('locale', args.lang)
    i18n.set('fallback', 'en')

    if args.log:
        Config().log_to_stdout = True

    # Init connection
    # BG- Създаване на връзка
    wurzelBot = WurzelBot()
    succ = wurzelBot.login(args.server, args.user, args.password, args.lang, args.portalacc)
    if not succ:
        exit(-1)

    try:
        wurzelBot.note.get_note_settings()

        # Send bees
        wurzelBot.send_bees(tour=1)
        
        # Remove weed
        print(i18n.t('wimpb.remove_weed_from_all_gardens'))
        wurzelBot.remove_weeds()

        # Harvest
        wurzelBot.harvest()

        # Plant plants
        if wurzelBot.note.get_garden_plant_1():
            wurzelBot.growVegetablesInGardens(wurzelBot.note.get_garden_plant_1())
        if wurzelBot.note.get_garden_plant_2():
            wurzelBot.growVegetablesInGardens(wurzelBot.note.get_garden_plant_2())
        if wurzelBot.note.get_watergarden_plant_1():
            wurzelBot.growPlantsInAquaGardens(wurzelBot.note.get_watergarden_plant_1())
        if wurzelBot.note.get_watergarden_plant_2():
            wurzelBot.growPlantsInAquaGardens(wurzelBot.note.get_watergarden_plant_2())
        if wurzelBot.note.get_watergarden_plant_edge():
            wurzelBot.growPlantsInAquaGardens(wurzelBot.note.get_watergarden_plant_edge())

        # Water plants
        time.sleep(3)
        print(i18n.t('wimpb.watering_all_plants'))
        wurzelBot.water()

        # Claim Daily
        print(i18n.t('wimpb.claim_bonus'))
        wurzelBot.get_daily_bonuses()

        # Play minigames
        Logger().print('')
        Logger().print('Playing minigames...')
        wurzelBot.minigames.play(allowed_events = ['advent_calendar', 'birthday_calendar', 'summer_calendar', 'fair', 'pumpkin_digging'])

        # Check Herbgarden
        if wurzelBot.note.get_herbgarden_active():
            wurzelBot.check_herb_garden()

        # Taking care of megafruit
        if wurzelBot.megafruit is not None:
            wurzelBot.check_megafruit(mushroom=Mushroom.CHANTERELLE, buy_from_shop=True, allowed_care_item_prices = ['money'])

        wurzelBot.check_park()

        # Cut bonsais
        if wurzelBot.bonsaifarm is not None:
            Logger().print('\nCutting bonsais...')
            wurzelBot.cut_and_renew_bonsais(allowed_prices=['money'])

    finally:
        # Close connection
        # BG-Затваряне на връзката
        wurzelBot.logout()

if __name__ == "__main__":
    main()
