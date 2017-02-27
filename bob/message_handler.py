import data_handler

from random import randint
import time

# TODO optimoi leetin suoritusjärjestys
# TODO tee assign_name funktiosta fiksumpi

# TODO nimet järjestykseen


def assign_name(msg):
    try:
        firstname = msg['from']['first_name']
        userid = msg['from']['last_name'] + " " + firstname[0] + "."
    except:
        try:
            userid = msg['from']['last_name']
        except:
            try:
                userid = msg['from']['first_name']
            except:
                try:
                    userid = str(msg['from']['username'])
                except:
                    userid = str(msg['from']['id'])
    return userid


def bob_handler(msg, bot):
    chat_dict = data_handler.read_json_file("bob-data.json")
    if "chats" not in chat_dict.keys():
        chat_dict['chats'] = {}
    chats = chat_dict['chats']
    message = msg['text']
    msg_chat_id = str(msg['chat']['id'])
    msg_from_id = str(msg['from']['id'])
    userid = assign_name(msg)
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
