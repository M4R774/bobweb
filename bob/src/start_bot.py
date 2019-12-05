import logging.config
logging.config.fileConfig('log_settings.ini')
import bob

# TODO: Logging
# TODO: Containerization
# TODO: Settings as env variables instead of .json?
# TODO: xkcd spammer, random or latest?
# TODO: Reminder upgrades (replys, quotes?)
# TODO: Periodic proverbs (1 per 1-60 days)
# TODO: weather?
# TODO: For some reason, the reminder "pääsivätkö amikset Niina Tuonosen, 18v, ja Tommi Penttilän, 19v miljönääreiksi
# 30 vuotiaina? " was not saved fully, why is this?


def main():
    logger = logging.getLogger("bob_logger")
    logger.info("Hello world, I am Bob. :-)")
    start_bot()


def start_bot():
    logger = logging.getLogger("bob_logger")
    try:
        logger.info("Starting the main loop")
        bob.main_loop()
    except:  # TODO: Narrow down exception scope
        logger.error("Bob is rip... ")


if __name__ == "__main__":
    main()
