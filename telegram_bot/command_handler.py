"""
Handler for user's command 
"""

import logging

from pydantic import ValidationError
from telebot import TeleBot

import database
import logger_config
import normalization_validation
from telegram_bot import keyboard_markups

logger = logging.getLogger(__name__)


def command_handler(bot: TeleBot):
    """
    @bot.message_handler(
        commands=[
            "help",
        ]
    )
    def send_help(message):
        bot.reply_to(message, "1. Выберите параметры для оповещений.\n")
    """

    @bot.message_handler(
        commands=[
            "start",
        ]
    )
    def send_start(message):
        """
        Get user's start command options
        """
        # Add tlg user to database
        user_id = message.from_user.id
        try:
            clear_data = normalization_validation.TlgUserId.model_validate(
                {"user_id": user_id}
            )
        except ValidationError as e:
            logger.error(
                "command_handler -> send_start user_id validation error: %s", e
            )
        else:
            database.add_tlg_user_to_database(clear_data.user_id)
            msg = (
                "<b>Бот новых объявлений с list.am:</b>\n"
                "Давайте настроим оповещения:\n"
            )

            bot.send_message(
                message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
            )

            # send_duplicates option
            msg = "<b>Отправлять повторяющиеся объявления при их обновлении?</b>"
            bot.send_message(
                message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.send_duplicates(),
            )
