import data_handler

from random import randint
import time

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
    """
    pass


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
            # bot.sendMessage(bob_chat.id, reply)
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
        # bot.sendMessage(bob_chat.id, reply)
    sender.save()


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



