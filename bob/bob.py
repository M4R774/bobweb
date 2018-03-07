import message_handler
import data_handler
import scheduled

# seperately installed
import telepot
import schedule

import sys
import time
import json
import os
from . web/halloffame.models import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


# Have to do this for it to work in 1.9.x!
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#############

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


