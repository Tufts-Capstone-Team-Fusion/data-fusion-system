import cv2
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
from get_frames import extract_frames

points = []
img = None

# This function is responsible for generating a homography using openCV
# it takes in a thermal and rgb image and makes the user click points on 
# the rgb image and then corresponding points on the thermal image.
# it then creates a matrix using those corresponding points and saves it
def doCalibration(rgb_image, thermal_image):
    # points and img must be set outside of this function
    def get_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Clicked at ({x}, {y})")
            points.append([x, y])
            cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
            cv2.imshow('image', img)

    # gets the list of keypoints
    def getKeyPoints(image):
        global img
        global points
        img = image
        points = []
        
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', get_mouse_click)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Press 'q' to exit
                break

        return copy.copy(points)

    # get keypoints for each image
    rbg_pts = getKeyPoints(rgb_image)
    therm_pts = getKeyPoints(thermal_image)

    # check to make sure the number of keypoints makes sense
    if (len(rbg_pts) != len(therm_pts)):
        print("number of points must be equal on both images")
        return None
    if (len(rbg_pts) < 4):
        print("calibration requires 4 points minimum")
        return None
    if (len(rbg_pts) < 10):
        print("Warning: we recommend using more points for calibration")

    # Convert points to numpy arrays
    dst_pts = np.array(therm_pts).reshape(-1, 1, 2)
    src_pts = np.array(rbg_pts).reshape(-1, 1, 2)

    # Compute homography matrix using RANSAC
    homography_matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    np.save('calibration_matrix.npy', homography_matrix)
    return homography_matrix

# loads the videos into arrays of images
print("extracting videos to frames")
thermal_frames = extract_frames("../assets/thermal_video3.mp4")
rgb_frames = extract_frames("../assets/rgb_video3.mp4")

# if the calibration matrix exists, load it, otherwise force the user to make one
print("done extracting videos")
print("checking if calibration matrix exists")
homography_matrix = None
if os.path.exists('calibration_matrix.npy'):
    print("matrix existed from previous calibration, continuing")
    homography_matrix = np.load('calibration_matrix.npy')
else:
    print("calibration matrix not found, calibrating")
    print("click matching points in the same order")
    homography_matrix = doCalibration(rgb_frames[0].copy(), thermal_frames[0].copy())
if homography_matrix is None:
    print("something went wrong, exiting")
    exit(1)


# takes the x, y coordinates from an rgb image and outputs the x,y coordinates
# of the corresponding point on the thermal image.
def translatePoint(x, y):
    pt = np.array([[x], [y], [1]], dtype=np.float32)
    transformed_pt = np.dot(homography_matrix, pt)

    w = transformed_pt[2, 0]
    u = transformed_pt[0, 0] / w
    v = transformed_pt[1, 0] / w

    return (round(u), round(v))

# checks if the point is within the bounds
def checkPoint(x, y, maxX, maxY):
    if (x < 0 or x >= maxX):
        return False
    if (y < 0 or y >= maxY):
        return False
    return True


# The first of the implemented fusion algorithms. It takes an rgb image and a thermal
# image. It then scales the rgb values based on the normalized thermal greyscale
# value and returns the result
def combine_images(rgb_image, thermal_image):
    gray_thermal = cv2.cvtColor(thermal_image.copy(), cv2.COLOR_BGR2GRAY) #grayscale for brightness multiplying
    output_image = np.zeros_like(thermal_image)

    maxY, maxX = gray_thermal.shape[:2]

    # Loop over all points in the image
    rgb_height, rgb_width = rgb_image.shape[:2]
    for y in range(rgb_height):
        for x in range(rgb_width):
            tX, tY = translatePoint(x, y) 
            if not checkPoint(tX, tY, maxX, maxY): continue
            scale = gray_thermal[tY, tX] / 255.0
            output_image[tY, tX] = (rgb_image[y, x] * scale).astype(np.uint8)

    return output_image

# combine_images2 takes a rgb and thermal image and combines them together by
# adding their values together. This is the fastest fusion algorithm becuase
# it doesn't do much work in python, instead it hands off the work to OpenCV's
# .addWeighted() function which runs much faster than looping over every pixel
# in python.
def combine_images2(rgb_image, thermal_image):
    # if you don't like the orange look of the thermal you can make it grayscale
    gray_thermal = cv2.cvtColor(thermal_image.copy(), cv2.COLOR_BGR2GRAY)
    gray_thermal_rgb = cv2.cvtColor(gray_thermal, cv2.COLOR_GRAY2BGR)

    warped_img = cv2.warpPerspective(rgb_image, homography_matrix, (gray_thermal.shape[1], gray_thermal.shape[0]))

    # controls how strong each image is in the output
    alpha = 0.5

    # Blend the images
    # switch "thermal_image" with "gray_thermal_rgb" to make thermal grayscale
    output_image = cv2.addWeighted(thermal_image, alpha, warped_img, 1 - alpha, 0)

    return output_image


# This algorithm first warps the rgb image and then combines the two images
# together similar to the first combine_images(). However, it does not need to
# do the costly matrix multiplications. However, there is something wrong with
# this method because the images do not come out calibrated.
def combine_images3(rgb_image, thermal_image):
    gray_thermal = cv2.cvtColor(thermal_image.copy(), cv2.COLOR_BGR2GRAY) #grayscale for brightness multiplying

    warped_img = cv2.warpPerspective(rgb_image, homography_matrix, (gray_thermal.shape[1], gray_thermal.shape[0]))

    rgb_height, rgb_width = rgb_image.shape[:2]
    for y in range(rgb_height):
        for x in range(rgb_width):
            scale = gray_thermal[y, x] / 255.0
            thermal_image[y, x] = (rgb_image[y, x] * scale).astype(np.uint8)

    return thermal_image

# calls the combine_images() function on each pair of frames
def combine_videos(rgb, thermal):
    frames = []
    # This was a bit of a lazy solution, we manually change this value to change
    # the number of frames that get fused.
    maxFrames = 400
    for i in range(maxFrames):
        print("combining images (", i, "/", maxFrames, ")")
        fusedIm = combine_images2(rgb[i], thermal[i])
        frames.append(fusedIm)
    return frames

# takes the arrays of frames and makes them into a video
def frames_to_video(frames, output_video_path, fps=60):
    # Get the height and width of the frames
    frame_height, frame_width, _ = frames[0].shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # Write each frame to the video
    for frame in frames:
        video_writer.write(frame)

    # Release the VideoWriter
    video_writer.release()

print("combining frames")
combined_frames = combine_videos(rgb_frames, thermal_frames)
print("making video")
# change this file path to change the name of the resulting file
frames_to_video(combined_frames, "../assets/fused10.mp4")
print("done!")