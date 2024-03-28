import cv2
import numpy as np

# # Load images
image = cv2.imread("../assets/check10.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

pattern_size = (6, 9)

ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

print(ret)
print(corners)