import torch
import json
import numpy as np
import random
import os
from yaml import safe_load
import base64

import logging


def load_config(config_path: str, config_name: str) -> dict:
    with open(os.path.join(config_path, config_name)) as file:
        config = safe_load(file)
    return config


def init_logging(
    level=logging.INFO,
    save_to_file=False,
    formatter="%(asctime)s-%(levelname)s-%(message)s",
):
    logging.basicConfig(
        #         filename = "test.log",
        level=level,
        format=formatter,
        datefmt="%d-%b-%y %H:%M:%S",
    )


def set_seed(seed: int) -> None:
    """
    Set the seed for random number generators for reproducibility.

    Args:
    - seed (int): The seed value.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def format_timediff(
    seconds: int, format_str: str = "{hours}h{minutes}m{seconds}"
) -> str:
    """
    Format the time difference in seconds into a readable string.

    Args:
    - seconds (int): The time difference in seconds.
    - format_str (str): The format string for the output.

    Returns:
    - str: The formatted time difference string.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_timediff = format_str.format(
        hours=hours, minutes=minutes, seconds=seconds
    )

    return formatted_timediff


def get_all_filepaths(folder_path: str, n=99999999) -> tuple[list[str], int]:
    """
    Get all file paths from the specified folder.

    Args:
    - folder_path (str): The path to the folder.
    - n (int): Maximum number of file paths to retrieve (default is 99999999).

    Returns:
    - tuple[list[str], int]: A tuple containing a list of file paths and the size of the list.
    """
    file_paths = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(folder_path)
        for file in files
        if os.path.basename(root) == os.path.basename(folder_path)
    ][:n]

    return file_paths, len(file_paths)


def get_filepaths_iterator(folder_path: str, n: int):
    """
    Get an iterator of file paths from the specified folder up to a limit of n files.

    Args:
    - folder_path (str): The path to the folder.
    - n (int): The maximum number of files to include in the iterator.

    Returns:
    - Iterator[str]: An iterator of file paths.
    """
    file_paths = (
        os.path.join(root, file)
        for root, dirs, files in os.walk(folder_path)
        for file in files
    )
    limited_file_paths = (file_path for _, file_path in zip(range(n), file_paths))
    return limited_file_paths


def get_filename(long_path: str, extension=False) -> str:
    """
    Get the filename from a long path.

    Args:
    - long_path (str): The long path containing the filename.
    - extension (bool): Whether include extension / no

    Returns:
    - str: The filename.
    """
    filename = os.path.basename(long_path)
    if not extension:
        filename = os.path.splitext(filename)[0]

    return filename


def unpack_json(json_file_path):
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{json_file_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
