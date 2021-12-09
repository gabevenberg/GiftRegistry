#! /usr/bin/env python3

import argparse, json, logging
from pathlib import Path
from pprint import pprint

#logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)

def parse_arguments():
    parser=argparse.ArgumentParser(description='launches the GiftRegistry application')
    parser.add_argument('configFile', type=Path, help='location of the JSON configuration file.', default='~/.config/GiftRegistry/config.json')
    args=parser.parse_args()

    logging.debug(f'{args.configFile.resolve()=}')
    return args.configFile.resolve()

def read_config(configFile):
    with open(configFile, 'r') as jsonFile:
        config = json.load(jsonFile)
        logging.debug(f'{config=}')
        return config

if __name__ == '__main__':
    import WeddingRegistryGUI
    from databaseInteraction import appDatabase
    configFile=parse_arguments()
    #I know global variables are discoraged, but these are the only two we will be using. (besides, these were technically already global, I just made it explicit.)
    config=read_config(configFile)
    DB=appDatabase(
        config['dbHost'],
        config['dbName'],
        config['dbUser'],
        config['dbPass'],
        config['dbPort']
    )
    try:
        #rest of the program goes here.
        #if config.uiMode=='GUI':
        #    WeddingRegistryGUI.send_login_page()
        DB.populateWithTestData()
        pprint(DB.getUnpurchasedGifts())
        DB.purchaseItem(2, 3, 1)
        pprint(DB.getUnpurchasedGifts())
    finally:
        #this makes sure that the db connection is properly closed.
        DB.close()
