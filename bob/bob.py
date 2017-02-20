import message_handler
import data_handler

from telepot.delegate import pave_event_space, per_chat_id, create_open

# käyttäjä olio
# chat olio

import sys
import time
import telepot
import json

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
bot.message_loop(message_handler.handle)
print("Bob is now running and receiving messages. ")
print(bot.getMe())

while True:
    time.sleep(10)


