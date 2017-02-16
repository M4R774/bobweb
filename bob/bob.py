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

# TODO kaikilla ei ole nimia telegramissa
# TODO kerro uusi pistemaara aina kun kayttajan pistemaara muuttuu
# TODO rankit ja ilmoitukset ylennyksist�
# TODO ei kahta kertaa pisteite pelaajille
# TODO tarkasta ett� pistem��r� ei ole > rankkien m��r�
# TODO Prestiget


# tsatti_lista tallennetaan tiedostoon aina tapahtuman [TODO] tapahtuessa
# esimerkki .txt tiedoston rakenteesta:
#
#	"chat_id1"
#	"userid1" "user1score"
#	"userid2" "user2score"
#	[tyhja rivi]
#	"chat_id2"
#	"userid1"|"user1score"
#	"userid2"|"user2score"

# filename where the user data is stored
datafileName = "bob-data.json"

# Dict where all info about users is saved before writing to .json file
userData = {}

# Ranks read from ranks.txt
ranks = []


latestLeetDay = int(datetime.datetime.now().strftime("%Y%m%d")) - 1


# Reads the ranks.txt and returns it contents as a list
def read_ranks_file():
    file = open('ranks.txt')

    for line in file:
        # strip removes all whitsespaces from end and beginning
        line = line.strip()
        ranks.append(line)
    file.close()
    return ranks


# Reads bob-data.json file and returns its contents
def read_data_file():
    pass


# dumps the data to .json file
def write_file(data):
    pass


def handle(msg):
    chat_id = str(msg['chat']['id'])
    # tsatti_lista = readFile()
    chat_title = "null"

    if int(chat_id) < 0:
        chat_title = msg['chat']['title']
    command = msg['text']
    ranks = readRanksFile()
    global latestLeetDay

    if chat_id in userData:
        pass
    else:
        userData[chat_id] = {}

    try:
        userid = msg['from']["first_name"] + str(" ") + msg['from']["last_name"]
    except:
        try:
            userid = msg['from']['username']
        except:
            userid = msg['from']['id']

    print('Got command: %s from %s' % (command, userid))

    if command == '1337' or command == '/1337':
        now = datetime.datetime.now()
        if (int(now.strftime('%H')) + 2 == 13 and int(now.strftime('%M')) == 37):  # or userid == 'developer':
            if latestLeetDay != int(datetime.datetime.now().strftime("%Y%m%d")):
                readFile()
                if userid in str(userData[chat_id]):
                    userData[chat_id][userid] = int(userData[chat_id][userid]) + 1
                else:
                    userData[chat_id][userid] = 1

                message = str('Elite! %s has been promoted to %s' % (userid, ranks[int(userData[chat_id][userid])]))
                bot.sendMessage(chat_id, message)
                writeFile(userData)
                latestLeetDay = int(datetime.datetime.now().strftime("%Y%m%d"))
            else:
                bot.sendMessage(chat_id, ("%s was too slow :(" % userid))

        else:
            bot.sendMessage(chat_id, "But it's not even leet? :((")

    elif command == '1337ranks' or command == '/ranks':
        message = "Ranks: "
        readFile()
        ranks = readRanksFile()
        for user, score in userData[chat_id].items():
            message = message + str("\n") + ranks[int(score)] + " " + str(user)
        bot.sendMessage(chat_id, message)

    elif command == '420' and randint(0, 1) == 1:  # int(now.strftime('%H')) + 2 == 4 and int(now.strftime('%M')) == 20
        bot.sendMessage(msg['from']['id'], "http://www.huhmagazine.co.uk/images/uploaded/index/snoop_twitter_02.jpg")

    # debuggaus komentoja, muuta kommenteiksi julkaisussa(?)
    # elif command == '/debug':
    #	bot.sendMessage(chat_id, chat_id)
    #	bot.sendMessage(chat_id, userid)
    #	bot.sendMessage(chat_id, tsatti_lista[chat_id])

    # elif command == '/readFile':
    #	print(readFile())

    # elif command == '/writeFile':
    #	writeFile(tsatti_lista)

    elif command == '/printRanks':
        print(readRanksFile())
        bot.sendMessage(chat_id, readRanksFile())

        # elif command == '/reset':
        #	latestLeetDay = int(datetime.datetime.now().strftime ("%Y%m%d"))-1


        # else:
        #	bot.sendMessage(chat_id, "Tuntematon komento. Ota yhteys luojaani saadaksesi lisatietoa.")


bot = telepot.Bot('botin id tähän')
bot.notifyOnMessage(handle)
print("Waiting for input...")

while True:
    time.sleep(10)
