import data_handler

import telepot


def bob_handler(msg):
    chat_dict = data_handler.read_json_file("bob-data.json")
    message = msg['text']
    existing_chats = []
    #print(chat_dict)
    for chat in chat_dict:
        #print(chat)
        existing_chats.append(chat_dict[chat])
    #print(msg)
    if msg['chat']['id'] not in existing_chats:
        chat_dict['chats'] = {}
        chat_dict['chats'][msg['chat']['id']] = {}
        chat_dict['chats'][msg['chat']['id']]['users'] = {}
        chat_dict['chats'][msg['chat']['id']]['users'][msg['from']['id']] = {}
        print(chat_dict)

    if message == '1337':
        if msg['from']['id'] in chat_dict['chats'][msg['chat']['id']]['users']:
            chat_dict['chats'][msg['chat']['id']]['users'][msg['from']['id']]['score'] += 1
        else:
            chat_dict['chats'][msg['chat']['id']]['users'][msg['from']['id']]['score'] = 1

# called everytime message arrives
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    settings = data_handler.read_json_file("settings.json")

    if True:  # content_type == "text" and settings["bob_ID"] == chat_id:
        bob_handler(msg)

"""
try:
chat_id = str(msg['chat']['id'])
chat_title = "null"
if int(chat_id) < 0:
    chat_title = msg['chat']['title']
command = msg['text']
ranks = readRanksFile()
global latest_leet_day
global mistakeLeets
if chat_id not in chat_list:
    chat_list[chat_id] = {}
"""
