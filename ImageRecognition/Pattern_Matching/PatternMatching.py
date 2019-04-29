import cv2
import numpy as np

captures = [cv2.imread('pictures/two/all.jpeg',0)]
templates = [cv2.imread('pictures/two/close.jpeg',0)]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
           'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']

for meth in methods:
    for capture in captures:
        for template in templates:
            w, h = template.shape[::-1]
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(capture, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            print(str(max_val))