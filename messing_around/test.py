import cv2
import numpy as np

# print(cv2.__version__)
# # Load images
image1 = cv2.imread("image1small.png")
image2 = cv2.imread("image2small.png")

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
src_pts = [
    [238, 160],
    [264, 164],
    [247, 223],
    [85, 170],
    [179, 512],
    [317, 510]
]
dst_pts = [
    [320, 89],
    [357, 94],
    [332, 174],
    [58, 220],
    [224, 580],
    [428, 575]
]

# Convert points to numpy arrays
src_pts = np.array(src_pts).reshape(-1, 1, 2)
dst_pts = np.array(dst_pts).reshape(-1, 1, 2)


# Compute homography matrix using RANSAC
homography_matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

print(homography_matrix)

# Use homography matrix for transformation if needed
warped_image = cv2.warpPerspective(image1, homography_matrix, (image2.shape[1], image2.shape[0]))

# Display the images side by side
# concatenated_images = np.concatenate((image1, image2), axis=1)
cv2.imshow("Matches", warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



# source my_env/bin/activate then:
# python3 filenaem