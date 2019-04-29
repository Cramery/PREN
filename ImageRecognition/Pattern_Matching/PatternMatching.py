import cv2
import numpy as np

captures = [cv2.imread('pictures/two/all.jpeg',0)]
template = cv2.imread('pictures/two/close.jpeg',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED',
           'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']

for meth in methods:
    for capture in captures:
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(capture, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        print(str(max_val))

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(capture,top_left, bottom_right, 255, 2)