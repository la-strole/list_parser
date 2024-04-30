import os

from dotenv import load_dotenv
from telebot import TeleBot

from list_am_parser import list_am_scrapper
from telegram_bot import callback_handler, command_handler, message_handler

# Add a bot instance.
load_dotenv()
token = os.getenv("TLG_BOT_TOKEN")

assert token
bot = TeleBot(token)

command_handler.command_handler(bot)
message_handler.message_handler(bot)
callback_handler.callback_handler(bot)

if __name__ == "__main__":

    GET_PARAMS = {
        "n": "1",  # ереван
        "price2": "500000",  # цена до disallow by robots.txt
        "crc": "0",  # валюта 0 - драмы, 1 - usd
        "_a3_1": "80",  # площадь от
        "gl": "2",  #  1 галерея, 2 - список
    }

    result = list_am_scrapper(GET_PARAMS, bot)
    assert result
    bot.infinity_polling()
