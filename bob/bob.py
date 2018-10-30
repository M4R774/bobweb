import message_handler
import data_handler
import scheduled

# separately installed
import telepot
import schedule

import sys
import time
import json
import os

# Django db imports
import django
# import v10consolidator.settings

sys.path.append('C:/Users/martt/OneDrive/Harrasteprojektit/bobweb\web')
from halloffame.models import *

# TODO: Figure out how the django db works
# https://stackoverflow.com/questions/2180415/using-django-database-layer-outside-of-django

# TODO: Test the database

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
django.setup()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":  # and settings["bob_ID"] == chat_id:
        message_handler.bob_handler(msg, bot)


settings_data = {}
try:
    with open("settings.json", mode="r") as data_file:
        json_string = data_file.read()
        settings_data = json.loads(json_string)
except:
    print("Failed to read settings.json")
    print(sys.exc_info()[0])
    print("Exiting...")
    exit()

bot = telepot.Bot( settings_data["bot_token"] )
bot.message_loop(handle)

# commented out because of bug
# schedule.every().friday.at("16:15").do(scheduled.bob_friday(bot))


print("Bob is now running and receiving messages. ")
# print(bot.getMe())

while True:
    schedule.run_pending()
    time.sleep(60)


