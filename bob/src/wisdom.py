import random
from datetime import date
import logging
from django.utils import timezone
from django.db.models import Max
from django.db.models import Sum
import django
import sys
import os
sys.path.append('../../web')  # needed for sibling import
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
from django.conf import settings
django.setup()
# Seperate imports to remove red underlines
from halloffame.models import Chat, TelegramUser, ChatMember, Proverb
logger = logging.getLogger("bob_logger")


def respond_with_random_wisdom(msg, bot):
    wisdom = stale_proverb()
    bot.sendMessage(msg['chat']['id'], wisdom)

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


def add_new_wisdom_to_database(msg, bot):
    # TODO: Max char limit to?
    # TODO: 10% chance for the unix wisdom
    pass


"""
# Post random proverb
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
"""


def get_proverb():
    proverb = get_last_proverb_with_randomness()
    update_proverb_access_date_and_count(proverb)
    return proverb


def get_last_proverb_with_randomness():
    proverbs = Proverb.objects.all()
    for i in range(0, proverbs.count()):
        if 0.9 < random.random():
            return proverbs[i]
    return proverbs.last()


def update_proverb_access_date_and_count(proverb):
    proverb.send_count += 1
    proverb.last_seen = date.today()
    proverb.save()
