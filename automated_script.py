#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import src.Main as main
import time

parser = argparse.ArgumentParser()
parser.add_argument('server', type=int, help='server number')
parser.add_argument('user', type=str, help='username for login')
parser.add_argument('password', type=str, help='password for login', default=False)
args = parser.parse_args()

wurzelBot = main.initWurzelBot()
wurzelBot.launchBot(args.server, args.user, args.password)

wurzelBot.harvestAllGarden()

lowest = wurzelBot.getLowestStockEntry()
if lowest != 'Your stock is empty':
    wurzelBot.growPlantsInGardens(lowest)

time.sleep(3)
wurzelBot.waterPlantsInAllGardens()

#Deinitialisierung des Bots
wurzelBot.exitBot()



