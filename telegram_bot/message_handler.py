"""
User's message handler
"""

import logging

from pydantic import ValidationError
from telebot import TeleBot, types

import database
import logger_config
import normalization_validation
from telegram_bot import keyboard_markups

logger = logging.getLogger(__name__)


def test_reply(message, parent_start_text):
    """
    Test if message is reply to another message
    """
    try:
        parent = message.reply_to_message
        return parent.text.startswith(parent_start_text)
    except AttributeError:
        return False


def message_handler(bot: TeleBot):

    # Set price_value_amd
    @bot.message_handler(func=lambda msg: test_reply(msg, "Максимальная цена в AMD"))
    def set_max_price(message: types.Message):
        try:
            user_id = normalization_validation.TlgUserId.model_validate(
                {"user_id": message.from_user.id}
            ).user_id
            option_name = (
                normalization_validation.TlgBotUserFilterOption.model_validate(
                    {"option_name": "price_value_amd"}
                ).option_name
            )
            option_value = normalization_validation.MaxPriceAMD.model_validate(
                {"option": message.text}
            ).option

        except ValidationError as e:
            logger.error("message_handler -> error: %s", e)
            bot.send_message(
                message.chat.id,
                text="Ошибка в сумме. Попробуйте отправить Reply еще раз",
                disable_notification=True,
                parse_mode="html",
            )
            return None
        database.change_telegram_user_filtres_options(
            user_id, option_name, option_value
        )

        # Set agent_status
        msg = "<b>Объявления от собственников или агентств (3 из 12)</b>"
        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
            reply_markup=keyboard_markups.agent_status(),
        )

    # Set room counts
    @bot.message_handler(func=lambda msg: test_reply(msg, "Количество комнат"))
    def set_room_count(message: types.Message):
        try:
            user_id = normalization_validation.TlgUserId.model_validate(
                {"user_id": message.from_user.id}
            ).user_id
            option_name = (
                normalization_validation.TlgBotUserFilterOption.model_validate(
                    {"option_name": "rooms_count"}
                ).option_name
            )
            option_value = normalization_validation.RoomCount.model_validate(
                {"option": message.text}
            ).option

        except ValidationError as e:
            logger.error("message_handler -> error: %s", e)
            bot.send_message(
                message.chat.id,
                text="Ошибка в количестве комнат. Попробуйте отправить Reply еще раз",
                disable_notification=True,
                parse_mode="html",
            )
            return None
        database.change_telegram_user_filtres_options(
            user_id, option_name, option_value
        )

        # furniture option
        msg = "<b>Наличие мебели (6 из 12)</b>"
        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
            reply_markup=keyboard_markups.furniture(),
        )

    # Set total_area
    @bot.message_handler(func=lambda msg: test_reply(msg, "Общая площадь"))
    def set_total_area(message: types.Message):
        try:
            user_id = normalization_validation.TlgUserId.model_validate(
                {"user_id": message.from_user.id}
            ).user_id
            option_name = (
                normalization_validation.TlgBotUserFilterOption.model_validate(
                    {"option_name": "total_area"}
                ).option_name
            )
            option_value = normalization_validation.Area.model_validate(
                {"option": message.text}
            ).option

        except ValidationError as e:
            logger.error("message_handler -> error: %s", e)
            bot.send_message(
                message.chat.id,
                text="Ошибка общей площади. Попробуйте отправить Reply еще раз",
                disable_notification=True,
                parse_mode="html",
            )
            return None
        database.change_telegram_user_filtres_options(
            user_id, option_name, option_value
        )

        # land_area option
        msg = "<b>Площадь участка. ОТ Ответ в Reply (10 из 12)</b>"
        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
            reply_markup=keyboard_markups.land_area(),
        )

    # Set Land area
    @bot.message_handler(func=lambda msg: test_reply(msg, "Площадь участка"))
    def set_land_area(message: types.Message):
        try:
            user_id = normalization_validation.TlgUserId.model_validate(
                {"user_id": message.from_user.id}
            ).user_id
            option_name = (
                normalization_validation.TlgBotUserFilterOption.model_validate(
                    {"option_name": "land_area"}
                ).option_name
            )
            option_value = normalization_validation.Area.model_validate(
                {"option": message.text}
            ).option

        except ValidationError as e:
            logger.error("message_handler -> error: %s", e)
            bot.send_message(
                message.chat.id,
                text="Ошибка в площади участка. Попробуйте отправить Reply еще раз",
                disable_notification=True,
                parse_mode="html",
            )
            return None
        database.change_telegram_user_filtres_options(
            user_id, option_name, option_value
        )

        # floors_count option
        msg = "<b>Количество этажей. (1-4) Ответ в Reply (11 из 12)</b>"
        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
            reply_markup=keyboard_markups.floors_count(),
        )

    # Set floors_count
    @bot.message_handler(func=lambda msg: test_reply(msg, "Количество этажей"))
    def set_floors_count(message: types.Message):
        try:
            user_id = normalization_validation.TlgUserId.model_validate(
                {"user_id": message.from_user.id}
            ).user_id
            option_name = (
                normalization_validation.TlgBotUserFilterOption.model_validate(
                    {"option_name": "floors_count"}
                ).option_name
            )
            option_value = normalization_validation.FloorsCount.model_validate(
                {"option": message.text}
            ).option

        except ValidationError as e:
            logger.error("message_handler -> error: %s", e)
            bot.send_message(
                message.chat.id,
                text="Ошибка в количестве этажей. Попробуйте отправить Reply еще раз",
                disable_notification=True,
                parse_mode="html",
            )
            return None
        database.change_telegram_user_filtres_options(
            user_id, option_name, option_value
        )

        # district option
        msg = "<b>Выберите район. (12 из 12)</b>"
        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
            reply_markup=keyboard_markups.district(),
        )

    @bot.message_handler(func=lambda msg: True)
    def default_message(message):
        """
        Default message
        """
        msg = (
            "<b>Внимание!</b>\n"
            "Бот не предусматривает ответов на сообщения. "
            "Настройки делаются через REPLY к соответствующим сообщениям"
        )
        bot.send_message(
            message.chat.id,
            text=msg,
            disable_notification=True,
            parse_mode="HTML",
        )


def send_adv_message(bot: TeleBot, chat_id: int, row_dict) -> None:
    """
    Send adv for user
    """
    bot.send_photo(
        chat_id=chat_id,
        photo=row_dict["image_href"],
        disable_notification=True,
        parse_mode="HTML",
    )
    bot.send_message(
        chat_id=chat_id,
        text=f"<b>{row_dict['title']}</b>\n{row_dict['price_value']} {row_dict['currancy']}\nhttps://list.am/ru/item/{row_dict['id']}",
        disable_notification=True,
        parse_mode="HTML",
        reply_markup=keyboard_markups.details(),
    )
