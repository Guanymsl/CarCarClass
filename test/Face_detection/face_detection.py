import cv2
import time
import numpy as np

from os.path import exists
from urllib.request import urlretrieve
from imutils.video import WebcamVideoStream

PROTOTXT = "deploy.prototxt"
CAFFEMODEL = "res10_300x300_ssd_iter_140000.caffemodel"

if not exists(f"./{PROTOTXT}") or not exists(f"./{CAFFEMODEL}"):
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/{PROTOTXT}", PROTOTXT)
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/{CAFFEMODEL}", CAFFEMODEL)

net = cv2.dnn.readNetFromCaffe(prototxt=PROTOTXT, caffeModel=CAFFEMODEL)

def detect(img, min_confidence=0.5):
    (h, w) = img.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detectors = net.forward()

    rects = []

    for i in range(0, detectors.shape[2]):
        confidence = detectors[0, 0, i, 2]
        if confidence < min_confidence:
            continue

        box = detectors[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x0, y0, x1, y1) = box.astype("int")
        rects.append((x0, y0, x1 - x0, y1 - y0))

    return rects

def main():
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)

    while True:
        ret, frame = vs.read()
        if ret:
            rects = detect(frame, 0.5)

            for rect in rects:
                (x, y, w, h) = rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

if __name__ == '__main__':
    main()