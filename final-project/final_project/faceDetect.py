import time
import cv2
import numpy as np

import model

def detectFace(net, img: np.ndarray, minConfidence: float) -> np.ndarray:
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
        rects.append((x0, y0, x1 - x0, y1 - y0))

    return rects

def detectFeature() -> bool:
    raise NotImplementedError

def faceDetection(net, cap, cur):
    positions = []
    cnt = 0

    for _ in range(10):
        if cnt >= 3:
            return

        ret, frame = cap.read()
        if not ret:
            cnt += 1
            continue

        rects = detectFace(net, frame, 0.5)
        if len(rects) == 0 or not detectFeature():
            cnt += 1
            continue

        centers = np.array([(x + 0.5 * w, y + 0.5 * h) for (x, y, w, h) in rects])

        xCenter = frame.shape[1] / 2
        distances = np.abs(centers[:, 0] - xCenter)
        positions.append(centers[np.argmin(distances)])

        time.sleep(0.2)

    Avg = np.average(positions, axis = 0)
    wAvg, hAvg = Avg[0], Avg[1]
    screwMotorAngle, motorAngle = model.transform(wAvg, hAvg)
    model.modify(screwMotorAngle, motorAngle, cur)
