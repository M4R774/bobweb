import message_handler
import reminder
import schedule
import telepot
import time
import json
import sys

# TODO: Logging
# TODO: Containerization
# TODO: Settings as env variables instead of .json
# TODO: xkcd spammer, random or latest?
# TODO: Reminder upgrades (replys, quotes?)
# TODO: Periodic proverbs (1 per 1-60 days)
# TODO: weather?

settings_data = {}


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":  # and settings_data["bob_ID"] == chat_id:
        message_handler.msg_handler(msg, bot, settings_data)


def main():
    # Read the settings.json in to a memory
    try:
        with open("settings.json", mode="r") as data_file:
            json_string = data_file.read()
            settings_data = json.loads(json_string)
    except FileNotFoundError:
        print("Error: settings.json file not found. ")
        print(sys.exc_info()[0])
        print("Exiting...")
        exit()

    bot = telepot.Bot(settings_data["bot_token"])
    bot.message_loop(handle)

    print("Bob is now running and receiving messages. ")

    while True:
        reminder.check_reminders(bot)
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
