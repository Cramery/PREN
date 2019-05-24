import cv2
import os
import numpy as np

def __getCroppedBoxes(videostream):
    crops = []
    for image in videostream:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gauss = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(gauss, 100, 200)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        for i, cnt in enumerate(contours):
            if hierarchy[0][i][3] != -1 and hierarchy[0][i][2] < 0:
                if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 3000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if w < 50:
                        if h < 100:
                            if 0.35 < w / h < 0.7:
                                box_classified = True
                                rect = cv2.minAreaRect(cnt)
                                box = cv2.boxPoints(rect)
                                box = np.int0(box)
                                for point in box:
                                    if point[0] == 0 or point[1] == 0:
                                        box_classified = False
                                if box_classified:
                                    # Append to Crops
                                    x, y, width, height = cv2.boundingRect(box)
                                    crops.append(canny[y: y + height, x: x + width])
    return crops

def writeImages(stream):
    cwd = os.getcwd()
    imgCounter = 0
    for img in stream:
        frameString = cwd + "/images/" + "crop_" + str(imgCounter) + ".jpg"
        cv2.imwrite(frameString, img)
        print(frameString)
        imgCounter += 1

def _readTemplateArray(path):
    templateArray = []
    path = os.getcwd() + path
    for imgName in os.listdir(path):
        templateArray.append(path + imgName)
    return templateArray

def main():
    print("Software started")
    imageNames = _readTemplateArray("/images/")
    imagelist = []
    for img in imageNames:
        #print(img)
        image = cv2.imread(img)
        imagelist.append(image)
    crops = __getCroppedBoxes(imagelist)
    print(len(crops))
    writeImages(crops)

if __name__ == "__main__":
    main()

