import numpy as np
import cv2
import imutils
from time import sleep

def cropImageTopLeft(img):
    y, x = img.shape[:2]
    # crop top left
    return img[0:y//2, 0:(2*x//3)]

initial_image = imutils.rotate(cv2.imread('./Images/H14.jpg'),180)
crop_image = cropImageTopLeft(initial_image)
gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
gauss = cv2.GaussianBlur(gray, (5,5),0)
canny = cv2.Canny(gauss,100,200)

contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
result = []
crops = []

for i, cnt in enumerate(contours):
    if hierarchy[0][i][3] != -1 and hierarchy[0][i][2] < 0:
        print("hir1")
        if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 3000:
            print("hir2")
            x, y, w, h = cv2.boundingRect(cnt)
            if w < 50:
                print("hir3")
                if h < 100:
                    print("hir4")
                    if 0.35 < w / h < 0.7:
                        print("hir5")
                        box_classified = True
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        for point in box:
                            if point[0] == 0 or point[1] == 0:
                                box_classified = False
                        if box_classified:
                            result.append(cnt)
                            print(hierarchy[0][i])
                            print(rect)
                            box = cv2.boxPoints(rect)
                            box = np.int0(box)
                            print(box)
                            print("--------------------")
                            #Append to Crops
                            x, y, width, height = cv2.boundingRect(box)
                            crops.append(canny[y: y + height, x: x + width])

while True:
    for c in crops:
        cv2.imshow("crop",c)
        sleep(1)
    cv2.imshow("img", cv2.drawContours(crop_image, result, -1, (0, 255, 0), 3))
    cv2.imshow("img", canny)
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
       break

#Do Cleanup
cv2.destroyAllWindows()