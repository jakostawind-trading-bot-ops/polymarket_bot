import logging
import logging.config
import time


def configure_logging(level: str = "INFO") -> None:
    logging.Formatter.converter = time.gmtime

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s.%(msecs)03dZ | "
                    "%(levelname)-8s | "
                    "%(name)s | "
                    "%(filename)s:%(lineno)d | "
                    "%(funcName)s | "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": level,
            "handlers": ["console"],
        },
    })