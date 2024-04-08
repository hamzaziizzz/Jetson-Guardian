"""
This module is created to define the general utilities required by the project.

Date: 29 March 2024
Author: Hamza Aziz
"""

import os.path
from custom_logger import core_logger


def create_directory(directory_name: str) -> None:
    """
    This function will create a new directory (if not present already) by the given name.

    Parameters:
        directory_name (str): The name of the directory to be created or checking existence.

    Returns:
        None
    """
    try:
        os.makedirs(directory_name)
    except OSError as error:
        core_logger.error(f"Directory can not be created due to the following error:\n        {error}")
