import cv2

# All images we saved will be saved in this array, these are the pictures from the train
imgs = [cv2.imread('pictures/two/close.jpeg', 0)]

# All template-pictures
templates = [cv2.imread('pictures/templates/two.jpeg', 0),
             cv2.imread('pictures/templates/six.jpeg', 0)]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED',
           'cv2.TM_CCOEFF', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF']

for img in imgs:
    w, h = img.shape[::-1]
    for meth in methods:
        highprob = 0
        i = 0
        highprob = 0
        for template in templates:
            i += 1
            template2 = template.copy()
            method = eval(meth)
            # Apply template Matching
            res = cv2.matchTemplate(template, img, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # welches Template ist es am ehsten?
            # Nr. und Prozentzahl dieses Templates hinzufÃ¼gen (Median dieser Berechnen)
            if max_val > highprob:
                highprob = max_val
                highNr = i

        print(highNr) # Sobald alle Zahlen als Templates eingelesen sind, macht dies Sinn
        print(highprob)
