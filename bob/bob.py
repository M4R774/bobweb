# -*- coding: utf-8 -*-

from bob import message_handler
from bob import data_handler

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

# TODO rankit ja ilmoitukset ylennyksist�
# TODO ei kahta kertaa pisteite pelaajille
# TODO tarkasta ett� pistemäärä ei ole > rankkien määrä
# TODO Prestiget

latest_leet_day = int(datetime.datetime.now().strftime("%Y%m%d")) - 1



bot = telepot.Bot('botin id tähän')
bot.notifyOnMessage(handle)
print("Waiting for input...")

while True:
    time.sleep(10)
