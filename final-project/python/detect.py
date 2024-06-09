import time
import cv2
import os
import numpy as np
import mediapipe as mp

from os.path import exists
from urllib.request import urlretrieve

from model import transform, update

#Model for face detection
if not os.path.exists('./data'):
    os.makedirs('./data')
PROTOTXT = "deploy.prototxt"
CAFFEMODEL = "res10_300x300_ssd_iter_140000.caffemodel"
if not exists(f"./data/{PROTOTXT}") or not exists(f"./data/{CAFFEMODEL}"):
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/{PROTOTXT}", f"./data/{PROTOTXT}")
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/{CAFFEMODEL}", f"./data/{CAFFEMODEL}")
net = cv2.dnn.readNetFromCaffe(prototxt = f"./data/{PROTOTXT}", caffeModel = f"./data/{CAFFEMODEL}")

#Model for eye detection
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(static_image_mode = False, max_num_faces = 1, min_detection_confidence = 0.5)

def detectFace(img: np.ndarray, minConfidence: float) -> np.ndarray:
    (h, w) = img.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detectors = net.forward()

    rects = []

    for i in range(0, detectors.shape[2]):
        confidence = detectors[0, 0, i, 2]
        if confidence < minConfidence:
            continue

        box = detectors[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x0, y0, x1, y1) = box.astype("int")
        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        rects.append((x0, y0, x1 - x0, y1 - y0))

    return rects

def getCenter(landmarks: np.ndarray, shape: np.ndarray) -> tuple[float, float, float, float]:
    xCoords = [int(l.x * shape[1]) for l in landmarks]
    yCoords = [int(l.y * shape[0]) for l in landmarks]
    w = max(xCoords) - min(xCoords)
    h = max(yCoords) - min(yCoords)
    return ((min(xCoords) + max(xCoords)) / 2, (min(yCoords) + max(yCoords)) / 2, w, h)

def detectFeature(faceRoi: np.ndarray) -> tuple[bool, float, float]:
    faceRgb = cv2.cvtColor(faceRoi, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(faceRgb)

    if results.multi_face_landmarks:
        for faceLandmarks in results.multi_face_landmarks:

            leftEyeIndices = mpFaceMesh.FACEMESH_LEFT_EYE
            rightEyeIndices = mpFaceMesh.FACEMESH_RIGHT_EYE
            if len(leftEyeIndices) == 0 or len(rightEyeIndices) == 0:
                return False, None, None

            leftEye = [faceLandmarks.landmark[i] for i, _ in leftEyeIndices]
            rightEye = [faceLandmarks.landmark[i] for i, _ in rightEyeIndices]

            leftEyeCenter = getCenter(leftEye, faceRoi.shape)
            rightEyeCenter = getCenter(rightEye, faceRoi.shape)

            print(leftEyeCenter)
            print(rightEyeCenter)

            if np.abs(leftEyeCenter[1] - rightEyeCenter[1]) > 50 or np.abs(leftEyeCenter[2] - rightEyeCenter[2]) > 15:
                return False, None, None

            return True, leftEyeCenter[2], rightEyeCenter[2]

    return False, None, None

def faceDetection(_cap, _cnt: int, _curAngle: tuple[float, float]) -> tuple[int, float, float]:
    positions = []
    yDistances = []
    eyeWidths = []

    ff = 0

    for _ in range(10):
        if ff >= 3:
            print("Skip this loop!")
            return _cnt + 1, _curAngle

        ret, frame = _cap.read()
        if not ret:
            ff += 1
            continue

        rects = detectFace(frame, 0.5)
        if len(rects) == 0:
            ff += 1
            continue

        centers = np.array([(x + 0.5 * w, y + 0.5 * h) for (x, y, w, h) in rects])
        xCenter = frame.shape[1] / 2
        yCenter = frame.shape[0] / 2
        
        print(xCenter)
        print(yCenter)

        distances = np.abs(centers[:, 0] - xCenter)
        
        print(distances)
        if min(distances) > 150:
            ff += 1
            continue

        roi = rects[np.argmin(distances)]
        faceRoi = frame[roi[1] : roi[1] + roi[3], roi[0] : roi[0] + roi[2]]

        ext, leftWidth, rightWidth = detectFeature(faceRoi)

        if ext:
            positions.append(centers[np.argmin(distances)])
            yDistances.append(centers[np.argmin(distances)][1] - yCenter)
            eyeWidths.append((leftWidth + rightWidth) / 2)

        else:
            ff += 1

        time.sleep(0.2)

    centAvg = np.average(positions, axis = 0)
    xCent, yCent = centAvg[0], centAvg[1]
    print(f"Face Center: (x, y) = ({xCent}, {yCent})")

    distAvg = np.average(yDistances)
    print(f"Vertical Distance: {distAvg}")

    widthAvg = np.average(eyeWidths)
    print(f"Average Eyes Width: {widthAvg}")

    angle = np.floor(transform(distAvg, widthAvg))
    print(f"Angle: {angle}")

    return 0, update(angle, _curAngle)
