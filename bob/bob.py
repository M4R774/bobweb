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
#
# siis otsikkona chatin id ja taman perassa kayttajien pisteet.
# Eri chatit erottuvat toisistaan tyhjalla rivilla, jotka ohjelma etsii.
# Tyhjia riveja saa olla toistaiseksi vain tasan 1 chattien valissa

# tiedoston nimi jonne 1337 pisteet tallennetaan
scoresFileName = "1337scores.txt"

# Dict where all info about users is saved before writing to .txt file
tsatti_lista = {}

# Ranks read from ranks.txt
ranks = []

global latestLeetDay
latestLeetDay = int(datetime.datetime.now().strftime("%Y%m%d")) - 1


# Reads the ranks.txt to ranks list and returns the list
def readRanksFile():
    file = open('ranks.txt')

    for line in file:
        # strip removes all whitsespaces from end and beginning
        line = line.strip()
        ranks.append(line)
    file.close()
    return ranks


# Lukee tiedoston tietorakenteeseen, palauttaa tsatti_lista:n
def readFile():
    # try:
    # scoresFileNamelle annetaan arvo koodin alussa
    file = open(scoresFileName, 'r')

    firstAfterEmptyLine = True
    lineNumber = 1
    for line in file:
        line = line.strip()
        if line == "":
            # print("R%s Tyhj� rivi"%(lineNumber))
            firstAfterEmptyLine = True

        elif firstAfterEmptyLine:
            firstAfterEmptyLine = False
            # chat_id on seuraava rivi jolla lukee jotain tyhjan rivin jalkeen
            # ja se viedaan dictiin
            # elements = line.rsplit("|")
            # chat_id = elements[0]
            chat_id = line
            tsatti_lista[chat_id] = {}
        # print("R%s chatID= %s" %(lineNumber, chat_id))

        else:
            elements = line.rsplit("|")
            if len(elements) == 2:
                # print("R%s %s, kelpaa"%(lineNumber, line))
                tsatti_lista[chat_id][elements[0]] = elements[1]
            else:
                pass
                # print("R%s %s, virheellinen"%(lineNumber, line))

        lineNumber = lineNumber + 1
    file.close()
    return tsatti_lista


# except:
#	print("Virhe: Tiedostoa ei saa luettua")
#	bot.sendMessage(DEBUG CHATIN ID TÄHÄN, "Botti on havainnut virheen, tiedostoa ei saatu luettua")

# Kirjoittaa tietorakenteen tiedostoon
def writeFile(tsatti_lista):
    #	try:
    # scoresFileNamelle annetaan arvo koodin alussa
    file = open(scoresFileName, 'w')
    for chat_id in tsatti_lista:
        file.write(str(chat_id) + str("\n"))

        for user in tsatti_lista[str(chat_id)]:
            try:
                file.write(str(user) + "|" + str(tsatti_lista[chat_id][user]) + str("\n"))
            except:
                pass
        file.write(str("\n"))
    file.close


"""
	except:
		print("Virhe: Tiedostoa ei saa luettua")
		bot.sendMessage(DEBUG CHATIN ID TÄHÄN, "Botti on havainnut virheen, tiedostoa ei saatu kirjoitettua")
"""


def handle(msg):
    chat_id = str(msg['chat']['id'])
    # tsatti_lista = readFile()
    chat_title = "null"

    if int(chat_id) < 0:
        chat_title = msg['chat']['title']
    command = msg['text']
    ranks = readRanksFile()
    global latestLeetDay

    if chat_id in tsatti_lista:
        pass
    else:
        tsatti_lista[chat_id] = {}

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
                if userid in str(tsatti_lista[chat_id]):
                    tsatti_lista[chat_id][userid] = int(tsatti_lista[chat_id][userid]) + 1
                else:
                    tsatti_lista[chat_id][userid] = 1

                message = str('Elite! %s has been promoted to %s' % (userid, ranks[int(tsatti_lista[chat_id][userid])]))
                bot.sendMessage(chat_id, message)
                writeFile(tsatti_lista)
                latestLeetDay = int(datetime.datetime.now().strftime("%Y%m%d"))
            else:
                bot.sendMessage(chat_id, ("%s was too slow :(" % userid))

        else:
            bot.sendMessage(chat_id, "But it's not even leet? :((")

    elif command == '1337ranks' or command == '/ranks':
        message = "Ranks: "
        readFile()
        ranks = readRanksFile()
        for user, score in tsatti_lista[chat_id].items():
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
