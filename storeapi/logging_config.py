from logging.config import dictConfig

from storeapi.config import DevConfig, config


# Logging configuration
def configure_logging():
    """Configure logging settings for the application."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                }
            },
            "formatters": {
                "default": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s - %(levelname)s : %(lineno)d  %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "json_ensure_ascii": False,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | (%(correlation_id)s) | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "rich.logging.RichHandler",
                    "formatter": "default",
                    "level": "DEBUG",
                    "filters": ["correlation_id"],
                },
                "RotatingFileHandler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "storeapi.log",
                    "maxBytes": 10 * 1024 * 1024,  # 10 MB
                    "backupCount": 5,
                    "formatter": "file",
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "encoding": "utf-8",
                    "filters": ["correlation_id"],
                },
            },
            "loggers": {
                "storeapi": {
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "handlers": ["console", "RotatingFileHandler"],
                    "propagate": False,
                },
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["console", "RotatingFileHandler"],
                },
                "database": {
                    "level": "WARNING",
                    "handlers": ["console", "RotatingFileHandler"],
                },
                "sqlalchemy": {
                    "level": "WARNING",
                    "handlers": ["console", "RotatingFileHandler"],
                },
                "asyncpg": {
                    "level": "WARNING",
                    "handlers": ["console", "RotatingFileHandler"],
                },
            },
        }
    )
