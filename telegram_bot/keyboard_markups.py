"""
Markups for bot keybaords
"""

from telebot import types
from telebot.util import quick_markup


def send_duplicates() -> types.InlineKeyboardMarkup:
    """
    If send duplicates advertisement with similar id
    """

    markup = quick_markup(
        {
            "Да": {"callback_data": "1"},
            "Нет": {"callback_data": "2"},
        },
        row_width=2,
    )

    return markup


def agent_status() -> types.InlineKeyboardMarkup:
    """
    Set adv from agent or lendlords
    """

    markup = quick_markup(
        {
            "Только собственник": {"callback_data": "3"},
            "Только агентство": {"callback_data": "4"},
            "Не важно": {"callback_data": "5"},
        },
        row_width=2,
    )

    return markup


def garage_option() -> types.InlineKeyboardMarkup:
    """
    Garage existing
    """

    markup = quick_markup(
        {
            "Да": {"callback_data": "6"},
            "Нет": {"callback_data": "7"},
            "Не важно": {"callback_data": "8"},
        },
        row_width=2,
    )

    return markup


def max_price_amd() -> types.InlineKeyboardMarkup:
    """
    Max price undefined
    """

    markup = quick_markup(
        {
            "Не важно": {"callback_data": "9"},
        },
        row_width=1,
    )

    return markup


def room_count() -> types.InlineKeyboardMarkup:
    """
    Room count undefind
    """

    markup = quick_markup(
        {
            "Не важно": {"callback_data": "10"},
        },
        row_width=1,
    )

    return markup


def furniture() -> types.InlineKeyboardMarkup:
    """
    Furniture options
    """

    markup = quick_markup(
        {
            "Есть": {"callback_data": "11"},
            "Нет": {"callback_data": "12"},
            "Частичная мебель": {"callback_data": "13"},
            "По договоренности": {"callback_data": "14"},
            "Не важно": {"callback_data": "15"},
        },
        row_width=2,
    )

    return markup


def children() -> types.InlineKeyboardMarkup:
    """
    Children options
    """

    markup = quick_markup(
        {
            "Да": {"callback_data": "16"},
            "Нет": {"callback_data": "17"},
            "Не важно": {"callback_data": "18"},
        },
        row_width=2,
    )

    return markup


def animals() -> types.InlineKeyboardMarkup:
    """
    Animals options
    """

    markup = quick_markup(
        {
            "Да": {"callback_data": "19"},
            "Нет": {"callback_data": "20"},
            "Не важно": {"callback_data": "21"},
        },
        row_width=2,
    )

    return markup


def total_area() -> types.InlineKeyboardMarkup:
    """
    Total_area options
    """

    markup = quick_markup(
        {
            "Не важно": {"callback_data": "22"},
        },
        row_width=1,
    )

    return markup


def land_area() -> types.InlineKeyboardMarkup:
    """
    Land_area options
    """

    markup = quick_markup(
        {
            "Не важно": {"callback_data": "23"},
        },
        row_width=1,
    )

    return markup


def floors_count() -> types.InlineKeyboardMarkup:
    """
    floors_count options
    """

    markup = quick_markup(
        {
            "Не важно": {"callback_data": "24"},
        },
        row_width=1,
    )

    return markup


def district() -> types.InlineKeyboardMarkup:
    """
    district options
    """

    markup = quick_markup(
        {
            "Ачапняк": {"callback_data": "25"},
            "Арабкир": {"callback_data": "26"},
            "Аван": {"callback_data": "27"},
            "Давидашен": {"callback_data": "28"},
            "Эребуни": {"callback_data": "29"},
            "Зейтун Канакер": {"callback_data": "30"},
            "Кентрон": {"callback_data": "31"},
            "Малатия Себастия": {"callback_data": "32"},
            "Нор Норк": {"callback_data": "33"},
            "Шенгавит": {"callback_data": "34"},
            "Норк Мараш": {"callback_data": "35"},
            "Нубарашен": {"callback_data": "36"},
            "Не важно": {"callback_data": "37"},
        },
        row_width=2,
    )

    return markup
