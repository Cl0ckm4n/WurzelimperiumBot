#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import i18n
import src.Logger as logger
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
        logger.logger()

    # Init connection
    wurzelBot = WurzelBot()
    succ = wurzelBot.login(args.server, args.user, args.password, args.lang, args.portalacc)
    if not succ:
        exit(-1)

    try:
        wurzelBot.check_ivyhouse()

    # Close connection
    finally:
        wurzelBot.logout()

if __name__ == "__main__":
    main()
