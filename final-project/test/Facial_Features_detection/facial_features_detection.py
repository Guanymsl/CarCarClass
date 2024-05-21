import cv2
import os

# Absolute paths to the cascade files
face_cascade_path = "/Users/guanymsl/Desktop/CarCarClass/final-project/test/Facial_Features_detection/haarcascade_frontalface_default.xml"
eye_cascade_path = "/Users/guanymsl/Desktop/CarCarClass/final-project/test/Facial_Features_detection/haarcascade_eye.xml"

# Load the cascades
face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# Check if the cascade files are loaded properly
if face_cascade.empty():
    raise IOError(f"Error loading face cascade file at {face_cascade_path}")
if eye_cascade.empty():
    raise IOError(f"Error loading eye cascade file at {eye_cascade_path}")

capture = cv2.VideoCapture(0)

try:
    while True:
        _, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_roi = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(face_roi)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    capture.release()
    cv2.destroyAllWindows()
