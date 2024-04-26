"""
Callback data handler
"""
from typing import Dict, List, Optional

from telebot import TeleBot, types

import keyboard_markups
import serialization


def get_route_image(caption: str, reverse_flag: bool) -> Optional[Dict]:
    # Retrieve the current route type.
    if "Обратный" in caption or "обратный" in caption:
        current_route_type = "reverse"
    else:
        current_route_type = "straight"
    # Obtain the bus label.
    bus_label = caption.split(":")[1]
    bus_key = serialization.convert_label_to_bus_key(bus_label)

    if reverse_flag:
        if current_route_type == "straight":
            current_route_type = "reverse"
        else:
            current_route_type = "straight"

    if current_route_type == "straight":
        route_info = serialization.get_bus_straight_route_info(bus_key)
        caption = f"Маршрут:{bus_label}"
    else:
        route_info = serialization.get_bus_reverse_route_info(bus_key)
        caption = f"Обратный маршрут:{bus_label}"

    if route_info:
        result = {
            "filename": route_info["image"],
            "caption": caption,
            "reply_markup": keyboard_markups.create_route_image_markup(),
        }
        return result
    else:
        return None


def get_bus_stations(caption: str, reverse_flag: bool) -> Optional[Dict]:
    # Retrieve the current route type.
    if "Обратный" in caption or "обратный" in caption:
        current_route_type = "reverse"
    else:
        current_route_type = "straight"

    # Obtain the bus label.
    bus_label = caption.split(":")[1]
    bus_key = serialization.convert_label_to_bus_key(bus_label)

    if reverse_flag:
        if current_route_type == "straight":
            current_route_type = "reverse"
        else:
            current_route_type = "straight"

    if current_route_type == "straight":
        route_info = serialization.get_bus_straight_route_info(bus_key)
        caption = f"Маршрут:{bus_label}"
    else:
        route_info = serialization.get_bus_reverse_route_info(bus_key)
        caption = f"Обратный маршрут:{bus_label}"

    if route_info:
        stations_list = route_info["station_list"]

        msg = f"<b>{caption}\n{route_info['route_name']}</b>\n\n"
        for station in stations_list:
            msg += f"{station}\n\n"

        reply_markup = keyboard_markups.show_reverse_route_stations()
        result = {"text": msg, "reply_markup": reply_markup}
        return result
    else:
        return None


def callback_handler(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        # Retrieve the callback data from the button that was clicked.
        callback_data: str = call.data

        # Perform actions based on the callback data

        if callback_data == "1":  # Show the stations on the bus route.
            # Retrieve the caption.
            caption = call.message.caption
            data = get_bus_stations(caption, reverse_flag=False)
            if data:
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text=data["text"],
                    parse_mode="html",
                    disable_notification=True,
                    reply_markup=data["reply_markup"],
                )
            else:
                bot.send_message(
                    call.message.chat.id, "Не удалось найти остановки для маршрута."
                )

        elif callback_data == "2":  # Display the image of the reverse route.
            # Retrieve the caption.
            caption = call.message.caption
            data = get_route_image(caption, reverse_flag=True)
            if data:
                with open(data["filename"], "rb") as file:
                    bot.edit_message_media(
                        media=types.InputMediaPhoto(file, caption=data["caption"]),
                        chat_id=call.message.chat.id,
                        message_id=call.message.id,
                        reply_markup=data["reply_markup"],
                    )
            else:
                bot.send_message(
                    call.message.chat.id, "Не удалось найти обратный маршрут."
                )

        elif callback_data == "3":  # Display the bus stations on the reverse route.
            # Modify the text message with information about the reverse bus stations.
            # Retrieve the current route type.
            caption = call.message.text.split("\n")[0]
            data = get_bus_stations(caption, reverse_flag=True)
            if data:
                # Substitute the message text with new content.
                bot.edit_message_text(
                    text=data["text"],
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    parse_mode="html",
                    reply_markup=data["reply_markup"],
                )
            else:
                bot.send_message(
                    call.message.chat.id,
                    "Не удалось найти остановки для обратного маршрута.",
                )

        elif callback_data.startswith(
            "st"
        ):  # Select a station from among multiple station names.
            user_number = callback_data[2:]
            message_text_with_stations = call.message.text.split("\n")
            station = ""
            for line in message_text_with_stations:
                splitline: List[str] = line.split(".")
                if splitline[0] == user_number:
                    station = splitline[1].strip()
                    break
            if station:
                msg = f"На остановке <b>{station}</b> останавливается транспорт:\n\n"
                station_json_buses = (
                    serialization.get_station_json_bus_list_for_station(station)
                )
                if not station_json_buses:
                    msg = "Не удалось найти транспорт."
                else:
                    for bus in serialization.station_json_bus_sort(station_json_buses):
                        label = serialization.convert_station_json_bus_info_to_label(
                            bus
                        )
                        label_with_thin_bcksps = label.replace(" ", "\u00a0")
                        msg += label_with_thin_bcksps

                bot.send_message(
                    call.message.chat.id,
                    text=msg,
                    disable_notification=True,
                    parse_mode="html",
                )
            else:
                raise ValueError
