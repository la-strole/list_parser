"""
List am parser to populate database.
"""

import logging
import random
import re
import time
from typing import Dict, List, Literal, Tuple

import requests
from bs4 import BeautifulSoup
from pydantic import ValidationError

import database
import logger_config
import normalization_validation
from telegram_bot import message_handler

logger = logging.getLogger(__name__)

# URL for list.am page.
URL = "https://www.list.am/ru/category/63"

# Fake headers.
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "www.list.am",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
}


def get_links_and_dates_for_items(
    session: requests.Session,
    get_params: Dict[str, str],
    latest_db_date: str,
    url=URL,
    referer_header="",
) -> Tuple[List[Dict[str, str]], bool, str] | None:
    """
    Get the list of items from list.am and add it to the final list
    if date updated is later than db_last_date.
    Returns tuple: list of dictionaries like {id, href, date_update}
    and if all page items are added (booblean) and request url to use as Referer header
    date_update is isoformat string.
    """
    # Add random delay.

    time_sleep = random.randint(1, 50)
    logger.debug(
        "list_am_parser.py -> get_links_and_dates_for_items: Frozen with sleep time: %s",
        time_sleep,
    )
    time.sleep(time_sleep)

    # Get page and set referer header
    if referer_header:
        response = session.get(
            url, params=get_params, headers={"Referer": referer_header}
        )
    else:
        response = session.get(url, params=get_params)

    if response.status_code == 200:

        try:
            # Make soup.
            soup = BeautifulSoup(response.text, "lxml")

            # Find regular advertisement.
            regular_advertisement_tag = soup.findAll(class_="dl")[1]

            item_tags = regular_advertisement_tag.findAll(
                href=re.compile(r"/ru/item/\d+")
            )
            assert len(item_tags) > 0, "Links tags found error"
            logger.debug(
                "list_am_parser.py -> get_links_and_dates_for_items: item_tags count = %s",
                len(item_tags),
            )

            item_page_list = []
            for ad in item_tags:
                date_updated = normalization_validation.convert_date_to_object(
                    str(ad.find(class_="d").string)
                )
                assert date_updated, "Error with date updated parsing."
                if date_updated > latest_db_date:
                    try:
                        district = str(object=ad.find(class_="at").string).split(",")[0]
                    except Exception as e:
                        logger.warning("Can not find district %s.", e)
                        district = None
                    item_page_list.append(
                        {
                            "id": ad["href"].split("/")[-1],
                            "href": f"https://list.am{ad['href']}",
                            "date_update": date_updated,
                            "district": district,
                        }
                    )

            logger.debug(
                "list_am_parser.py -> get_links_and_dates_for_items: returns Advertisment list= %s",
                item_page_list,
            )
            logger.debug(
                "list_am_parser.py -> get_links_and_dates_for_items: Advertisment count = %s",
                len(item_page_list),
            )

            return (
                item_page_list,
                (len(item_page_list) == len(item_tags)),
                response.request.url,
            )

        except (TypeError, AssertionError, KeyError, IndexError) as e:
            logger.error(
                "list_am_parser.py -> get_links_and_dates_for_items: error %s", e
            )
            return None
    else:
        logger.error(
            "list_am_parser.py -> get_links_and_dates_for_items: Response status code = %s",
            response.status_code,
        )
        return None


def get_candidates_hrefs(
    session: requests.Session, get_params: Dict[str, str]
) -> Tuple[List[dict], str] | None:
    """
    Collect candidate hrefs with date_update larger than latest db date.
    Returns list of candidate hrefs and latest db date.
    """

    candidate_list = []

    # Find the latest db date
    latest_db_date: str = database.get_the_last_date_as_isoformat()

    page_number = 1
    referer_header = ""
    url = URL
    try:
        while True:
            # Get items from the page.
            result = get_links_and_dates_for_items(
                session, get_params, latest_db_date, url, referer_header
            )
            assert result, (
                "list_am_parser.py -> get_candidates_hrefs: "
                f"get_links_and_dates_for_items returns None. url = {url}/{get_params}"
            )

            items_list = result[0]
            # Extend candidate list.

            if (
                items_list and items_list[0] in candidate_list
            ):  # Redirection to the first page from more than last page.
                logger.debug(
                    "list_am_parser.py -> get_candidates_hrefs: "
                    "Redirection to the first page from more than last page."
                )
                break

            candidate_list.extend(items_list)

            # If all items from the page added to candidate list - go to the next page.
            if result[1]:
                page_number += 1
                referer_header = result[2]
                url = f"{URL}/{page_number}"
            else:
                break

    except AssertionError as e:
        logger.error("list_am_parser.py -> get_candidates_hrefs: %s", e)
        return None

    logger.debug(
        "list_am_parser.py -> get_candidates_hrefs: returns %s", candidate_list
    )
    return (candidate_list, latest_db_date)


def get_info_for_each_item(
    session: requests.Session, links_list: List[Tuple]
) -> list | None:
    """
    Populate list for every item from item page from candiate list.
    Add it to the database.
    """

    # Navigate to the item in links list.
    for link in links_list:
        # Add random pause before requesting.
        time_sleep = random.randint(1, 50)
        logger.debug(
            "list_am_parser.py -> get_info_for_each_item: Frozen with sleep time: %s",
            time_sleep,
        )
        time.sleep(time_sleep)

        response = session.get(
            url=link[0],
            headers={"Referer": URL},
        )
        try:
            assert response.status_code in (
                200,
                404,
            ), (
                "list_am_parser.py -> get_info_for_each_item: "
                f"Link details ({link}) request error: status code {response.status_code}"
            )

            if response.status_code == 404:
                continue

            house_info_dict = {"district": link[1]}

            # Make soup.
            soup = BeautifulSoup(response.text, "lxml")

            house_info = soup.find(id="pcontent")

            house_info_dict["image_href"] = (
                f"https:{house_info.find(class_='pv').find('img')['src']}"
            )
            house_info_dict["title"] = str(
                house_info.find(class_="vih").find("h1").string
            )
            price_tag = house_info.find(class_="vih").find("span", class_="price")
            house_info_dict["price_value"] = price_tag["content"]
            house_info_dict["currancy"] = price_tag.find("meta")["content"]

            group_about_tags = house_info.find(class_="vi").findAll(class_="attr")
            for group in group_about_tags:
                columns = group.findAll(class_="c")
                for item in columns:
                    house_info_dict[str(item.find(class_="t").string)] = str(
                        item.find(class_="i").string
                    )

            house_info_dict["description"] = " ".join(
                house_info.find(class_="vi").find(class_="body").stripped_strings
            )
            footer_span_tags = (
                house_info.find(class_="vi").find(class_="footer").findAll("span")
            )
            assert (
                len(footer_span_tags) >= 2
            ), "list_am_parser.py -> get_info_for_each_item: footer_span_tags len < 2"
            house_info_dict["id"] = str(footer_span_tags[0].string).rsplit(
                " ", maxsplit=1
            )[-1]
            house_info_dict["date_posted"] = footer_span_tags[1]["content"]
            if len(footer_span_tags) > 2:
                date_updated_string = str(footer_span_tags[2].string).split(" ")
                date_updated = normalization_validation.second_convert_date_to_object(
                    f"{date_updated_string[-2]} {date_updated_string[-1]}"
                )
                assert date_updated, (
                    "list_am_parser.py -> get_info_for_each_item: "
                    "Can not normalize date updated from get_info_for_each_item()"
                )
                house_info_dict["date_updated"] = date_updated
            house_info_dict["location"] = str(
                house_info.find(class_="loc").find("a").string
            )
            house_info_dict["agent_status"] = "Агентство" in response.text
            try:
                house_info_dict["user_link"] = (
                    "https://list.am"
                    + soup.find(id="uinfo").find(href=re.compile(r"/user/\d+"))["href"]
                )
            except Exception as e:
                logger.warning(
                    "list_am_parser.py -> get_info_for_each_item: "
                    "Can not parse user link %s",
                    e,
                )
                house_info_dict["user_link"] = "https://example.com"

            # Normalize the house_info_dict
            house_info_dict = {
                normalization_validation.valid_keys[k]: v
                for k, v in house_info_dict.items()
            }
            # Simple Currency exchange
            if house_info_dict["currancy"] == "AMD":
                house_info_dict["price_amd"] = int(house_info_dict["price_value"])
            elif house_info_dict["currancy"] == "USD":
                house_info_dict["price_amd"] = int(house_info_dict["price_value"]) * 398
            elif house_info_dict["currancy"] == "RUB":
                house_info_dict["price_amd"] = int(house_info_dict["price_value"]) * 4
            # Validate the row and add it to the database.
            try:
                clear_row = normalization_validation.DatabaseRow.model_validate(
                    house_info_dict
                )
            except ValidationError as e:
                logger.error(
                    (
                        "list_am_parser.py -> get_info_for_each_item: "
                        "Item %s Validate the row error: %s"
                    ),
                    house_info_dict[id],
                    e,
                )
                return None
            else:
                # Populate database
                database.populate_database(clear_row)
                logger.debug(
                    "list_am_parser.py -> get_info_for_each_item: item %s added to the database",
                    house_info_dict["id"],
                )

        except (AssertionError, TypeError, KeyError) as e:
            logger.error(
                "list_am_parser.py -> get_info_for_each_item: Get house info error %s",
                e,
            )
            return None

    return 1


def send_tlg_msg_to_user(user_id, latest_date, bot) -> None | Literal[0] | Literal[1]:
    """
    Send a message to the user
    """
    try:
        adv_list = database.get_adv_for_user(user_id, latest_date)
        assert (
            adv_list is not None
        ), f"list_am_parser.py -> send_tlg_msg_to_user: get_adv_for_user {user_id} returns None"
        if not adv_list:
            logger.debug(
                "list_am_parser.py -> send_tlg_msg_to_user: No adv for user %s", user_id
            )
            return 0
        # get chat id
        chat_id = database.get_chat_id_for_user(user_id)
        assert (
            chat_id
        ), f"list_am_parser.py -> send_tlg_msg_to_user Can not get chat id for user {user_id}"
        # Send tlg message
        for row in adv_list:
            # Test if send tlg message
            test_send = database.test_send_if_duplicate_item_id(user_id, row["id"])
            assert test_send is not None, (
                "list_am_parser.py -> send_tlg_msg_to_user: "
                "test_send_if_duplicate_item_id returns None, "
                f"user_id={user_id}, item_id={row['id']}"
            )
            if test_send:
                message_handler.send_adv_message(bot, chat_id, row)
                logger.debug(
                    "list_am_parser.py -> send_tlg_msg_to_user: Send message to user %s",
                    user_id,
                )
                # Add id as sent
                result = database.add_item_id_as_sent_for_user(user_id, row["id"])
                assert result, (
                    "list_am_parser.py -> send_tlg_msg_to_user: "
                    "add_item_id_as_sent_for_user return None"
                )
        return 1

    except AssertionError as e:
        logger.error("list_am_parser.py -> send_tlg_msg_to_user: error: %s", e)
        return None


def list_am_scrapper(bot, get_params: Dict[str, str] | None = None):
    """
    Scarper for list.am web site.
    """
    try:
        # Validate GET parameters.
        if get_params:
            for key in get_params:
                assert (
                    key in normalization_validation.available_parameters
                ), "Invalid GET parameters"
        else:
            get_params = {}

        # Session for saving cookies.
        with requests.Session() as session:

            # Update headers with fake headers.
            session.headers.update(HEADERS)
            logger.debug(
                "list_am_parser.py -> list_am_scrapper: Update html headers with fake headers"
            )

            # Get candidates list to visit each item page.
            candidate_list = get_candidates_hrefs(session, get_params)
            assert candidate_list and len(candidate_list) == 2, (
                "list_am_parser.py -> list_am_scrapper: "
                "candidate_list is empty. get_candidates_hrefs returns None"
            )

            # Add info from candidates list properties to the database.
            result = get_info_for_each_item(
                session, [(i["href"], i["district"]) for i in candidate_list[0]]
            )
            assert result, (
                "list_am_parser.py -> list_am_scrapper: "
                "Can not add all candiadates to the database "
                "get_info_for_each_item returns None"
            )

            # Get users list
            users = database.get_users_list()
            assert (
                users
            ), "list_am_parser.py -> list_am_scrapper: get users list is empty"

            # Latest date in the database
            latest_date = candidate_list[1]

            # For user from list get adv
            for user_id in users:
                result = send_tlg_msg_to_user(user_id, latest_date, bot)
                if result is None:
                    raise AssertionError("send_tlg_msg_to_user returns None")

        return 1

    except AssertionError as e:
        logger.error("list_am_parser.py -> list_am_scrapper: error: %s", e)
        return None


"""
if __name__ == "__main__":
    from main import bot

    # Get only this adv from list.am
    GET_PARAMS = {
        "n": "1",  # ереван
        "price2": "500000",  # цена до disallow by robots.txt
        "crc": "0",  # валюта 0 - драмы, 1 - usd
        "_a3_1": "80",  # площадь от
        "gl": "2",  #  1 галерея, 2 - список
    }
    list_am_scrapper(bot, GET_PARAMS)
"""
