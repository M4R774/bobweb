import data_handler
import re
from random import randint
import random
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
import logging
import sys
import os
from django.utils import timezone
from django.db.models import Max
from django.db.models import Sum
import django
sys.path.append('../web')  # needed for sibling import
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
from django.conf import settings
django.setup()
from halloffame.models import *

logger = logging.getLogger("bob_logger")


def msg_handler(msg, bot):
    logger.info("Received message. ")
    msg_sorter(msg, bot)
    update_user_db(msg)
    debug_handler(msg, bot)


# Figure out the type of the message
def msg_sorter(msg, bot):
    if msg['text'].lower() == "huutista":
        joka_tuutista(msg, bot)
    # muistuta
    # 1337
    # viisaus
    # uusi viisaus


def joka_tuutista(msg, bot):
    bot.sendMessage(msg['chat']['id'], "..joka tuutista! 😂")


# Adds the user and the chat to the db
def update_user_db(msg):
    # Check if the chat exists alredy or not:
    if Chat.objects.filter(id=msg['chat']['id']).count() > 0:
        pass
    else:
        chat = Chat(id=msg['chat']['id'])
        if int(msg['chat']['id']) < 0:
            chat.title = msg['chat']['title']
        chat.save()
    # TODO: Make update instead of replacing old user, just like for the chats
    # Telegram user
    mario = TelegramUser(id=str(msg['from']['id']))
    if 'first_name' in msg['from']:
        mario.firstName = msg['from']['first_name']
    if 'last_name' in msg['from']:
        mario.lastName = msg['from']['last_name']
    if 'username' in msg['from']:
        mario.nickname = msg['from']['username']
    logger.info("Successfully updated user-db. ")


def extract_nickname(msg):
    # TODO: clean this up
    nickname = "NULL"
    first_name = "NULL"
    last_name = "NULL"
    if 'last_name' in msg['from']:
        nickname = msg['from']['last_name']
        last_name = msg['from']['last_name']
    if 'first_name' in msg['from']:
        nickname = msg['from']['first_name']
        first_name = msg['from']['first_name']
    if 'username' in msg['from']:
        nickname = msg['from']['username']
    return nickname


def debug_handler(msg, bot):
    if msg['text'] == "moi":
        sunglasses = u"\U0001F60E"
        reply = "I'm back! " + sunglasses + " #hype"
        bot.sendMessage(str(msg['chat']['id']), reply)

    if msg['text'] == "TelegramUser.objects.all()":
        reply = TelegramUser.objects.all()
        bot.sendMessage(str(msg['chat']['id']), str(reply))

    if msg['text'] == 'timezone.localtime(timezone.now())':
        reply = str(timezone.localtime(timezone.now()))
        bot.sendMessage(str(msg['chat']['id']), str(reply))

    if msg['text'] == "ChatMember_test":
        sender = ChatMember.objects.get(chat=str(msg['chat']['id']),
                                        tg_user=str(msg['from']['id']))
        sender.rank = sender.rank + 1
        sender.save()
        reply = ChatMember.objects.all()
        bot.sendMessage(str(msg['chat']['id']), str(reply))


# If leet is missed [höh kukaan ei sanonut leet, voi rähmä 2 leetitöntä päivää putkeen :(,
# eikö kukaan taaskaan? Lopun ajat ovat koittaneet,
# yrittäkää nyt, harmittaa, masentaa,
# mitä iloa on elää jos kukaan ei sano 1337?]
def bob_handler(msg, bot):
    bob_chat = Chat.objects.get(id=str(msg['chat']['id']))
    sender = ChatMember.objects.get(chat=str(msg['chat']['id']),
                                    tg_user=str(msg['from']['id']))
    if msg['text'] == '1337':
        print('[INFO] ' + time.strftime("%H:%M:%S") + ' Received 1337 message. ')
        print('[INFO] ' + time.strftime("%H:%M:%S") + ' bob_chat.latestLeet: ' + str(bob_chat.latestLeet))
        print('[INFO] ' + time.strftime("%H:%M:%S") + ' date.today(): ' + str(date.today()))
        print('[INFO] ' + time.strftime("%H:%M:%S") + ' Sender rank before: ' + str(sender.rank))
        ranks = data_handler.read_ranks_file()
        if bob_chat.latestLeet != date.today() and \
                int(time.strftime("%H")) == 13 and \
                int(time.strftime("%M")) == 37:
            print('[INFO] ' + time.strftime("%H:%M:%S") + ' Time and date correct! ')
            bob_chat.latestLeet = date.today()
            bob_chat.save()
            if sender._rank < len(ranks) - 1:
                sender._rank += 1
                up = u"\U0001F53C"
                reply = "Asento! " + str(sender.tg_user) + " ansaitsi ylennyksen arvoon " + \
                        ranks[sender._rank] + "! " + up + " Lepo. "
            else:
                sender.prestige += 1
                reply = "Asento! " + str(sender.tg_user) + \
                        " on saavuttanut jo korkeimman mahdollisen sotilasarvon! Näin ollen " + str(sender.tg_user) + \
                        " lähtee uudelle kierrokselle. Onneksi olkoon! " + \
                        "Juuri päättynyt kierros oli hänen " + str(sender.prestige) + ". Lepo. "
                sender._rank = 0
            print('[SEND] ' + time.strftime("%H:%M:%S") + " " + reply)
            bot.sendMessage(msg['chat']['id'], reply)

        # 33% chance for demotes
        elif randint(0, 1) == 0:
            print('[INFO] ' + time.strftime("%H:%M:%S") + ' Incorrect time, removing points. ')
            if sender._rank > 0:
                sender._rank -= 1
            down = u"\U0001F53D"
            reply = "Alokasvirhe! " + str(sender.tg_user) + " alennettiin arvoon " + \
                    ranks[sender._rank] + ". " + down
            print('[SEND] ' + time.strftime("%H:%M:%S") + ' ' + reply)
            bot.sendMessage(msg['chat']['id'], reply)
        else:
            print('[INFO] ' + time.strftime("%H:%M:%S") + ' Incorrect time, but the user got lucky. ')
        print('[-END] ' + time.strftime("%H:%M:%S") + ' Sender rank after: ' + str(sender.rank))
        sender.save()


def random_proverb():
    pass
    # max_id = Proverb.objects.all().aggregate(max_id=Max("id"))['max_id']
    for i in range(0, 100):
        pk = random.randint(1, max_id)
        proverb = Proverb.objects.filter(pk=pk).first()
        if proverb:
            return proverb
    # If it takes over 100 tries, return empty
    return None


def rare_proverb():
    pass
    # proverb = Proverb.objects.all().first()
    proverb.save()
    return proverb


def semi_rare_proverb():
    pass
#     proverbs = Proverb.objects.all()
    for i in range(0, proverbs.count()):
        if 0.9 < random.random():
            return proverbs[i]
    return proverbs.last()


def set_reminder(msg, bot):
    # if fails, send error message describing usage and return
    chat = Chat.objects.get(id=str(msg['chat']['id']))
    # TODO: make also float number possible
    # TODO: make also possible to simply put the date in to this
    # TODO: add months also
    # Extract times                   1          2          3          4     5
    expr = re.match(r'muistuta ([0-9]+y )?([0-9]+d )?([0-9]+h )?([0-9]+m )?(.+)', msg['text'])
    if expr.group(1) or expr.group(2) or expr.group(3) or expr.group(4):
        remind_date = datetime.now()
        if expr.group(1):
            year = float(expr.group(1)[:-2])
            remind_date = remind_date + timedelta(days=year*365)
        if expr.group(2):
            day = float(expr.group(2)[:-2])
            remind_date = remind_date + timedelta(days=day)
        if expr.group(3):
            hour = float(expr.group(3)[:-2])
            remind_date = remind_date + timedelta(hours=hour)
        if expr.group(4):
            minute = float(expr.group(4)[:-2])
            remind_date = remind_date + timedelta(minutes=minute)
        remember_this = expr.group(5)
        reminder = Reminder(remember_this=remember_this, chat=chat, date=remind_date)
        reminder.save()
        reply = 'Muistutetaan ' + str(remind_date.strftime('%d.%m.%Y klo %H:%M'))
        bot.sendMessage(msg['chat']['id'], reply)
    else:
        reply = 'Muistutus oli väärää muotoa. '
        bot.sendMessage(msg['chat']['id'], reply)
        print('[ERRO] Something went wrong')


# Shitposting features here
def spammer(msg, bot):
    pass
    # # Post random proverb
    if msg['text'].lower() == 'viisaus':
        proverb = semi_rare_proverb()
        proverb.send_count += 1
        proverb.save()
        if proverb.author:
            author = ' - ' + proverb.author
        else:
            author = ''
        if proverb.date:
            year = str(proverb.date.year)
        else:
            year = ''
        reply = proverb.proverb + author + ' ' + year
        bot.sendMessage(msg['chat']['id'], reply)
    # Add new proverb
    elif msg['text'][:14].lower() == 'uusi viisaus: ':
        sender_name = str(TelegramUser.objects.get(id=str(msg['from']['id'])))
        proverb = Proverb(proverb=msg['text'][14:], author=sender_name, date=date.today())
        proverb.save()
        reply = 'Viisaus tallennettu. '
        bot.sendMessage(msg['chat']['id'], reply)
    elif msg['text'].lower() == "bob, kuinka viisas olet?":
        reply = str(Proverb.objects.all().count())
        bot.sendMessage(msg['chat']['id'], reply)
    # Reminder
    elif msg['text'][:9].lower() == 'muistuta ':
        set_reminder(msg, bot)
    # If string "_* vai _*" is found, make split and post random
    elif re.search(r'..*\svai\s..*', msg['text']) is not None:
        options = re.split(r'\svai\s', msg['text'])
        reply = (random.choice(options))
        print('[SEND] ' + time.strftime("%H:%M:%S") + " " + reply)
        bot.sendMessage(msg['chat']['id'], reply)
    elif msg['text'].lower() == "huutista":
        reply = '...joka tuutista! 😂'
        bot.sendMessage(msg['chat']['id'], reply)




