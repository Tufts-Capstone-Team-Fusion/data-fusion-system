import cv2

def extract_frames(video_path):
    frames = []

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    success, image = video_capture.read()

    # Loop through the video frames
    while success:
        # Append the frame to the list
        frames.append(image)
        
        # Read the next frame
        success, image = video_capture.read()

    # Release the video capture object
    video_capture.release()

    return frames