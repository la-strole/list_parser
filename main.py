import os

from dotenv import load_dotenv
from telebot import TeleBot

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
    bot.infinity_polling()
