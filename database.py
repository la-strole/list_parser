"""
Database routines
"""

import logging
import sqlite3
from datetime import datetime
from typing import List

import logger_config
import normalization_validation

logger = logging.getLogger(__name__)


def create_database(db_name="database.db") -> None:
    """
    Create the new database
    """
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        with open("schema.sql", encoding="utf-8") as fp:
            cur.executescript(fp.read())
    logger.info("New database created")


def get_the_last_date_as_isoformat(db_name="database.db") -> str:
    """
    Get the last date from the dataadase in isoformat.
    """
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        date = cur.execute(
            "SELECT date_updated FROM advertisement ORDER BY date_updated DESC LIMIT 1"
        ).fetchone()[0]
        if not date:
            date = cur.execute(
                "SELECT date_posted FROM advertisement ORDER BY date_posted DESC LIMIT 1"
            ).fetchone()[0]
    except TypeError:
        logger.debug("Database don't have date.")
        return datetime(2024, 4, 25, 0, 0).isoformat()
    else:
        logger.debug("Get latest date from database: %s", date)
        return date
    finally:
        con.close()


def populate_database(
    database_row: normalization_validation.DatabaseRow, db_name="database.db"
):
    """
    Populate the database.
    """

    try:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # Check if this id already was in the database.
        row = cur.execute(
            "SELECT * FROM advertisement WHERE id = ?", (database_row.id,)
        ).fetchone()

        if row:
            # Update database row
            cur.execute(
                """
                UPDATE advertisement 
                SET id = :id, image_href = :image_href, title = :title, price_value = :price_value, 
                currancy = :currancy, description = :description, 
                date_posted = :date_posted , date_updated = :date_updated, location = :location, 
                agent_status = :agent_status, user_link = :user_link, 
                appliances = :appliances, garage = :garage, rooms_count = :rooms_count, 
                toilet_count = :toilet_count, utility_bills_included = :utility_bills_included, 
                furniture = :furniture, children_allowed = :children_allowed, 
                animals_allowed = :animals_allowed, total_area = :total_area, land_area = :land_area, 
                prepayment = :prepayment, appartment_state = :appartment_state, type = :type, 
                building_type = :building_type, facilities = :facilities, floors_count = :floors_count,
                district = :district, price_amd = :price_amd
                WHERE id = :id
                """,
                database_row.model_dump(),
            )
            con.commit()
            logger.debug("Update database row")
            return 1

        # Insert database row
        cur.execute(
            """
                    INSERT INTO advertisement 
                    (id, image_href, title, price_value, currancy, description, 
                    date_posted, date_updated, location, agent_status, user_link, 
                    appliances, garage, rooms_count, toilet_count, utility_bills_included, 
                    furniture, children_allowed, animals_allowed, total_area, land_area, 
                    prepayment, appartment_state, type, building_type, facilities, floors_count, district, price_amd) 
                    VALUES (:id, :image_href, :title, :price_value, :currancy, :description, 
                    :date_posted, :date_updated, :location, :agent_status, :user_link, :appliances, 
                    :garage, :rooms_count, :toilet_count, :utility_bills_included, :furniture, 
                    :children_allowed, :animals_allowed, :total_area, :land_area, :prepayment, 
                    :appartment_state, :type, :building_type, :facilities, :floors_count, :district, :price_amd)""",
            database_row.model_dump(),
        )
        con.commit()
        logger.debug("Insert row to database")
        return 1

    except sqlite3.Error as e:
        logger.error("database.py error: %s", e)
        return None
    finally:
        con.close()


def add_tlg_user_to_database(user_id, chat_id, db_name="database.db"):
    """
    Add a user to the database
    """
    # Check if user already exists
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Check if this id already was in the database.
        row = cur.execute(
            "SELECT * FROM telegram_user_filtres WHERE user_id = ?", (user_id,)
        )

        if not row.fetchone():
            cur.execute(
                """
                        INSERT INTO telegram_user_filtres
                        (user_id, chat_id) VALUES (?)
                        """,
                (user_id, chat_id),
            )
            logger.debug("Add new tlg user to the database")

        else:
            cur.execute(
                """
                    UPDATE telegram_user_filtres 
                    SET chat_id = ? 
                    WHERE user_id = ?
                    """,
                (chat_id, user_id),
            )
            logger.debug("Change chat_id for existed user")

        con.commit()
        return 1
    except sqlite3.Error as e:
        logger.error("database.py add_tlg_user_to_database error: %s", e)
        return None
    finally:
        con.close()


def change_telegram_user_filtres_options(
    user_id, option_name, option_value, db_name="database.db"
):
    """
    Change send_duplicates option
    """
    # Check if user already exists
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # Check if this id already was in the database.
        cur.execute(
            f"UPDATE telegram_user_filtres SET {option_name} = ? WHERE user_id = ?",
            (option_value, user_id),
        )
        con.commit()
        logger.debug("Change %s in the database", option_name)
        return 1
    except sqlite3.Error as e:
        logger.error("database.py add_tlg_user_to_database error: %s", e)
        return None
    finally:
        con.close()


def get_adv_for_user(
    user_id, last_date, db_name="database.db"
) -> List[dict[str, str]] | None:
    """
    Get result from the database with users filters.
    """
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Get user params from database
        par = dict(
            cur.execute(
                "SELECT * FROM telegram_user_filtres WHERE user_id = ?", (user_id,)
            ).fetchone()
        )

        base_sql = f"""
        SELECT * FROM advertisement 
        WHERE (date_updated > '{last_date}' OR date_posted > '{last_date}')
        """

        if par["price_value_amd"] is not None:
            base_sql += f" AND price_amd <= {par['price_value_amd']}"
        if par["agent_status"] is not None:
            base_sql += f" AND agent_status = {par['agent_status']}"
        if par["garage"] is not None:
            base_sql += " AND garage"
        if par["rooms_count"] is not None:
            base_sql += f" AND rooms_count = {par['rooms_count']}"
        if par["furniture"] is not None:
            base_sql += f" AND furniture = '{par['furniture']}'"
        if par["children_allowed"] is not None:
            base_sql += " AND children_allowed"
        if par["animals_allowed"] is not None:
            base_sql += " AND animals_allowed"
        if par["total_area"] is not None:
            base_sql += f" AND total_area >= {par['total_area']}"
        if par["land_area"] is not None:
            base_sql += f" AND land_area >= {par['land_area']}"
        if par["floors_count"] is not None:
            base_sql += f" AND floors_count = {par['floors_count']}"
        if par["district"] is not None:
            base_sql += f" AND district = '{par['district']}'"

        result = cur.execute(
            f"{base_sql} ORDER BY MAX(date_updated, date_posted)"
        ).fetchall()

        if result:
            logger.debug("databse: create_user_sql_query -> returns result: %s", result)
            return [dict(row) for row in result]
        logger.debug("database: create_user_sql_query -> returns empty list")
        return []

    except (sqlite3.Error, AssertionError, TypeError) as e:
        logger.error("database error -> create_sql_query error : %s", e)
        return None

    finally:
        con.close()


def get_item_info(item_id, db_name="database.db"):
    """
    Returns information about item from the database
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        result = cur.execute(
            """
        SELECT * FROM advertisement 
        WHERE id = ?
        """,
            (item_id,),
        )
        result = result.fetchall()
        print("1: result = %s", result)
        print("2: result type = %s", type(result))
    return result[0]


def get_chat_id_for_user(user, db_name="database.db"):
    """
    Returns chat id for user
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    con.row_factory = sqlite3.Row
    try:
        result = cur.execute(
            "SELECT chat_id FROM telegram_user_filtres WHERE user_id = ?", (user,)
        )
        return result.fetchone()[0]
    except sqlite3.Error as e:
        logger.error("database: Can not get chat id for user %s", e)
        return None


def get_users_list(db_name="database.db"):
    with sqlite3.connect(db_name) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute("SELECT user_id FROM telegram_user_filtres").fetchall()
        if result:
            return [row["user_id"] for row in result]
        return None


def add_item_id_as_sent_for_user(user_id, item_id, db_name="database.db"):
    with sqlite3.connect(db_name) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO sent_adv (adv_id, tlg_user_id) VALUES(?, ?)",
                (item_id, user_id),
            )
            con.commit()
            logger.debug("database -> add_item_id_as_sent_for_user error Added")
            return 1
        except sqlite3.Error as e:
            logger.error("database -> add_item_id_as_sent_for_user error: %s", e)
            return None


def test_send_if_duplicate_item_id(user_id, item_id, db_name="database.db"):
    with sqlite3.connect(db_name) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            # Test if user want to duplicate items
            result = cur.execute(
                "SELECT send_duplicates FROM telegram_user_filtres WHERE user_id = ?",
                (user_id,),
            ).fetchone()[0]
            if result == 1:
                return True
            # Test if adv is already sent to this user
            result = cur.execute(
                "SELECT * FROM sent_adv WHERE adv_id = ? AND tlg_user_id = ?",
                (item_id, user_id),
            ).fetchone()
            if result:
                return False
            return True

        except sqlite3.Error as e:
            logger.error("database -> add_item_id_as_sent_for_user error: %s", e)
            return None
