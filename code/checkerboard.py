import cv2
import numpy as np

# # Load images
image = cv2.imread("../assets/check9.png")

# Get the dimensions of the image
height, width, _ = image.shape

# Define the dimensions of each section
section_height = height // 3
section_width = width // 3

# Create a mask to color everything black
mask = np.zeros((height, width), dtype=np.uint8)

# Define the indices of the middle section
start_row = section_height
end_row = 2 * section_height
start_col = section_width
end_col = 2 * section_width

# Color everything black except the middle section
mask[start_row:end_row, start_col:end_col] = 255

# Apply the mask to the original image
result = cv2.bitwise_and(image, image, mask=mask)

gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Find contours in the edged image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop over the contours to find rectangles
for contour in contours:
    # Approximate the contour to a polygon
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    # Check if the contour is a rectangle
    if len(approx) == 4:
        # Create a mask with everything outside the rectangle
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [approx], 0, (255), -1)
        mask = cv2.bitwise_not(mask)
        
        # Set everything outside the rectangle to black
        result[mask != 0] = [0, 0, 0]  # Set to black color
        break

# Display the result
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()


# pattern_size = (6, 9)

# ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

# print(ret)
# print(corners)