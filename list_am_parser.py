"""
List am parser to populate database.
"""

import logging
import random
import re
import time
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

import database
import logger_config
import normalization_validation

logger = logging.getLogger(__name__)

# URL for list.am page.
URL = "https://www.list.am/ru/category/63"

# Fake headers.
headers = {
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
    logger.debug("Frozen with sleep time")
    time.sleep(random.randint(1, 5))
    # Get page.
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
            logger.info("item_tags count = %s", len(item_tags))

            item_page_list = []
            for ad in item_tags:
                date_updated = normalization_validation.convert_date_to_object(
                    str(ad.find(class_="d").string)
                )
                assert (
                    date_updated
                ), "get_links_and_dates_for_single_page: Error with date updated parsing."
                if date_updated > latest_db_date:
                    item_page_list.append(
                        {
                            "id": ad["href"].split("/")[-1],
                            "href": f"https://list.am{ad['href']}",
                            "date_update": date_updated,
                        }
                    )

            logger.debug(
                "get_links_and_dates_for_items returns Advertisment list = %s",
                item_page_list,
            )

            return (
                item_page_list,
                (len(item_page_list) == len(item_tags)),
                response.request.url,
            )

        except (TypeError, AssertionError, KeyError) as e:
            logger.error("Get links of houses error %s", e)
            return None
    else:
        logger.error("Response status code = %s", response.status_code)
        return None


def get_candidates_hrefs(
    session: requests.Session, get_params: Dict[str, str]
) -> list | None:
    """
    Collect candidate hrefs with date_update larger than latest db date.
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
            assert (
                result
            ), f"get_candidates_hrefs: get_links_and_dates_for_items returns None. url = {url}"
            items_list = result[0]
            # Extend candidate list.
            candidate_list.extend(items_list)
            # If all items from the page added to candidate list - go to the next page.
            if result[1]:
                page_number += 1
                referer_header = result[2]
                url = f"{URL}/{page_number}"
            else:
                break

    except AssertionError as e:
        logger.error("get_candidates_hrefs: %s", e)
        return None

    logger.debug("get_candidates_hrefs returns %s", candidate_list)
    return candidate_list


def get_info_for_each_item(session: requests.Session, links_list: list) -> list | None:
    """
    Populate list for every item from item page from candiate list.
    """
    result = []
    # Navigate to the item in links list.
    for link in links_list:
        # Add random pause before requesting.
        logger.debug("Frozen with sleep time")
        time.sleep(random.randint(1, 15))
        response = session.get(
            url=link,
            headers={"Referer": URL},
        )
        try:
            assert (
                response.status_code == 200
            ), f"Link details ({link}) request error: status code {response.status_code}"

            house_info_dict = {}

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
            assert len(footer_span_tags) >= 2, "footer_span_tags len is not 3"
            house_info_dict["id"] = str(footer_span_tags[0].string).rsplit(
                " ", maxsplit=1
            )[-1]
            house_info_dict["date_posted"] = footer_span_tags[1]["content"]
            if len(footer_span_tags) > 2:
                date_updated_string = str(footer_span_tags[2].string).split(" ")
                date_updated = normalization_validation.second_convert_date_to_object(
                    f"{date_updated_string[-2]} {date_updated_string[-1]}"
                )
                assert (
                    date_updated
                ), "Can not normalize date updated from get_info_for_each_item()"
                house_info_dict["date_updated"] = date_updated
            house_info_dict["location"] = str(
                house_info.find(class_="loc").find("a").string
            )
            house_info_dict["agent_status"] = "Агентство" in response.text
            house_info_dict["user_link"] = (
                "https://list.am"
                + soup.find(id="uinfo").find(href=re.compile(r"/user/\d+"))["href"]
            )

            # Normalize the house_info_dict
            house_info_dict = {
                normalization_validation.valid_keys[k]: v
                for k, v in house_info_dict.items()
            }
            result.append(house_info_dict)

        except (AssertionError, TypeError, KeyError) as e:
            logger.error("Get house info error %s", e)
            break
    else:
        logger.debug("get_info_for_each_item returns %s", result)
        return result


def list_am_scrapper(get_params: Dict[str, str]):
    """
    Scarper for list.am web site.
    """
    try:
        # Validate GET parameters.
        for key in get_params:
            assert (
                key in normalization_validation.available_parameters
            ), "Invalid GET parameters"

        # Session for saving cookies.
        with requests.Session() as session:

            # Update headers with fake headers.
            session.headers.update(headers)
            logger.debug("Update html headers with fake headers")

            # Get candidates list to go to the each item link.
            candidate_list = get_candidates_hrefs(session, get_params)
            assert (
                candidate_list
            ), "list_am_scrapper: candidate_list is empty. get_candidates_hrefs returns None"

            # Get candidates list properties to add to the database.
            database_rows = get_info_for_each_item(
                session, [i["href"] for i in candidate_list]
            )
            assert (
                database_rows
            ), "list_am_scrapper: Database rows are empty. get_info_for_each_item returns None"

            # Write info to the database.

    except AssertionError as e:
        logger.error("list_am_scrapper error: %s", e)
        return None
