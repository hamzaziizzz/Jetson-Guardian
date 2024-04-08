"""
This module is created to produce a stream from an IP Camera and publishes it to a Kafka topic.

Date: 29 March 2024
Author: Hamza Aziz
"""

import threading
import time
import cv2

# Custom Modules
from parameters import CAMERA_IP_ADDRESSES, FRAME_DROP_FACTOR, IP_CAM_REINIT_WAIT_DURATION
from custom_logger import ip_cam_streamer_logger


class IPCamera:
    """
    A class to represent an IP camera
    """

    def __init__(self, cam_name: str, cam_ip: str, shared_buffer):
        """
        Initialize the camera
        """
        self.frame = None
        self.shared_buffer = shared_buffer
        self.cam_name = cam_name
        self.cam_ip = cam_ip
        # initialize the video camera stream and read the first frame
        self.stream = cv2.VideoCapture(self.cam_ip)
        # we need to read the first frame to initialize the stream
        self.grabbed, _ = self.stream.read()
        # store whether the camera stream was initialized successfully
        self.is_initialized = self.grabbed
        # set the flag to process the frame
        self.process_this_frame = True
        # initialize a frame counter
        self.frame_counter = 0
        if not self.grabbed:
            ip_cam_streamer_logger.error(
                f"Camera stream from {self.cam_name} (url: {self.cam_ip})) unable to initialize"
            )
        else:
            ip_cam_streamer_logger.info(
                f"Camera stream from {self.cam_name} (url: {self.cam_ip}) initialized"
            )

    def _read_one_frame(self):
        """
        Reads a frame from the camera
        """
        self.grabbed, self.frame = self.stream.read()

    def _read_and_discard_frame(self):
        """
        Reads and discards one frame
        """
        _, _ = self.stream.read()

    def release(self):
        """
        Releases the camera stream
        """
        self.stream.release()

    def place_frame_in_buffer(self):
        """
        Places the frame in the buffer
        """
        if self.process_this_frame:
            self._read_one_frame()
            if not self.grabbed:
                # if the frame was not grabbed, then we have reached the end of the stream
                ip_cam_streamer_logger.error(
                    f'Could not read a frame from the camera stream from {self.cam_name} (url: {self.cam_ip})). '
                    f'Releasing the stream...')
                self.release()
                self.is_initialized = False
            else:
                # TODO: Publish the captured frame to a Kafka topic
                cv2.imshow(f"{self.cam_name}", self.frame)
                self.shared_buffer.put((self.frame, self.cam_name, self.cam_ip))
        else:
            self._read_and_discard_frame()

        # toggle the flag to process alternate frames to improve the performance
        self.frame_counter += 1
        if self.frame_counter % FRAME_DROP_FACTOR == 0:
            self.process_this_frame = True
        else:
            self.process_this_frame = False


def create_camera(cam_name: str, cam_ip: str, shared_buffer):
    """
    Creates a camera object and places the frames in the buffer

    Parameters:
        cam_name (str): name of the camera
        cam_ip (str): url of the camera
        shared_buffer: shared memory space to store the pre-processed frames

    Returns:
        None
    """
    cam = IPCamera(cam_name, cam_ip, shared_buffer)
    # Place the frames in the buffer until the end of the camera stream is reached

    while True:
        if cam.is_initialized:
            cam.place_frame_in_buffer()
        else:
            # destroy the camera object since the camera stream was not initialized
            ip_cam_streamer_logger.error(
                f"Camera stream from {cam.cam_name} (url: {cam.cam_ip})) is not accessible. Destroying the camera "
                f"object...")
            del cam

            # put the thread to sleep for 10 seconds
            ip_cam_streamer_logger.info(
                f"Putting the thread to sleep for {cam_name} (url: {cam_ip})) for {IP_CAM_REINIT_WAIT_DURATION} "
                f"seconds..."
            )
            time.sleep(IP_CAM_REINIT_WAIT_DURATION)

            # again try to recreate a new camera object
            ip_cam_streamer_logger.info(f"Creating a new camera object for {cam_name} (url: {cam_ip}))...")
            cam = IPCamera(cam_name, cam_ip, shared_buffer)


def producer_main(shared_buffer):
    # Create a thread for each camera and start the thread
    for cam_name in CAMERA_IP_ADDRESSES:
        cam_ip = CAMERA_IP_ADDRESSES[cam_name]
        cam_thread = threading.Thread(target=create_camera, args=(cam_name, cam_ip, shared_buffer))
        cam_thread.start()
