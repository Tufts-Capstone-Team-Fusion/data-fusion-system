import cv2
import numpy as np

# # Load images
rgb_image = cv2.imread("../assets/rbg_image.png")
thermal_image = cv2.imread("../assets/thermal_image.png")

# # Detect key points and compute descriptors (using SIFT as an example)
# sift = cv2.SIFT_create()
# keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
# keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

# # Match descriptors
# bf = cv2.BFMatcher()
# matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# # Apply ratio test to filter good matches
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.75 * n.distance:
#         good_matches.append(m)

# # Get corresponding points
# src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
# dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
# Show the images

# Manually input corresponding points
# used photpea to find points
# src is thermal
therm_pts = [
    [238, 160],
    [264, 164],
    [247, 223],
    [58, 220],
    [179, 512],
    [317, 506]
]
# dst is visual
rbg_pts = [
    [320, 89],
    [357, 94],
    [332, 174],
    [85, 170],
    [236, 580],
    [428, 575]
]

# Convert points to numpy arrays
dst_pts = np.array(therm_pts).reshape(-1, 1, 2)
src_pts = np.array(rbg_pts).reshape(-1, 1, 2)

# Compute homography matrix using RANSAC
homography_matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

def translatePoint(x, y):
    pt = np.array([[x], [y], [1]], dtype=np.float32)
    transformed_pt = np.dot(homography_matrix, pt)

    w = transformed_pt[2, 0]
    u = transformed_pt[0, 0] / w
    v = transformed_pt[1, 0] / w

    # print(f"Transformed Point: ({u}, {v})")

    return (round(u), round(v))


# Use homography matrix for transformation if needed
# warped_image = cv2.warpPerspective(image1, homography_matrix, (image2.shape[1], image2.shape[0]))

# image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) #grayscale for brightness multiplying
gray_thermal = cv2.cvtColor(thermal_image.copy(), cv2.COLOR_BGR2GRAY) #grayscale for brightness multiplying
output_image = np.zeros_like(thermal_image)


BRIGHTNESS_THRESHOLD = 75
CUTOFF_THRESHOLD_ENABLED = True #todo not permanent

# Loop over all points in the image
rgb_height, rgb_width = rgb_image.shape[:2]
for y in range(rgb_height):
    for x in range(rgb_width):
        tX, tY = translatePoint(x, y)
        if CUTOFF_THRESHOLD_ENABLED:    #only show pixels over a certain brightness
            if gray_thermal[tY, tX] > BRIGHTNESS_THRESHOLD:
                output_image[tY, tX] = rgb_image[y, x]
        else:   #scale all pixels by brightness
            scale = gray_thermal[tY, tX] / 255.0
            output_image[tY, tX] = (rgb_image[y, x] * scale).astype(np.uint8)

cv2.imshow("Overlay", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
