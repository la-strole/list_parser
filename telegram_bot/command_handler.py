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
        chat_id = message.chat.id
        try:
            clear_data = normalization_validation.TlgUserId.model_validate(
                {"user_id": user_id}
            )
            clear_data_chat = normalization_validation.TlgChatId.model_validate(
                {"chat_id": chat_id}
            )
        except ValidationError as e:
            logger.error(
                "command_handler -> send_start user_id validation error: %s", e
            )
        else:
            database.add_tlg_user_to_database(
                clear_data.user_id, clear_data_chat.chat_id
            )
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
            msg = (
                "<b>Отправлять объявления с тем же id при их обновлении? (1 из 12)</b>"
            )
            bot.send_message(
                message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.send_duplicates(),
            )

    @bot.message_handler(
        commands=[
            "mysettings",
        ]
    )
    def send_user_settings(message):
        """
        Send user's settings
        """
        # Get user's settings from the database
        user_id = message.from_user.id
        clear_data = normalization_validation.TlgUserId.model_validate(
            {"user_id": user_id}
        )
        par = database.get_user_params_from_database(clear_data.user_id)
        if par:
            msg = "<b>Текущие настройки:</b>\n"
            # Get reverse test from normalization/validation
            for par_name in par:
                # Get reverse name
                for key, value in normalization_validation.valid_keys.items():
                    if value == par_name:
                        if par[par_name] is None:
                            msg = msg + f"<b>{key}:</b> не определено\n"
                        elif par_name in (
                            "send_duplicates",
                            "agent_status",
                            "garage",
                            "children_allowed",
                            "animals_allowed",
                        ):
                            msg = (
                                msg + f"<b>{key}:</b> Да\n"
                                if par[par_name] == 1
                                else msg + f"<b>{key}:</b> Нет\n"
                            )
                        else:
                            msg = msg + f"<b>{key}:</b> {par[par_name]}\n"
                        break

        else:
            msg = "Увы, пока нет сохраненных настроек."

        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
        )

    @bot.message_handler(
        commands=[
            "help",
        ]
    )
    def send_help(message):
        """
        Send help msg
        """
        msg = (
            "Бот раз в 30 минут отправляет сообщения о новых объявлениях "
            "по аренде домов в Ереване на list.am в соответствии с выбранными фильтрами. "
            "Выберите /start для настройки фильтров. Вы можете изменить их в любой момент, "
            "заново ответив на сообщения (или перенастроить их все, нажав еще раз /start). "
            "Просмотреть текущие фильтры можно в меню командой /mysettings. \nУдачи в поиске!"
        )

        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
        )
