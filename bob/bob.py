# -*- coding: utf-8 -*-
import locale
import os
import sys
import unicodedata
import sys
import time
import telepot
import datetime
import codecs
import random
import json
import message_handler

# TODO kaikilla ei ole nimia telegramissa
# TODO kerro uusi pistemaara aina kun kayttajan pistemaara muuttuu
# TODO rankit ja ilmoitukset ylennyksist�
# TODO ei kahta kertaa pisteite pelaajille
# TODO tarkasta ett� pistemäärä ei ole > rankkien määrä
# TODO Prestiget

latest_leet_day = int(datetime.datetime.now().strftime("%Y%m%d")) - 1


# Reads the ranks.txt and returns it contents as a list
def read_ranks_file():
    ranks = []
    file = open('ranks.txt')
    for line in file:
        # strip removes all whitsespaces from end and beginning
        line = line.strip()
        ranks.append(line)
    file.close()
    return ranks


# Reads bob-data.json file and returns its contents
def read_data_file():
    try:
        with open("bob-data.json", mode="r") as data_file:
            json_string = data_file.read()
            leet_data = json.loads(json_string)
            return leet_data
    except:
        pass


# dumps the data to .json file
def write_file(data):
    try:
        with open("bob-data.json", mode="w") as data_file:
            json_string = json.dumps(data)
            data_file.write(json_string)
        pass
    except:
        pass


bot = telepot.Bot('botin id tähän')
bot.notifyOnMessage(handle)
print("Waiting for input...")

while True:
    time.sleep(10)
