from logging.config import dictConfig


def setup_logger():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(name)s at %(asctime)s - %(levelname)s - %(message)s",
                    "datefmt": "%HH:%MM:%SS",
                }
            },
            "handlers": {
                "console": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                }
            },
            "root": {"handlers": ["console"], "level": "INFO"},
        }
    )
