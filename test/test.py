"""
Tests
"""

import sqlite3

import pytest
from telebot import TeleBot, apihelper, util

import database

# Test changing tlg user filters

# Test getting adv with specific filters

# Test changing send item id table and is is working for specuific user filter


@pytest.fixture
def setup_databse():
    """
    Fixture to set up the in-memory database with test data
    """

    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    with open("./test/database_dump.sql") as fp:
        cur.executescript(fp.read())

    # Add users filter
    """
    filters_dict { 
        'send_duplicates': True ,
        'price_value_amd': 500000,
        'agent_status': None,
        'garage': BOOLEAN DEFAULT NULL,
        'rooms_count' INTEGER DEFAULT NULL,
        'toilet_count' INTEGER DEFAULT NULL,
        'furniture' TEXT DEFAULT NULL,
        'children_allowed' BOOLEAN DEFAULT NULL,
        'animals_allowed' BOOLEAN DEFAULT NULL,
        'total_area' INTEGER DEFAULT NULL,
        'land_area' INTEGER DEFAULT NULL,
        'floors_count' INTEGER DEFAULT NULL,
        'district' VARCHAR(50) DEFAULT NULL
    }
    """
    yield cur


@pytest.fixture
def setup_tlg_bot():
    """
    Setup mock tlg bot
    """

    def custom_sender(method, url, **kwargs):
        result = util.CustomRequestResponse(
            '{"ok":true,"result":{"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}'
        )
        return result

    apihelper.CUSTOM_REQUEST_SENDER = custom_sender
    tb = TeleBot("test")
    yield tb
