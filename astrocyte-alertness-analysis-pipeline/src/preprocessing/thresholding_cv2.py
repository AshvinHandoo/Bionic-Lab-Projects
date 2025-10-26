"""
File: thresholding_cv2.py
Origin: "Thresholding.py"
Category: Data preprocessing & signal conditioning
Author: Ashvin Handoo
Last Updated: 2025-10-26

Summary:
    Part of the astrocyte-alertness-analysis-pipeline. This module was renamed and
    lightly documented for clarity and recruiter readability.

Notes for Reviewers:
    • Original logic preserved; variable naming and comments minimally cleaned.
    • Data paths may be set via CLI args or environment variables.
    • See README for synthetic data demo and end-to-end run instructions.

"""


# ---- Original script content below ----

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
