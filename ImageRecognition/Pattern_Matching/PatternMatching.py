import cv2
import numpy as np

# Import all captured images

path = 'pictures/two/close.jpeg'
captures = []
i = 0

captures.append(cv2.imread(path,0))

templates = [cv2.imread('pictures/two/all.jpeg',0), cv2.imread('pictures/six/all.jpeg',0)]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
           'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']

for meth in methods:
    for capture in captures:
        maxwkeit = 0
        maxno = 0
        i = 0
        for template in templates:
            i += 1
            w, h = template.shape[::-1]
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(capture, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            print(str(max_val))
            if max_val > maxwkeit:
                maxwkeit = max_val
                maxno = i
        print(str(maxno))