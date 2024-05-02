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
            msg = "<b>Максимальная цена в AMD</b>\nОтвет в reply. (2 из 12)"
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
            msg = "<b>Объявления от собственников или агентств (3 из 12)</b>"
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
            msg = "<b>Наличие гаража? (4 из 12)</b>"
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
            msg = "<b>Количество комнат (1-8)</b>\nОтвет в reply. (5 из 12)"
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
            msg = "<b>Наличие мебели (6 из 12)</b>"
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
            msg = "<b>Можно с детьми (7 из 12)</b>"
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
            msg = "<b>Можно с животными (8 из 12)</b>"
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
            msg = "<b>Общая площадь. \n кв.м. ОТ \nОтвет в Reply (9 из 12)</b>"
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
            msg = "<b>Площадь участка.\n кв.м. ОТ \nОтвет в Reply (10 из 12)</b>"
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
            msg = "<b>Количество этажей. (1-4) Ответ в Reply (11 из 12)</b>"
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
            msg = "<b>Выберите район. (12 из 12)</b>"
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

        elif callback_data == "details":
            # Get message id
            text = call.message.text
            try:
                item_id = text[text.rfind("/") + 1 :]
                assert int(item_id)
            except ValueError as e:
                logger.error(
                    "Callback -> details: Can not get item id from message: %s", e
                )
                return None

            try:
                # Get into form database
                row = database.get_item_info(item_id)
                assert (
                    row
                ), f"Callback -> Can not get data from database for item with id {id}"
                if row["agent_status"] == 1:
                    agency = "Агентство"
                elif row["agent_status"] == 0:
                    agency = "Собственник"
                else:
                    agency = ""
                text = (
                    f"<b>Адрес:</b> {row['location']}\n"
                    f"<b>Район:</b> {row['district']}\n"
                    f"<b>Цена: {row['price_value']} {row['currancy']} {agency}</b>\n"
                    "<b>О доме:</b>\n"
                    f"\t<b>Тип:</b> {row['type']}\n"
                    f"\t<b>Тип здания:</b> {row['building_type']}\n"
                    f"\t<b>Общая площадь:</b> {row['total_area']} \u33a1\n"
                    f"\t<b>Полощадь участка</b> {row['land_area']} \u33a1\n"
                    f"\t<b>Количество этажей:</b> {row['floors_count']}\n"
                    f"\t<b>Количество комнат:</b> {row['rooms_count']}\n"
                    f"\t<b>Количество санузлов:</b> {row['toilet_count']}\n"
                    f"\t<b>Мебель:</b> {row['furniture']}\n"
                    f"\t<b>Гараж:</b> {normalization_validation.convert_database_boolean(row['garage'])}\n"
                    f"\t<b>Ремонт:</b> {row['appartment_state']}\n"
                    f"\t<b>Удобства:</b> {row['appliances']}\n"
                    "<b>Условия сделки:</b>\n"
                    f"\t<b>Дети:</b> {normalization_validation.convert_database_boolean(row['children_allowed'])}\n"
                    f"\t<b>Животные:</b> {normalization_validation.convert_database_boolean(row['animals_allowed'])}\n"
                    f"\t<b>Коммунальные платежи:</b> {normalization_validation.convert_utility_bills(row['utility_bills_included'])}\n"
                    f"\t<b>Предоплата:</b> {row['prepayment']}\n"
                    f"<b>Описание:</b>\n{row['description']}\n"
                    f"<b>Опубликовано:</b> {normalization_validation.convert_iso_date_str(row['date_posted'])}\n"
                    f"<b>Обновлено:</b> {normalization_validation.convert_iso_date_str(row['date_updated'])}\n"
                    f"<b>https://list.am/ru/item/{row['id']}</b>"
                )
                bot.edit_message_text(
                    text=text,
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode="HTML",
                )
            except (AssertionError, KeyError) as e:
                logger.error(
                    "Callback -> details: Can not get data from database: %s", e
                )
                return None
