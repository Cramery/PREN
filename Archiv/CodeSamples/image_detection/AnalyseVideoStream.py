from WebcamVideoStream import WebcamVideoStream
import pytesseract
import cv2
import logging

# Logger Setup
def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(created)f : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

def main():
    #Select Webcam to Stream from
    vs = WebcamVideoStream(0)
    vs.start()

    #Initialize Config for tesseract
    #tesconfigargs = ('-l digits --psm 10')
    tesconfigargs = '--oem 0 -c tessedit_char_whitelist=0123456789-. --psm 10'

    #Set pytesseract CMD (Windows only)
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

    #Instanciate Logger
    setup_logger('log', r'C:\Temp\ImageAnalysis.csv')
    log = logging.getLogger('log')

    log.info("-------------------------------------Capture started----------------------------------------------")

    while True:

        frame = vs.read()
        cv2.imshow('frame', frame)

        #Color to GrayScale Filter
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #small Gaussian Blur Filter to filter out grainy Stuff
        gauss = cv2.GaussianBlur(gray, (5,5),0)

        #canny detector
        canny = cv2.Canny(gauss,100,200)
        cv2.imshow('canny', canny)

        _, cnts, _= cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]


        ## loop over our contours
        screenCnt = None
        for c in cnts:
            if cv2.contourArea(c) > 1000:

                #approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                #if our approximated contour has four points, then
                #we can assume that we have found our screen
                if len(approx) == 4:
                    screenCnt = approx
                    cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
                    x,y,width,height = cv2.boundingRect(screenCnt)
                    croppedframe = frame[y: y + height , x: x + width] # both opencv and numpy are "row-major", so y goes first

                    digit = pytesseract.image_to_string(croppedframe, config=tesconfigargs)

                    # Print and Log recognized text
                    log.info(digit)
                    break

        cv2.imshow('frame', frame)
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
           break

    #Do Cleanup
    vs.stop()
    cv2.destroyAllWindows()

#Execute Main
if __name__ == '__main__':
    main()
