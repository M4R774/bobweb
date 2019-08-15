import telepot
from telepot.loop import MessageLoop
import sys
import json
import logging.config
import reminder
import time
import schedule
import message_handler
from postgres import Postgres


def main_loop():
    while True:
        # reminder.check_reminders(bob)
        # schedule.run_pending()
        time.sleep(60)


def get_bot_token():
    with open("settings.json", mode="r") as data_file:
        json_string = data_file.read()
        settings_data = json.loads(json_string)
        return settings_data["bot_token"]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        message_handler.msg_handler(msg, bob, db_connection)

"""
def init_db_connection():
    try:
        db = connect_to_database()
        return db
    except: # TODO: Narrow down handling
        logger.error("Database connection failed. ")
        exit(1)


def connect_to_database():
    db = Postgres("postgresql://postgres:postgres@db:5432/postgres")
    logger.info("Database connection initialized. ")
    return db
"""

logger = logging.getLogger("bob_logger")
db_connection = init_db_connection()
bob = telepot.Bot(get_bot_token())
MessageLoop(bob, handle).run_as_thread()
