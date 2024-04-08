"""
This module is created to define all the parameters required by the project at one place.

Date: 29 March 2023
Author: Hamza Aziz
"""

# Toggle for which frame to be processed
FRAME_DROP_FACTOR = 1

# Wait time before try to reconnect the camera
IP_CAM_REINIT_WAIT_DURATION = 10  # seconds

# IP addresses of the IP Cameras
CAMERA_IP_ADDRESSES = {
    "outdoor-camera": "rtsp://grilsquad:grilsquad@192.168.5.1:554/stream1"
}

# Log file paths
LOGS_FOLDER = "logs"
IP_CAM_LOGGER_FILE_PATH = f"{LOGS_FOLDER}/ip_cam_streamer.log"
CORE_PROJECT_LOGGER_FILE_PATH = f"{LOGS_FOLDER}/core_project.log"
