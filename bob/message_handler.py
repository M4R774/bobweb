import data_handler
import re
from random import randint
import random
import time
from datetime import date
import sys
import os
sys.path.append('../web')  # needed for sibling import
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
from django.conf import settings
django.setup()
from halloffame.models import *

# TODO tee assign_name funktiosta fiksumpi
# TODO nimet järjestykseen


# Adds the user to the db
def update_user_db(msg):
    # Chat
    chat = Chat(id=msg['chat']['id'])
    if int(msg['chat']['id']) < 0:
        chat.title = msg['chat']['title']
    chat.save()

    # Telegram user
    mario = TelegramUser(id=str(msg['from']['id']))
    if 'first_name' in msg['from']:
        mario.firstName = msg['from']['first_name']
    if 'last_name' in msg['from']:
        mario.lastName = msg['from']['last_name']
    if 'username' in msg['from']:
        mario.nickname = msg['from']['username']
    mario.save()

    # The relation between tg user and chat
    if ChatMember.objects.filter(chat=str(msg['chat']['id']),
                                 tg_user=str(msg['from']['id']))\
                                 .exists():
        pass
    else:
        chat_member = ChatMember(chat=Chat.objects.get(id=str(msg['chat']['id'])),
                        tg_user=TelegramUser.objects.get(id=str(msg['from']['id'])))
        chat_member.save()
    return mario


def debug_handler(msg, bot):
    """
    if msg['text'] == "moi":
        sunglasses = u"\U0001F60E"
        reply = "I'm back! " + sunglasses + " #hype"
        bot.sendMessage(str(msg['chat']['id']), reply)
    """
    if msg['text'] == "TelegramUser.objects.all()":
        reply = TelegramUser.objects.all()
        bot.sendMessage(str(msg['chat']['id']), str(reply))
    """
    if msg['text'] == "ChatMember_test":
        sender = ChatMember.objects.get(chat=str(msg['chat']['id']),
                                        tg_user=str(msg['from']['id']))
        sender.rank = sender.rank + 1
        sender.save()
        reply = ChatMember.objects.all()
        bot.sendMessage(str(msg['chat']['id']), str(reply))
    """
    pass


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
            if sender.rank <= len(ranks):
                sender.rank += 1
                up = u"\U0001F53C"
                reply = "Asento! " + str(sender.tg_user) + " ansaitsi ylennyksen arvoon " + \
                        ranks[sender.rank] + "! " + up + " Lepo. "
            else:
                sender.prestige += 1
                reply = "Asento! " + str(sender.tg_user) + \
                        " on saavuttanut jo korkeimman mahdollisen sotilasarvon " + \
                        ranks[sender.rank] + "! Näin ollen " + str(sender.tg_user) + \
                        " lähtee uudelle kierrokselle. Onneksi olkoon! " + \
                        "Juuri päättynyt kierros oli hänen " + str(sender.prestige) + ". Lepo. "
                sender.rank = 0
            print('[SEND] ' + time.strftime("%H:%M:%S") + reply)
            # bot.sendMessage(msg['chat']['id'], reply)

        # 33% chance for demotes
        elif randint(0, 2) == 0:
            print('[INFO] ' + time.strftime("%H:%M:%S") + ' Incorrect time, removing points. ')
            if sender.rank > 0:
                sender.rank -= 1
            down = u"\U0001F53D"
            reply = "Alokasvirhe! " + str(sender.tg_user) + " alennettiin arvoon " + \
                    ranks[sender.rank] + ". " + down
            print('[SEND] ' + time.strftime("%H:%M:%S") + reply)
            # bot.sendMessage(msg['chat']['id'], reply)
        else:
            print('[INFO] ' + time.strftime("%H:%M:%S") + ' Incorrect time, but the user got lucky. ')
        print('[-END] ' + time.strftime("%H:%M:%S") + ' Sender rank after: ' + str(sender.rank))
    sender.save()


def spammer(msg, bot):
    # Shitposting features here

    # If string "_* vai _*" is found, make split and post random
    if re.search(r'..*\svai\s..*', msg['text']) is not None:
        options = re.split(r'\svai\s', msg['text'])
        reply = (random.choice(options))
        print('[SEND] ' + time.strftime("%H:%M:%S") + " " + reply)
        bot.sendMessage(msg['chat']['id'], reply)

    # TODO: Viisaus (proverb feature)
    # viisaus: post random proverb
    # uusi viisaus: parempi pyy pivossa kuin 10 oksalla


def msg_handler(msg, bot, settings_data):
    # print('Received message. ' + str(msg))
    update_user_db(msg)
    if True: # str(msg['chat']['id']) == settings_data['bob_ID']:
        bob_handler(msg, bot)

    if str(msg['chat']['id']) != settings_data['bob_ID']:
        spammer(msg, bot)

    if str(msg['from']['id']) == settings_data['dev_ID']:
        debug_handler(msg, bot)



