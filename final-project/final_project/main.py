import time
import cv2
import RPi.GPIO as GPIO
from os.path import exists
from urllib.request import urlretrieve

from model import Angle, modify
from manual import manualControl
from faceDetect import faceDetection

MODE = "Detection"
BUTTON_PIN = None

PROTOTXT = "deploy.prototxt"
CAFFEMODEL = "res10_300x300_ssd_iter_140000.caffemodel"
if not exists(f"./{PROTOTXT}") or not exists(f"./{CAFFEMODEL}"):
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/{PROTOTXT}", PROTOTXT)
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/{CAFFEMODEL}", CAFFEMODEL)

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def modeSelection(_mode: str) -> tuple[str, bool]:
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        newMode = "Manual" if _mode == "Detection" else "Detection"
        return newMode, True
    return _mode, False

def main(mode: str = MODE):
    net = cv2.dnn.readNetFromCaffe(prototxt = PROTOTXT, caffeModel = CAFFEMODEL)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam!")
        return

    setupGPIO()
    modify(0, 0)
    cur = Angle()

    try:
        while True:
            mode, switch = modeSelection(mode)
            if switch:
                time.sleep(0.5)

            if mode == "Detection":
                faceDetection(net, cap, cur)
                time.sleep(10)

            elif mode == "Manual":
                manualControl(cur)

    except:
        print("Some errors have occurred!")

    finally:
        GPIO.cleanup()
        cap.release()

if __name__ == "__main__":
    main()
