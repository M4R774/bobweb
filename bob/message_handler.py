import data_handler

from random import randint
import time

import sys
import os
sys.path.append('C:/Users/martt/OneDrive/Harrasteprojektit/bobweb/web')  # needed for sibling import
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
from django.conf import settings
django.setup()
from halloffame.models import *

# TODO optimoi leetin suoritusjärjestys
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
        mario.first_name = msg['from']['first_name']
    if 'last_name' in msg['from']:
        mario.last_name = msg['from']['last_name']
    if 'username' in msg['from']:
        mario.username = msg['from']['username']
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

    if msg['text'] == "ChatMember_test":
        sender = ChatMember.objects.get(chat=str(msg['chat']['id']),
                                        tg_user=str(msg['from']['id']))
        sender.rank = sender.rank + 1
        sender.save()
        reply = ChatMember.objects.all()
        bot.sendMessage(str(msg['chat']['id']), str(reply))


# TODO: Solve the userid problem ASAP
def bob_handler(msg, bot):
    bob_chat = Chat.objects.get(id=str(msg['chat']['id']))
    sender = ChatMember.objects.get(chat=str(msg['chat']['id']),
                                    tg_user=str(msg['from']['id']))
    if msg['text'] == '1337' and \
            int(time.strftime("%H")) == 13 and \
            int(time.strftime("%M")) == 37 and \
            bob_chat.latestLeet != date.today():
        bob_chat.latestLeet = date.today()
        ranks = data_handler.read_ranks_file()

        if sender.rank < 56:
            sender.rank += 1
            up = u"\U0001F53C"
            reply = "Elite! " + userid + " has been promoted to " + \
                    ranks[sender.rank] + "! " + up
            bot.sendMessage(bob_chat.id, reply)
        else:
            sender.rank = 0
            sender.prestige += 1
    # 33% chance for demotes
    elif msg['text'] == '1337' and randint(0, 2) == 0:
        if sender.rank > 0:
            sender.rank -= 1
        down = u"\U0001F53D"
        reply = "Rookie mistake! " + userid + " has been demoted to " + \
                ranks[sender.rank] + ". " + down
        bot.sendMessage(bob_chat.id, reply)
# ################ SAVE THE USER ########################


def ministry_of_media_handler(msg, bot):
    # Paskapostausfeatureita tänne
    pass


def msg_handler(msg, bot, settings_data):
    update_user_db(msg)
    if str(msg['chat']['id']) == settings_data['bob_ID']:
        bob_handler(msg, bot)
    elif str(msg['chat']['id']) == settings_data['ministry_of_media_ID']:
        bob_handler(msg, bot)

    if str(msg['from']['id']) == settings_data['dev_ID']:
        debug_handler(msg, bot)


"""
    chat_dict = data_handler.read_json_file("bob-data.json")
    #if "chats" not in chat_dict.keys():
    #    chat_dict['chats'] = {}

    # Test prints
    # print("chat_dict:", chat_dict)
    # print("msg:", msg)
    # print(msg['chat']['id'])
    # print(chats.keys())

    if msg_chat_id not in chats.keys():
        chats[msg_chat_id] = {}
        chats[msg_chat_id]['users'] = {}
        chats[msg_chat_id]['users'][msg_from_id] = {}
        chats[msg_chat_id]['users'][msg_from_id]['score'] = 0
        chats[msg_chat_id]['users'][msg_from_id]['prestige'] = 0
        chats[msg_chat_id]['users'][msg_from_id]['userid'] = userid
        chats[msg_chat_id]['latestleet'] = "4000 BC"
        chats[msg_chat_id]['mistakes'] = 0
        chats[msg_chat_id]['registered'] = time.strftime("%d.%m.%Y")
        chats[msg_chat_id]['messages'] = 0

    chats[msg_chat_id]['messages'] += 1

    if message == '1337':
        today = time.strftime("%d.%m.%Y")
        nowhours = time.strftime("%H")
        nowminutes = time.strftime("%M")

        #print(msg_from_id)
        #print(chats[msg_chat_id]['users'].keys())
        if nowhours == 13 and 36 <= nowminutes <= 38:
            ranks = data_handler.read_ranks_file()
            if chats[msg_chat_id]['latestleet'] != today:
                chats[msg_chat_id]['latestleet'] = today
                if chats[msg_chat_id]['users'][msg_from_id]['score'] < 56:
                    if msg_from_id not in chats[msg_chat_id]['users'].keys():
                        chats[msg_chat_id]['users'][msg_from_id]['score'] = 1
                        chats[msg_chat_id]['users'][msg_from_id]['prestige'] = 0
                        chats[msg_chat_id]['users'][msg_from_id]['userid'] = userid
                    else:
                        chats[msg_chat_id]['users'][msg_from_id]['score'] += 1
                    up = u"\U0001F53C"
                    reply = "Elite! " + userid + " has been promoted to " + ranks[chats[msg_chat_id]['users'][msg_from_id]['score']] + "! " + up
                    bot.sendMessage(msg_chat_id, reply)
                else:
                    chats[msg_chat_id]['users'][msg_from_id]['score'] = 0
                    chats[msg_chat_id]['users'][msg_from_id]['prestige'] += 1
            else:
                # 33% chance for demotes
                if randint(0, 2) == 0:
                    if chats[msg_chat_id]['users'][msg_from_id]['score'] > 0:
                        chats[msg_chat_id]['users'][msg_from_id]['score'] -= 1
                    down = u"\U0001F53D"
                    reply = "Rookie mistake! " + userid + " has been demoted to " + ranks[chats[msg_chat_id]['users'][msg_from_id]['score']] + ". " + down
                    bot.sendMessage(msg_chat_id, reply)
                chats[msg_chat_id]['mistakes'] += 1
    # print(chat_dict[msg_chat_id])
    data_handler.write_json_file(chat_dict, "bob-data.json")

    if message == "meri on tullut takaisin123" and msg_chat_id == "67948831":
        settings = data_handler.read_json_file("settings.json")
        sunglasses = u"\U0001F60E"
        reply = "I'm back! " + sunglasses + " #hype"
        bot.sendMessage(settings["bob_ID"], reply)
"""

