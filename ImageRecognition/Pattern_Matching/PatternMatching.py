import cv2
import os

# Import all captured images
path = 'pictures_real/fahrt/'
capturenames = os.listdir(path)  # list of subdirectories and files
captures = []

for capturename in os.listdir(path):
    temp = path + capturename
    captures.append(cv2.imread(temp,0))

# Read all template images
path = 'pictures_real/templates/'
templatenames = os.listdir(path)
templates = []
for templatename in templatenames:
    temp = path + templatename
    templates.append(cv2.imread(temp, 0))


# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
           'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']

numbers = [0, 0, 0, 0, 0, 0, 0, 0]

for meth in methods:
    maxwkeittemp = 0
    maxnotemp = 0
    for capture in captures:
        # capture = cv2.resize(capture, (20, 40))
        # Get widht/height
        height, width = capture.shape
        # if capture is too small, dont do anything
        if (height > 30 & width > 18):
            # so something
            i = 0
            for template in templates:
                i += 1
                w, h = template.shape[::-1]
                method = eval(meth)

                # Apply template Matching
                res = cv2.matchTemplate(capture, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                # print(str(max_val))
                if max_val > maxwkeittemp:
                    maxwkeittemp = max_val
                    maxnotemp = i
    numbers[maxnotemp] += 1;
max = max(numbers)
print(numbers.index(max))

