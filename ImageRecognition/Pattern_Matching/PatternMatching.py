import cv2
import os

# Import all captured images
path = 'pictures_real/fahrt/'
capturenames = os.listdir(path)  # list of subdirectories and files
captures = []

for capturename in capturenames:
    temp = path + capturename
    captures.append(cv2.imread(temp,0))

# Read all template images
path = 'pictures/two/templates/'
templatenames = os.listdir(path)
templates = []
for templatename in templatenames:
    temp = path + templatename
    templates.append(cv2.imread(temp, 0))


# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
           'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']

for meth in methods:
    print(str(meth))
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