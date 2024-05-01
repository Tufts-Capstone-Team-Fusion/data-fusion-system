import cv2
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
from get_frames import extract_frames

def split_video(input_video_path, output_left_path, output_right_path):
    # Open the input video
    video_capture = cv2.VideoCapture(input_video_path)

    # Get the frame dimensions
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the VideoWriters for the left and right videos
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    left_video_writer = cv2.VideoWriter(output_left_path, fourcc, 30.0, (frame_width // 2, frame_height))
    right_video_writer = cv2.VideoWriter(output_right_path, fourcc, 30.0, (frame_width // 2, frame_height))

    print("made it here")

    # Process each frame
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Split the frame into left and right sides
        left_frame = frame[:, :frame_width // 2, :]
        right_frame = frame[:, frame_width // 2:, :]

        # Write the left and right frames to their respective videos
        left_video_writer.write(left_frame)
        right_video_writer.write(right_frame)

    # Release VideoWriters and VideoCapture
    left_video_writer.release()
    right_video_writer.release()
    video_capture.release()

input_video = "../assets/sideBySide2.mp4"
output_left_path = "../assets/rgb_video3.mp4"
output_right_path = "../assets/thermal_video3.mp4"
split_video(input_video, output_left_path, output_right_path)