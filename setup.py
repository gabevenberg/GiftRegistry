#! /usr/bin/env python3

import argparse, json, logging
from pathlib import Path

#logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)

def parse_arguments():
    UIchoices={'GUI'}
    parser=argparse.ArgumentParser(description='launches the GiftRegistry application')
    parser.add_argument('configFile', type=Path, help='location of the JSON configuration file.', default='~/.config/GiftRegistry/config.json')
    parser.add_argument('UImode', help=f'Mode to run the app in. Valid choices are: {UIchoices}', default='GUI')
    args=parser.parse_args()
    
    if args.UImode not in UIchoices:
        raise ValueError(f'UImode must be in {UIchoices}')
    else:

        logging.debug(f'{args.configFile.resolve()=}')
        logging.debug(f'{args.UImode=}')
        return args.configFile.resolve(), args.UImode

def read_config(configFile):
    with open(configFile, 'r') as jsonFile:
        config = json.load(jsonFile)
        logging.debug(f'{config=}')
        return config

if __name__ == '__main__':
    import WeddingRegistryGUI, databaseInteraction
    configFile, UImode=parse_arguments()
    #I know global variables are discoraged, but these are the only two we will be using. (besides, these were technically already global, I just made it explicit.)
    config=read_config(configFile)
    connection=databaseInteraction.connect(
        config['dbHost'],
        config['dbName'],
        config['dbUser'],
        config['dbPass'],
        config['dbPort']
    )
    try:
        #rest of the program goes here.
        #if UImode=='GUI':
        #    WeddingRegistryGUI.send_login_page()
        with connection.cursor() as cur:
            cur.execute('select * from users;')
            print(cur.fetchall())
    finally:
        #this makes sure that the db connection is properly closed.
        connection.close()
