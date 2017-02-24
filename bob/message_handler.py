import data_handler

from random import randint
import time

# TODO optimoi leetin suoritusjärjestys
# TODO tee assign_name funktiosta fiksumpi

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

    # Test prints
    #print("chat_dict:", chat_dict)
    #print("msg:", msg)
    # print(msg['chat']['id'])
    #print(chats.keys())

    if msg_chat_id not in chats.keys():
        chats[msg_chat_id] = {}
        chats[msg_chat_id]['users'] = {}
        chats[msg_chat_id]['users'][msg_from_id] = {}
        chats[msg_chat_id]['users'][msg_from_id]['score'] = 0
        chats[msg_chat_id]['latestleet'] = "4000 BC"
        chats[msg_chat_id]['mistakes'] = 0
        chats[msg_chat_id]['registered'] = time.strftime("%d.%m.%Y")
        chats[msg_chat_id]['messages'] = 0

    chats[msg_chat_id]['messages'] += 1

    if message == '1337':
        userid = assign_name(msg)
        today = time.strftime("%d.%m.%Y")
        nowhours = time.strftime("%H")
        nowminutes = time.strftime("%M")

        #print(msg_from_id)
        #print(chats[msg_chat_id]['users'].keys())
        if True: #nowhours == 13 and 36 <= nowminutes <= 38:
            if chats[msg_chat_id]['latestleet'] != today:
                chats[msg_chat_id]['latestleet'] = today
                if msg_from_id not in chats[msg_chat_id]['users']:
                    chats[msg_chat_id]['users'][msg_from_id]['score'] = 1
                else:
                    chats[msg_chat_id]['users'][msg_from_id]['score'] += 1
                up = u"\U0001F53C"
                reply = userid + " has been promoted! " + up
                bot.sendMessage(msg_chat_id, reply)
            else:
                # 20% chance for demotes
                if randint(0, 2) == 0:
                    chats[msg_chat_id]['users'][msg_from_id]['score'] -= 1
                    up = u"\U0001F53C"
                    reply = "Rookie mistake! " + userid + " has been demoted. " + up
                    bot.sendMessage(msg_chat_id, reply)
                chats[msg_chat_id]['mistakes'] += 1

    if message == "moi123":
        sunglasses = u"\U0001F60E"
        reply = "Moi! " + sunglasses + " #hype"
        bot.sendMessage(msg_chat_id, reply)

    print(chat_dict)
    data_handler.write_json_file(chat_dict, "bob-data.json")
