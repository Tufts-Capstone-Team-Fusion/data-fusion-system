'''
Goal: have this file output the proper calibration points given a set of images with chessboards

Link to FLIR website talking about calibration (including what OpenCV links to use)
https://flir.custhelp.com/app/answers/detail/a_id/4639/~/flir-oem---boson%2C-lepton%2C-or-tau---intrinsic-thermal-camera-core-calibration#:~:text=The%20calibration%20can%20be%20done,halogen%20lamp%2C

Link to chessboard imaging help from OpenCV stereo camera calibration
https://martinperis.blogspot.com/2011/01/opencv-stereo-camera-calibration.html

'''
import cv2
import matplotlib.pyplot as plt
import numpy as np
import copy
import os

points = []
img = None

def doCalibration(rgb_image, thermal_image):
    # points and img must be set outside of this function
    def get_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Clicked at ({x}, {y})")
            points.append([x, y])
            cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
            cv2.imshow('image', img)

    # points = []
    # img = rgb_image

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


    rbg_pts = getKeyPoints(rgb_image)
    therm_pts = getKeyPoints(thermal_image)

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


# # # Load images
rgb_image = cv2.imread("../assets/checkerboard.png")
thermal_image = cv2.imread("../assets/check8.png")

homography_matrix = None
if os.path.exists('calibration_matrix.npy'):
    homography_matrix = np.load('calibration_matrix.npy')
else:
    print("calibration matrix not found, calibrating")
    homography_matrix = doCalibration(rgb_image, thermal_image)

if homography_matrix is None:
    print("something went wrong, exiting")
    exit(1)

def translatePoint(x, y):
    pt = np.array([[x], [y], [1]], dtype=np.float32)
    transformed_pt = np.dot(homography_matrix, pt)

    w = transformed_pt[2, 0]
    u = transformed_pt[0, 0] / w
    v = transformed_pt[1, 0] / w

    # print(f"Transformed Point: ({u}, {v})")

    return (round(u), round(v))


def checkPoint(x, y, maxX, maxY):
    if (x < 0 or x >= maxX):
        return False
    if (y < 0 or y >= maxY):
        return False
    return True

# image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) #grayscale for brightness multiplying
gray_thermal = cv2.cvtColor(thermal_image.copy(), cv2.COLOR_BGR2GRAY) #grayscale for brightness multiplying
output_image = np.zeros_like(thermal_image)


BRIGHTNESS_THRESHOLD = 75
CUTOFF_THRESHOLD_ENABLED = True #todo not permanent

maxY, maxX = gray_thermal.shape[:2]

# Loop over all points in the image
rgb_height, rgb_width = rgb_image.shape[:2]
for y in range(rgb_height):
    for x in range(rgb_width):
        tX, tY = translatePoint(x, y) 
        if not checkPoint(tX, tY, maxX, maxY): continue
        if CUTOFF_THRESHOLD_ENABLED:    #only show pixels over a certain brightness
            if gray_thermal[tY, tX] > BRIGHTNESS_THRESHOLD:
                output_image[tY, tX] = rgb_image[y, x]
        else:   #scale all pixels by brightness
            scale = gray_thermal[tY, tX] / 255.0
            output_image[tY, tX] = (rgb_image[y, x] * scale).astype(np.uint8)

cv2.imshow("Overlay", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()