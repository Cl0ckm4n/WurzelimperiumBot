#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 21.03.2017

@author: RuffKez
'''

import logging
import os
import time

#vars
logtime = time.strftime("%d-%m-%y-%H.%M.%S")

if not os.path.exists('logs'):
    os.makedirs('logs')

def logger():
    logging.basicConfig(handlers=[logging.FileHandler("wurzelbot.log", 'a', 'utf-8')], level=logging.DEBUG, format='%(asctime)s - %(message)s')