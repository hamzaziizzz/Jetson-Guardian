"""
This module contains custom logger which will be shared by all the modules

Date: 29 March 2024
Author: Hamza Aziz
"""

import logging

# Custom Modules
from parameters import LOGS_FOLDER, IP_CAM_LOGGER_FILE_PATH, CORE_PROJECT_LOGGER_FILE_PATH
from utils.general_utilities import create_directory

# create a directory for logs if it does not exist
log_file_dir = LOGS_FOLDER
create_directory(log_file_dir)

# Define log file paths for each component
ip_cam_streamer_log_file = IP_CAM_LOGGER_FILE_PATH
core_project_log_file = CORE_PROJECT_LOGGER_FILE_PATH

# CONFIGURE THE LOGGERS FOR EACH COMPONENT
# Core Logger
core_logger = logging.getLogger("core_project")
core_logger.setLevel(logging.DEBUG)
core_handler = logging.FileHandler(core_project_log_file)
core_formatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
core_handler.setFormatter(core_formatter)
core_logger.addHandler(core_handler)

# IP Camera Streamer Logger
ip_cam_streamer_logger = logging.getLogger('ip_cam_streamer')
ip_cam_streamer_logger.setLevel(logging.DEBUG)
ip_cam_streamer_handler = logging.FileHandler(ip_cam_streamer_log_file)
ip_cam_streamer_formatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
ip_cam_streamer_handler.setFormatter(ip_cam_streamer_formatter)
ip_cam_streamer_logger.addHandler(ip_cam_streamer_handler)
