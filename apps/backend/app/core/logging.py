import logging
from logging.config import dictConfig


def configure_logging() -> logging.Logger:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            }
        },
        "loggers": {
            "eagleeye": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }
    dictConfig(logging_config)
    return logging.getLogger("eagleeye")


logger = configure_logging()

