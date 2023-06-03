import re
from dataclasses import dataclass

@dataclass
class Config:
    """
    Generic config for entries in DayOne
    """
    datetime_format: str = "%Y-%m-%dT%H:%M:%S%Z"
    timeZone: str = "IST"
    # Regex that is used to find images in markdown. Currently this is compatible with Obsidian.
    image_regex = re.compile(r'(!\[\[.*?\]\])')
    # DayOne replacement text
    dayone_image = '![](dayone-moment://{image_name})'
    formats = ['.jpeg', '.png']


@dataclass
class LoggingConfig:
    """
    Logging configs
    """
    logger_format = '["%(levelname)s"] module: %(module)s func_name: %(funcName)s line: %(lineno)s \t "%(message)s"'
    logging_config = dict(
            version=1,
            disable_existing_loggers=False,
            root={
                "level": "INFO",
                "handlers": ["app"]
            },
            formatters={
                "app": {
                    "format": str(logger_format),
                    "class": "logging.Formatter"
                }
            },
            handlers={
                "app": {
                    "class": "logging.StreamHandler",
                    "formatter": "app",
                    "stream": "ext://sys.stdout"
                }
            }
    )


@dataclass
class CreationConfig:
    """
    Config for creation device
    """
    creationOSName: str = 'MacOS'
    creationDeviceType: str = 'MacBook Pro'
    creationDevice: str = 'My MacBook'
