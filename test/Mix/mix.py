import cv2
import time
import numpy as np
import mediapipe as mp
from imutils.video import WebcamVideoStream

from os.path import exists
from urllib.request import urlretrieve

PROTOTXT = "deploy.prototxt"
CAFFEMODEL = "res10_300x300_ssd_iter_140000.caffemodel"
if not exists(f"./{PROTOTXT}") or not exists(f"./{CAFFEMODEL}"):
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/{PROTOTXT}", PROTOTXT)
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/{CAFFEMODEL}", CAFFEMODEL)
face_net = cv2.dnn.readNetFromCaffe(prototxt = f"./{PROTOTXT}", caffeModel = f"./{CAFFEMODEL}")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def get_bounding_box(landmarks, shape):
    x_coords = [int(l.x * shape[1]) for l in landmarks]
    y_coords = [int(l.y * shape[0]) for l in landmarks]
    return (min(x_coords), min(y_coords)), (max(x_coords), max(y_coords))

def detect_face_and_eyes(image):
    h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    rects = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            rects.append((startX, startY, endX - startX, endY - startY))

            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

    centers = np.array([(x + 0.5 * w, y + 0.5 * h) for (x, y, w, h) in rects])

    xCenter = image.shape[1] / 2
    distances = np.abs(centers[:, 0] - xCenter)

    roi = rects[np.argmin(distances)]
    face_roi = image[roi[1] : roi[1] + roi[3], roi[0] : roi[0] + roi[2]]

    face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(face_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            left_eye_indices = mp_face_mesh.FACEMESH_LEFT_EYE
            right_eye_indices = mp_face_mesh.FACEMESH_RIGHT_EYE
            left_eye = [face_landmarks.landmark[i] for i, _ in left_eye_indices]
            right_eye = [face_landmarks.landmark[i] for i, _ in right_eye_indices]

            left_eye_bb = get_bounding_box(left_eye, face_roi.shape)
            right_eye_bb = get_bounding_box(right_eye, face_roi.shape)

            cv2.rectangle(face_roi, left_eye_bb[0], left_eye_bb[1], (255, 0, 0), 2)
            cv2.rectangle(face_roi, right_eye_bb[0], right_eye_bb[1], (255, 0, 0), 2)

    cv2.imshow("Image", image)

def main():
    vs = WebcamVideoStream().start()
    time.sleep(2.0)

    while True:
        frame = vs.read()
        detect_face_and_eyes(frame)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

if __name__ == '__main__':
    main()
