import re
import uuid
import logging
import jsonschema
from typing import List
from datetime import datetime

from .config import Config, CreationConfig

logger = logging.getLogger()


def validate_schema(data):
    return jsonschema.validate(data)


def process_timestamp(timestamp: str) -> str:
    d = datetime.utcfromtimestamp(timestamp)
    formatted_timestamp = d.strftime(Config.datetime_format)

    logger.debug(f'Formatted timestamp: {formatted_timestamp}')

    return formatted_timestamp


def process_tags(text: str) -> List:
    """
    Process the text and returns a list of all tags in the Markdown text

    Arguments:
        - text {str} -- Markdown text
    Returns:
        - {list} -- List of all tags
    """
    tags = re.findall("#[a-z]+", text)

    for tag in tags:
        logger.debug(f'Replacing {tag} in the main text')
        text = text.replace(tag, '')

    logger.debug(f'Formatted tags: {tags}')

    return text, [t[1:]for t in tags]


def generate_uuid() -> str:
    return uuid.uuid4().hex.upper()


def process_photos(text: str, ctime: str) -> str:
    """
    Find all regex matches of image patterns
    Iterate over each one of them and update the text in the dayone format

    Args:
        text (str): Original text where we need to search for image regex

    Returns:
        (str): Modified text replaced with compatible format
    """
    matches = Config.image_regex.findall(text)
    processed_imgs = []

    if matches:

        # For each match of the image in a line of text
        for idx, match in enumerate(matches):
            # Find out the format of the image
            for frmt in Config.formats:
                if len(match.split(frmt)) > 1:
                    photo_frmt = frmt
                    id = re.sub(r'!(\[.)', '', match.split(frmt)[0])
                    break

            photo = dict(
                orderInEntry=idx,
                creationDevice=CreationConfig.creationDevice,
                date=process_timestamp(ctime),
                identifier=id,
                md5=id,
                type=photo_frmt.replace('.', ''),
                isSketch=False,
            )

            logger.debug(f'Image identifiers: {photo}')
            processed_imgs.append(photo)

            text = text.replace(
                match,
                Config.dayone_image.format(image_name=id)
            )

            logger.debug(f'Found image: {match}')

    return text, processed_imgs


def process_text(text: str, ctime: str) -> str:
    """
    Process markdown text and return it in compatible format

    Args:
        text (str): Original text

    Returns:
        str: Processed text

    8ui*9x9ZirAFGS
    """

    lines = re.split("\n+", text)
    processed_lines, processed_imgs = [], []

    # Process line by line
    for line in lines:
        response = process_photos(line, ctime)
        processed_lines.append(response[0])
        processed_imgs += response[1]

    return '\n'.join(processed_lines), processed_imgs

