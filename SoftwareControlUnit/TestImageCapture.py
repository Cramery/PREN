import time
import io
import cv2
from picamera import PiCamera

def CaptureStream(getTopImages):
    streamCapture = []
    sequenceLength = 1
    captureSequence = [io.BytesIO() for i in range(sequenceLength)]
    time.sleep(0.07)
    with PiCamera(resolution=(640, 480)) as camera:
        camera.capture_sequence(
            captureSequence, format='jpeg', use_video_port=True)
        for frame in captureSequence:
            image = ioBytesToNpArray(frame)
            streamCapture.append(__cropImage(image, getTopImages))
    return streamCapture

def ioBytesToNpArray(stream):
    stream.seek(0)
    file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

def __cropImage(img, getTopImages = True):
    # get width and height of image
    y, x = img.shape[:2]
    # crop top left
    if(getTopImages):
        return img[0:y // 2, 0:x // 2]
    else:
        return img[y // 2:y, 0:x // 2]

def main():
    print("Software started")
    CaptureStream(True)

if __name__ == "__main__":
    main()