import message_handler
import data_handler
import scheduled
import schedule
import telepot
import time
import json
import sys
import os

# TODO: Facelift for bobweb
# TODO: After successfull

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


