"""
Handler for user's command 
"""

from telebot import TeleBot

from telegram_bot import keyboard_markups


def command_handler(bot: TeleBot):
    @bot.message_handler(
        commands=[
            "help",
        ]
    )
    def send_help(message):
        bot.reply_to(message, "1. Выберите параметры для оповещений.\n")

    @bot.message_handler(
        commands=[
            "start",
        ]
    )
    def send_start(message):
        """
        Send the list of transport as keyboard
        """
        msg = (
            "<b>Транспортный бот Еревана:</b>\n"
            "1. выберите номер транспорта для показа маршрута\n"
            "2. 'название остановки' - "
            "узнать, какой транспорт идет через остановку\n"
        )

        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
            reply_markup=keyboard_markups.create_all_bus_keyboard_markup(),
        )
