import cv2
import numpy as np

img = cv2.imread('ViCait.jpg')  # Load Image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Make Grayscale
_, frame = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)  # All Pixels with color lower than 128 get black, the others get white. INV turn black to white and white to black.

splittedImage = np.hsplit(frame, 2)  # Split Image horizontaly (vsplit for vertical)

whitePixelsLeft = np.count_nonzero(splittedImage[0])  # Count White Pixels on the left and right side
whitePixelsRight = np.count_nonzero(splittedImage[1])

# ++Show which side of the picture has more white
difference = whitePixelsLeft - whitePixelsRight

# Difference must always be positive
if (difference < 0):
    difference = difference * -1

if (difference < 250):  # If the difference is too minimal to say if right or left are more
    result = 0
    print("same same")
elif (whitePixelsLeft > whitePixelsRight):
    result = -1
    print("left more white")
else:
    result = 1
    print("right more white")
# --Show which side of the picture has more white