import os
import ujson
import argparse
import logging
import logging.config

from src.file_converter import convert_md
from src.config import LoggingConfig

logger = logging.getLogger()
logging.config.dictConfig(LoggingConfig.logging_config)

if __name__ == '__main__':
    """
    python3 --source <> --dest <>
    --debug y # To generate logs
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--source',
        help='Location of the file or folder which you want to convert. If you pass the folder location, all files present will be converted',
        type=str,
        default=None,
        required=True
    )

    parser.add_argument(
        '--dest',
        help='Location of the folder where you want to dump the converted notes in JSON format. Defaults to the current working directory.',
        type=str,
        default=os.path.join(os.getcwd()),
        required=False
    )

    parser.add_argument(
        '--debug',
        help='Weather to run in debug mode (y/n). Defaults to `n`',
        type=str,
        default='n',
        required=False
    )

    args = parser.parse_args()

    assert args.debug in ['y', 'n'], 'Debug mode must be one of `y` or `n`'

    logger.setLevel(logging.INFO)
    if args.debug == 'y':
        logger.setLevel(logging.DEBUG)

    logger.debug(f"Received arguments: {args}")

    entries = {
        "entries": convert_md(source = args.source)
    }

    with open(os.path.join(args.dest, "day_one_import.json"), "w") as fp:
        ujson.dump(entries, fp, escape_forward_slashes=False)
