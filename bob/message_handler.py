import data_handler

import telepot


def text_handler(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    settings = data_handler.read_json_file("settings.json")

    if settings["bob_ID"] == chat_id:
        # bobiin tulevat viestit
        pass


# called everytime message arrives
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    settings = data_handler.read_json_file("settings.json")

    if content_type == "text" and settings["bob_ID"] == chat_id:
        text_handler(msg)
