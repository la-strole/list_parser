"""
Database routines
"""

import logging
import sqlite3
from datetime import datetime

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


def get_the_last_date_as_isoformat(db_name="database.db") -> str:
    """
    Get the last date from the dataadase in isoformat.
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        date = cur.execute(
            "SELECT date_updated FROM advertisement ORDER BY date_updated DESC LIMIT 1"
        ).fetchone()[0]
        if not date:
            date = cur.execute(
                "SELECT date_posted FROM advertisement ORDER BY date_posted DESC LIMIT 1"
            ).fetchone()[0]
    if not date:
        return datetime(1989, 7, 21, 10, 10).isoformat()
    return date


def populate_database(
    database_row: normalization_validation.DatabaseRow, db_name="database.db"
):
    """
    Populate the database.
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # Check if this id already was in the database.
        row = cur.execute(
            "SELECT * FROM advertisement WHERE id = ?", (database_row.id,)
        ).fetchone()
        if row:
            # Update database row
            con.execute(
                """
                        UPDATE advertisement 
                        SET id = :id, image_href = :image_href, title = :title, price_value = :price_value, 
                        currancy = :currancy, description = :description, 
                        date_posted = :date_posted , date_updated = :date_updated, location = :location, 
                        agent_status = :agent_status, user_link = :user_link, 
                        appliances = :appliences, garage = :garage, rooms_count = :room_count, 
                        toilet_count = :toilet_count, utility_bills_included = :utility_bills_included, 
                        furniture = :furniture, children_allowed = :children_allowed, 
                        animals_allowed = :animals_allowed, total_area = :total_area, land_area = :land_area, 
                        prepayment = :prepayment, appartment_state = :appartment_state, type = :type, 
                        building_type = :building_type, facilities = :facilities, floors_count = :floors_count
                        WHERE id = :id
                        """,
                database_row.model_dump(),
            )
        else:
            # Commit database row
            con.execute(
                """
                        INSERT INTO advertisement 
                        (id, image_href, title, price_value, currancy, description, 
                        date_posted, date_updated, location, agent_status, user_link, 
                        appliances, garage, rooms_count, toilet_count, utility_bills_included, 
                        furniture, children_allowed, animals_allowed, total_area, land_area, 
                        prepayment, appartment_state, type, building_type, facilities, floors_count) 
                        VALUES (:id, :image_href, :title, :price_value, :currancy, :description, 
                        :date_posted, :date_updated, :location, :agent_status, :user_link, :appliances, 
                        :garage, :rooms_count, :toilet_count, :utility_bills_included, :furniture, 
                        :children_allowed, :animals_allowed, :total_area, :land_area, :prepayment, 
                        :appartment_state, :type, :building_type, :facilities, :floors_count)""",
                database_row.model_dump(),
            )
