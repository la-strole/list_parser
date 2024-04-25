"""
Validators and normalization functions
"""

import logging
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl, PositiveInt, field_validator

import logger_config

logger = logging.getLogger(__name__)

valid_keys: dict[str, str] = {
    "agent_status": "agent_status",
    "currancy": "currancy",
    "date_posted": "date_posted",
    "date_updated": "date_updated",
    "description": "description",
    "id": "id",
    "image_href": "image_href",
    "location": "location",
    "price_value": "price_value",
    "title": "title",
    "Бытовая техника": "appliances",
    "Гараж": "garage",
    "Количество комнат": "rooms_count",
    "Количество санузлов": "toilet_count",
    "Коммунальные платежи": "utility_bills_included",
    "Мебель": "furniture",
    "Можно с детьми": "children_allowed",
    "Можно с животными": "animals_allowed",
    "Общая площадь": "total_area",
    "Площадь участка": "land_area",
    "Предоплата": "prepayment",
    "Ремонт": "appartment_state",
    "Тип": "type",
    "Тип здания": "building_type",
    "Удобства": "facilities",
    "Этажей в доме": "floors_count",
}


class DatabaseRow(BaseModel):
    """
    Normalized database row.
    """

    id: PositiveInt
    image_href: str
    title: str
    price_value: PositiveInt
    currancy: Literal["USD", "AMD", "RUB"]  # TODO make currency exchange
    description: str
    date_posted: datetime
    date_updated: datetime | None = None
    location: str
    agent_status: bool
    user_link: str
    appliances: str | None = None
    garage: str | None = None
    rooms_count: str | None = None
    toilet_count: str | None = 1
    utility_bills_included: str | None = None
    furniture: str | None = None
    children_allowed: str | None = None
    animals_allowed: str | None = None
    total_area: str | None = None
    land_area: str | None = None
    prepayment: str | None = None
    appartment_state: str | None = None
    type: str | None = None
    building_type: str | None = None
    facilities: str | None = None
    floors_count: str | None = 1

    @field_validator("image_href", "user_link")
    @classmethod
    def http_validator(cls, value):
        HttpUrl(value)
        return value

    @field_validator("location")
    @classmethod
    def max_len_validator(cls, value):
        assert len(value) < 255
        return value

    @field_validator("garage")
    @classmethod
    def convert_to_boolean(cls, value):
        if value:
            return value != "Нет"

    @field_validator(("rooms_count"))
    @classmethod
    def convert_rooms_count_to_int(cls, value):
        if value:
            try:
                assert int(value) < 8
                return int(value)
            except ValueError:
                return 8

    @field_validator(("toilet_count"))
    @classmethod
    def convert_toilets_count_to_int(cls, value):
        if value:
            try:
                assert int(value) < 3
                return int(value)
            except ValueError:
                return 3

    @field_validator(("utility_bills_included"))
    @classmethod
    def convert_utility_bills_included_to_bool(cls, value):
        if value:
            return value == "Включены"

    @field_validator("children_allowed", "animals_allowed")
    @classmethod
    def convert_children_allowed_to_bool(cls, value):
        if value == "Да":
            return True
        if value == "Нет":
            return False
        return None

    @field_validator("total_area", "land_area")
    @classmethod
    def convert_total_area_to_int(cls, value):
        if value:
            string_list = value.split(" ")
            result = int(string_list[0])
            return result

    @field_validator(("floors_count"))
    @classmethod
    def convert_floors_count_to_int(cls, value):
        if value:
            try:
                assert int(value) < 4
                return int(value)
            except ValueError:
                return 4


# GET parameters
available_parameters = {
    "n": "1",  # ереван, 2 итд Ачапняк Арабкир Аван Давидашен Эребуни Зейтун Канакер Кентрон Малатия Себастия
    # Нор Норк Шенгавит Норк Мараш Нубарашен) disallow by robots.txt
    "cmtype": "",  # 1 (2) - частное/агенство - disallow by robots.txt
    "price1": "",  # цена от disallow by robots.txt
    "price2": "",  # цена до disallow by robots.txt
    "crc": "",  # валюта 0 - драмы, 1 - usd
    "_a3_1": "",  # площадь от
    "_a3_2": "",  # площадь до
    "_a34": "0",  # этажей в доме (1-4)
    "_a4": "0",  # количество комнат (1-8) можно несеолько через %2C
    "_a37": "0",  # количество санузлов (1-3) можно несеолько через %2C
    "_a78": "0",  # мебель (1-есть, 2-нет, 3-частичная, 4-по договоренности) можно несеолько через %2C
    "_a76": "0",  # гараж (1-нет, 2-одно место, 3-два, 4 - три и более)
    "_a38": "0",  # ремонт (1-без, 2-старый, 3-частичный, 4-косметический, 5-евро, 6-дизайнерский, 7-капитальный)
    # можно несеолько через %2C
    "_a83": "0",  # удобства
    "_a75": "0",  # бытовая техника
    "_a35_1": "",  # площадь участка от
    "_a35_2": "",  # площадь участка до
    "_a68": "0",  # можно с детьми (1-нет, 2-да, 3-по договоренности)
    "_a69": "0",  # можно с животными (1-нет, 2-да, 3-по договоренности)
    "gl": "2",  #  1 галерея, 2 - список
}


def convert_date_to_object(date_string: str) -> Optional[str | None]:
    """
    Converts a date string to object
    'Вторник, Апрель 23, 2024 21:42'
    """
    month_dict: dict[str, int] = {
        "Январь": 1,
        "Февраль": 2,
        "Март": 3,
        "Апрель": 4,
        "Май": 5,
        "Июнь": 6,
        "Июль": 7,
        "Август": 8,
        "Сентябрь": 9,
        "Октябрь": 10,
        "Ноябрь": 11,
        "Декабрь": 12,
    }
    try:
        split_date: list[str] = date_string.split(",")
        month_day: list[str] = split_date[1].strip().split(" ")
        month: int = month_dict[month_day[0]]
        day = int(month_day[1])
        year_time: list[str] = split_date[2].strip().split(" ")
        year = int(year_time[0])
        hour = int(year_time[1].split(":")[0])
        minute = int(year_time[1].split(":")[1])
        date_time_object = datetime(year, month, day, hour, minute)
        return date_time_object.isoformat()
    except Exception as e:
        logging.error("Can not convert date from main page to datetime object: %s", e)
        return None
