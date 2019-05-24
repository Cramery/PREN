# importing Modules

import cv2
import numpy as np

# video format
video_width = 640
video_height = 360
# set up for the color range
color_lower_range = [70, 40, 40]
color_upper_range = [220, 255, 255]
# set the size of alloud start/stop area
min_area_of_startstop = 1000
max_area_of_startstop = 3000

# Capturing Video through webcam.  set size
video_capture = cv2.VideoCapture(0)
ret = video_capture.set(3, video_width)
ret = video_capture.set(4, video_height)

while (1):
    # img = cv2.imread('/Users/adhurim/Desktop/PREN02/startStopSignal/start_stop_panel.JPG')
    _, img = video_capture.read()

    # converting frame(img) from BGR (Blue-Green-Red) to HSV (hue-saturation-value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # defining the range of Blue color
    blue_lower = np.array(color_lower_range, np.uint8)
    blue_upper = np.array(color_upper_range, np.uint8)

    # finding the range blue colour in the image
    blue = cv2.inRange(hsv, blue_lower, blue_upper)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")

    blue = cv2.dilate(blue, kernal)

    res = cv2.bitwise_and(img, img, mask=blue)

    # Tracking Colour (blue)
    contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # save the data of the detected
    detectedRectangle = []

    # looking for rectangles
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > min_area_of_startstop and area < max_area_of_startstop):
            x, y, w, h = cv2.boundingRect(contour)
            schnitt = w / h
            if (schnitt < 4 and schnitt > 2):
                # draw  a rectangle of every detected blue object
                # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                # print(area)

                # save the data of the rectangle
                # x start coordinate, x end coordinate, y start coordinate, width, heigth
                detectedRectangle.append([x + 1, x + w, y, w, h])

    # needed for iteration of the rectangle array
    current = 0
    next = 1
    detectedRectangle.sort()

    # detected object need to start and end at the same/near x-coordinate.
    # if the rectangle match, draw a red rectangle around
    while (next < len(detectedRectangle)):
        differenceDetectedPanelPosition = detectedRectangle[current][0] / detectedRectangle[next][0]
        diffeenceDetectedPanelWidth = detectedRectangle[current][1] / detectedRectangle[next][1]
        if (
                differenceDetectedPanelPosition > 0.8 and differenceDetectedPanelPosition < 1.2 and diffeenceDetectedPanelWidth > 0.8 and diffeenceDetectedPanelWidth < 1.2):
            print(detectedRectangle[current][0])

            img = cv2.rectangle(img, (detectedRectangle[current][0], detectedRectangle[current][2]), (
                detectedRectangle[current][1], detectedRectangle[current][2] + detectedRectangle[current][4]),
                                (0, 0, 255), 3)
            img = cv2.rectangle(img, (detectedRectangle[next][0], detectedRectangle[next][2]), (
                detectedRectangle[next][1], detectedRectangle[next][2] + detectedRectangle[next][4]),
                                (0, 0, 255), 3)

            print(len(detectedRectangle))

        current += 1
        next += 1
    detectedRectangle.clear()

    # print('stop looking for pic')
    cv2.imshow("Color Tracking", img)
    img = cv2.flip(img, 1)
    cv2.imshow("Blue", res)

    # escape with key "esc"
    if cv2.waitKey(10) & 0xFF == 27:
        video_capture.release()
        cv2.destroyAllWindows()
        break
