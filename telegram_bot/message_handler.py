"""
User's message handler
"""
from telebot import TeleBot, types

import keyboard_markups
import serialization


def message_handler(bot: TeleBot):
    @bot.message_handler(
        func=lambda msg: msg.text.startswith(serialization.BUS_ICON)
        or msg.text.startswith(serialization.TROLLEY_ICON)
    )
    def send_route_image(message: types.Message):
        assert message.text  # To avoid messages without text.
        bus_label = message.text
        bus_key = serialization.convert_label_to_bus_key(bus_label)
        route_info = serialization.get_bus_straight_route_info(bus_key)
        reversed_route_info = serialization.get_bus_reverse_route_info(bus_key)
        if route_info and reversed_route_info:
            with open(route_info["image"], "rb") as file:
                bot.send_photo(
                    message.chat.id,
                    photo=file,
                    caption=f"Маршрут:{bus_label}",
                    disable_notification=True,
                    reply_markup=keyboard_markups.create_route_image_markup()
                    if reversed_route_info["station_list"]
                    else keyboard_markups.create_route_image_markup_without_reverse_route(),
                )
        else:
            bot.send_message(
                message.chat.id, "Не удалось найти маршрут для транспорта."
            )

    @bot.message_handler(func=lambda msg: True)
    def send_bus_station_transport(message):
        # Attempt to locate the bus station name within the JSON object.
        possible_results = []
        user_text = message.text.upper()

        for station in serialization.get_all_stations_list():
            if user_text in station:
                possible_results.append(station)

        # If unable to find anything, return a message.
        if not possible_results:
            bot.reply_to(message, "Увы, не удалось найти такой остановки.")

        elif len(possible_results) == 1:
            station = possible_results[0]
            msg = f"На остановке <b>{station}</b> останавливается транспорт:\n\n"
            station_json_buses = serialization.get_station_json_bus_list_for_station(
                station
            )
            if not station_json_buses:
                msg = "Не удалось найти транспорт."
            else:
                for bus in serialization.station_json_bus_sort(station_json_buses):
                    label = serialization.convert_station_json_bus_info_to_label(bus)
                    label_with_thin_bcksps = label.replace(" ", "\u00a0")
                    msg += label_with_thin_bcksps

            bot.send_message(
                message.chat.id, text=msg, disable_notification=True, parse_mode="html"
            )

        elif len(possible_results) > 1:
            # Select a station.
            msg = "<b>Выберите остановку:</b>\n"
            for number, name in enumerate(possible_results):
                msg += f"{number+1}. {name}\n"
            bot.send_message(
                message.chat.id,
                text=msg,
                disable_notification=True,
                parse_mode="html",
                reply_markup=keyboard_markups.multiple_stations_markup(
                    possible_results
                ),
            )
