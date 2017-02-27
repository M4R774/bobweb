import data_handler
from operator import itemgetter


def bob_friday(bot):
    message = "Its Friday! Ranks: "
    data_dict = data_handler.read_json_file("bob-data.json")
    settings = data_handler.read_json_file("settings.json")
    bob_chat_id = settings['bob_ID']
    ranks = data_handler.read_ranks_file()
    users_unsorted = []
    for userid in data_dict['chats'][bob_chat_id].keys():
        users_unsorted.append(data_dict['chats'][bob_chat_id][userid])

    users_sorted = sorted(users_unsorted, key=itemgetter('prestige', 'score'))
    for user in users_sorted:
        message = message + "\n" + ranks[user['score']] + user['userid']
    bot.sendMessage(bob_chat_id, message)

