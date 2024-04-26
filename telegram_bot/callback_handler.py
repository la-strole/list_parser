"""
Callback data handler
"""

import logging

from pydantic import ValidationError
from telebot import TeleBot

import database
import logger_config
import normalization_validation
from telegram_bot import keyboard_markups

logger = logging.getLogger(__name__)


def callback_handler(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        # Retrieve the callback data from the button that was clicked.
        callback_data: str = call.data

        # Perform actions based on the callback data

        # Send_duplicates option.
        if callback_data in ("1", "2"):

            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "send_duplicates"}
                    ).option_name
                )
                option_value = normalization_validation.BooleanOption.model_validate(
                    {"option": callback_data == "1"}
                ).option

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # price_value_amd option
            msg = "<b>Максимальная цена в AMD</b>\nОтвет в reply."
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.max_price_amd(),
            )

        # max price not set
        elif callback_data == "9":
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "price_value_amd"}
                    ).option_name
                )
                option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # Set agent_status
            msg = "<b>Объявления от собственников или агенств</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.agent_status(),
            )

        # Set agent status
        elif callback_data in ("3", "4", "5"):

            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "agent_status"}
                    ).option_name
                )
                if callback_data == "3":
                    option_value = False
                elif callback_data == "4":
                    option_value = True
                else:
                    option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # garage option
            msg = "<b>Наличие гаража?</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.garage_option(),
            )

        # Set garage status
        elif callback_data in ("6", "7", "8"):
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "garage"}
                    ).option_name
                )
                if callback_data == "6":
                    option_value = True
                elif callback_data == "7":
                    option_value = False
                else:
                    option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # rooms_count option
            msg = "<b>Количество комнат (1-8)</b>\nОтвет в reply."
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.room_count(),
            )

        # Set room_count status
        elif callback_data == "10":
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "rooms_count"}
                    ).option_name
                )
                option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # furniture option
            msg = "<b>Наличие мебели</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.furniture(),
            )

        # Set furniture option
        elif callback_data in ("11", "12", "13", "14", "15"):
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "furniture"}
                    ).option_name
                )
                if callback_data == "11":
                    option_value = "Есть"
                elif callback_data == "12":
                    option_value = "Нет"
                elif callback_data == "13":
                    option_value = "Частичная мебель"
                elif callback_data == "14":
                    option_value = "По договоренности"
                else:
                    option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # children_allowed option
            msg = "<b>Можно с детьми</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.children(),
            )

        # Set children_allowed option
        elif callback_data in ("16", "17", "18"):
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "children_allowed"}
                    ).option_name
                )
                if callback_data == "16":
                    option_value = True
                elif callback_data == "17":
                    option_value = False
                else:
                    option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # animals_allowed option
            msg = "<b>Можно с животными</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.animals(),
            )

        # Set animals_allowed option
        elif callback_data in ("19", "20", "21"):
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "animals_allowed"}
                    ).option_name
                )
                if callback_data == "19":
                    option_value = True
                elif callback_data == "20":
                    option_value = False
                else:
                    option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # total_area option
            msg = "<b>Общая площадь. ОТ Ответ в Reply</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.total_area(),
            )

        # set total area to undefined
        elif callback_data == "22":
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "total_area"}
                    ).option_name
                )

                option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # land_area option
            msg = "<b>Площадь участка. ОТ Ответ в Reply</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.land_area(),
            )

        # set land area to undefined
        elif callback_data == "23":
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "land_area"}
                    ).option_name
                )

                option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # floors_count option
            msg = "<b>Количество этажей. (1-4) Ответ в Reply</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.floors_count(),
            )

        # set floors_count to undefined
        elif callback_data == "24":
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "floors_count"}
                    ).option_name
                )

                option_value = None

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # district option
            msg = "<b>Выберите район.</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
                reply_markup=keyboard_markups.district(),
            )

        # set district
        elif callback_data in (
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
            "32",
            "33",
            "34",
            "35",
            "36",
            "37",
        ):
            try:
                user_id = normalization_validation.TlgUserId.model_validate(
                    {"user_id": call.from_user.id}
                ).user_id
                option_name = (
                    normalization_validation.TlgBotUserFilterOption.model_validate(
                        {"option_name": "district"}
                    ).option_name
                )

                option_dict = {
                    "25": "Ачапняк",
                    "26": "Арабкир",
                    "27": "Аван",
                    "28": "Давидашен",
                    "29": "Эребуни",
                    "30": "Зейтун Канакер",
                    "31": "Кентрон",
                    "32": "Малатия Себастия",
                    "33": "Нор Норк",
                    "34": "Шенгавит",
                    "35": "Норк Мараш",
                    "36": "Нубарашен",
                    "37": None,
                }

                option_value = option_dict[callback_data]

            except ValidationError as e:
                logger.error("callback_handler -> error: %s", e)
                bot.send_message(
                    call.message.chat.id,
                    text="Ошибка. Обратитесь к администратору.",
                    disable_notification=True,
                    parse_mode="HTML",
                )
                return None

            database.change_telegram_user_filtres_options(
                user_id, option_name, option_value
            )

            # Final
            msg = "<b>Ура! Все настроили.</b>"
            bot.send_message(
                call.message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="HTML",
            )
