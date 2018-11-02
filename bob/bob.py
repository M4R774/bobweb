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
# How to use the django db from the bob:
# https://stackoverflow.com/questions/2180415/using-django-database-layer-outside-of-django

# TODO: Test the database
# TODO: Fix absolute paths
# TODO: Think solution for duplicate database problem
#   - Database only in bob folder?
#       - Need to change the django db folder
#   - Bot uses the database folder from the django folder
#       - Lets do this! How?
settings_data = {}


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":  # and settings_data["bob_ID"] == chat_id:
        message_handler.msg_handler(msg, bot, settings_data)


# Read the settings.json in to a memory
try:
    with open("settings.json", mode="r") as data_file:
        json_string = data_file.read()
        settings_data = json.loads(json_string)
except:
    print("Failed to read settings.json")
    print(sys.exc_info()[0])
    print("Exiting...")
    exit()

bot = telepot.Bot(settings_data["bot_token"])
bot.message_loop(handle)

# commented out because of bug
# schedule.every().friday.at("16:15").do(scheduled.bob_friday(bot))

os.chdir('../web')
print("Bob is now running and receiving messages. ")

while True:
    schedule.run_pending()
    time.sleep(60)


