"""
Project entry point
"""

import atexit
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv
from telebot import TeleBot

import logger_config
from database import create_database
from list_am_parser import list_am_scrapper
from telegram_bot import callback_handler, command_handler, message_handler

logger = logging.getLogger(__name__)

# Add a bot instance.
load_dotenv()
token = os.getenv("TLG_BOT_TOKEN")

assert token
bot = TeleBot(token)

command_handler.command_handler(bot)
message_handler.message_handler(bot)
callback_handler.callback_handler(bot)

if __name__ == "__main__":

    # Get only this adv from list.am
    GET_PARAMS = {
        "n": "1",  # ереван
        "price2": "500000",  # цена до disallow by robots.txt
        "crc": "0",  # валюта 0 - драмы, 1 - usd
        "_a3_1": "80",  # площадь от
        "gl": "2",  #  1 галерея, 2 - список
    }

    # create_database()

    list_am_scrapper(bot, GET_PARAMS)

    # create schedule for parsing time
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=list_am_scrapper,
        args=[bot, GET_PARAMS],
        # Set interval
        trigger=IntervalTrigger(seconds=1800),
        id="list_am_scrapper",
        name="Get data every 30 minutes",
        replace_existing=True,
    )
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # Run tlg bot
    bot.infinity_polling()
