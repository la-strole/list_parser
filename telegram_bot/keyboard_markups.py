"""
Markups for bot keybaords
"""

from typing import List

from telebot import types
from telebot.util import quick_markup

import serialization


def create_all_bus_keyboard_markup() -> types.ReplyKeyboardMarkup:
    """
    Develop a custom keyboard interface that includes all available bus numbers.
    """
    # Create a custom keyboard
    markup_all_bus = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Номер транспорта",
    )

    # Define the keyboard buttons 5x10
    keyboard = []
    for bus_key in serialization.get_all_buses_list():
        keyboard.append(
            types.KeyboardButton(serialization.convert_bus_key_to_label(bus_key))
        )

    markup_all_bus.add(*keyboard, row_width=5)

    return markup_all_bus


def create_route_image_markup() -> types.InlineKeyboardMarkup:
    """
    Develop a custom inline keybord interface
    for route image to show stations and reverse route.
    """

    markup = quick_markup(
        {
            "Показать остановки": {"callback_data": f"1"},
            "Показать обратный маршрут": {"callback_data": f"2"},
        },
        row_width=1,
    )

    return markup


def create_route_image_markup_without_reverse_route():
    markup = quick_markup(
        {
            "Показать остановки": {"callback_data": f"1"},
        },
        row_width=1,
    )

    return markup


def show_reverse_route_stations():
    """
    Develop a custom keybord interface that includes buses routes stations
    """
    markup = quick_markup(
        {
            "Показать остановки обратного маршрута": {"callback_data": "3"},
        },
        row_width=1,
    )

    return markup


def multiple_stations_markup(stations_list: list):
    keyboard = []
    for number, name in enumerate(stations_list):
        button = types.InlineKeyboardButton(
            text=name, callback_data="st" + str(number + 1)
        )
        keyboard.append(button)
    markup = types.InlineKeyboardMarkup()
    markup.add(*keyboard, row_width=1)
    return markup
