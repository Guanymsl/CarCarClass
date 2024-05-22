import cv2
import time
import numpy as np
from imutils.video import WebcamVideoStream

net = cv2.dnn.readNetFromCaffe('./model/deploy.prototxt', './model/res10_300x300_ssd_iter_140000.caffemodel')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_faces_and_eyes(image):
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            roi = image[startY:endY, startX:endX]

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

    cv2.imshow("Image", image)

def main():
    vs = WebcamVideoStream().start()
    time.sleep(2.0)

    while True:
        frame = vs.read()
        detect_faces_and_eyes(frame)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

if __name__ == '__main__':
    main()