"""
Logging configuration
"""

import logging.config
import os

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "simple",
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": os.getenv("LOG_LEVEL", "DEBUG")}},
}


logging.config.dictConfig(LOGGING)
