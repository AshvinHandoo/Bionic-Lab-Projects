# ThresholdingUtilities.py
# -------------------------------------------------------------------------
# Origin: "Thresholding.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   Helper utilities for computing and applying signal thresholds (e.g., std-
dev based cutoffs) used across event detection.
#
# Inputs:
#   - Numeric arrays/series from preprocessing or analysis
#
# Outputs:
#   - Threshold values, boolean masks, or labeled arrays
#
# File Relationships:
#   - Supports DilationEventDetection and EventThresholdDetection.
#
# Dependencies:
#   numpy, pandas
# -------------------------------------------------------------------------

import cv2
import numpy as np

img = cv2.imread('C:/Users/KozaiLab/Downloads/15.jpg', cv2.IMREAD_GRAYSCALE)

blank = np.zeros(img.shape[:2], dtype='uint8')

mask = cv2.circle(blank, (225, 120), 27, 255, -1)
cv2.imshow('Mask', mask)

masked = cv2.bitwise_and(img, img, mask=mask)

threshold_value = 105
replacement_value = 60

img[masked >= threshold_value] = replacement_value

cv2.imshow('Modified Image', img)

# Save the modified image
cv2.imwrite('modified_image.jpg', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
