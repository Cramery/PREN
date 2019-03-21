import cv2
import imutils
import numpy as np
import pytesseract as pt

#init
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

signType = None;
signData = None;

#Initialize Config for tesseract
#tesconfigargs = ('-l digits --psm 10')
tesconfigargs = '--oem 0 -c tessedit_char_whitelist=0123456789-. --psm 10'

#Run
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # load the image and resize it to a smaller factor so that the shapes can be approximated better
    resized = imutils.resize(frame, width=300)
    ratio = frame.shape[0] / float(resized.shape[0])

    #Hintergrund ausblenden
    fgmask = fgbg.apply(resized)

    # find contours in the fgmask
    cnts = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #Loop contours
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape has 4 vertices, it is either a square or a rectangle
        if len(approx) == 4:
            # multiply the contour (x, y)-coordinates by the resize ratio, then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

            #determine wheter shape is in the upper or lower half of the image
            # Split Image horizontaly
            splittedImage = np.hsplit(frame, 2)
            if (cv2.pointPolygonTest(c, splittedImage[0], False) > 0):
                #Image is at the top End
                #Haltesignal
                print("Haltesignal")
                signType = 0
            else:
                print("Stopsignal")
                signType = 1

            #Get contour with orginalsize
            screenCnt = cv2.approxPolyDP(c, 0.04 * peri, True)
            x, y, width, height = cv2.boundingRect(screenCnt)

            #Crop Frame
            # both opencv and numpy are "row-major", so y goes first
            croppedframe = frame[y: y + height, x: x + width]

            #ReadSigndata
            signData = pt.image_to_string(croppedframe, config=tesconfigargs)

            print(signData)

    # Display the resulting frame
    cv2.imshow('Frame', frame)
    cv2.imshow('Ohne Hintergrund', fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
