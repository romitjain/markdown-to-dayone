import os
from logging import getLogger
from .utils import (
    process_text,
    process_tags,
    process_timestamp,
    generate_uuid
)
from .config import (
    Config,
    CreationConfig
)

logger = getLogger()

def process_file(file: os.DirEntry) -> dict:
    """
    Processes a single markdown file and convert it into Day One format

    Args:
        file (os.DirEntry): File type

    Returns:
        dict: DayOne format dict
    """
    with open(file, "r") as fp:
        text = fp.read()

    file_sats = file.stat()

    text = file.name.replace('.md', '') + '\n' + text
    text, tags = process_tags(text)
    text, photos = process_text(text, file_sats.st_ctime)

    #TODO: Generate schema automatically
    entry = {}

    entry.update({
        "tags": tags,
        "uuid": generate_uuid(),
        "starred": False, #TODO: Take user input for starred files
        "creationOSName": CreationConfig.creationOSName,
        "timeZone": Config.timeZone,
        "photos": photos,
        "text": text,
        "creationDate": process_timestamp(file_sats.st_ctime),
        "creationDeviceType": CreationConfig.creationDeviceType,
        "modifiedDate": process_timestamp(file_sats.st_mtime)
    })

    #TODO: Validate schema
    # if validate_schema(entry):
    #     print("ERROR: Not able to validate the schema!")

    return entry


def convert_md(source:str) -> dict:
    """
    Converts all the files in a particular folder to JSON format that can be imported by Day One

    Args:
        source (str): Source folder where the markdown files are present

    Returns:
        dict: Dict that can be written to disk (expected by Day One)
    """

    print(f"\n\n-----\nProcessing folder: {source}\n-----\n\n")
    entries, sub_folders = [], []

    with os.scandir(source) as dir_contents:
        # Process directory contents one after the other
        for entry in dir_contents:

            if entry.name.startswith('.'):
                logger.info(f"Skipping hidden file/folder: {entry.name}")
                continue

            if entry.is_file() and entry.name.split(".")[-1] == "md":
                logger.info(f"Processing {entry.name}")

                data = process_file(entry)

                if data is not None:
                    logger.info(f"Completed processing for {entry.name}")
                    entries.append(data)
                    continue

                logger.error(f"Not able to process {entry.name}")
                continue

            elif entry.is_file() and entry.name.split(".")[-1] != "md":
                logger.info(f"Non markdown file found {entry.name}")
                continue

            logger.debug(f"Subfolder found {entry.name}")
            sub_folders.append(entry)

    logger.debug(f"Sub folders: {sub_folders}")
    for folder in sub_folders:
        temp = convert_md(folder)
        entries += temp

    return entries
