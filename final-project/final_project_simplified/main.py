import time
import cv2

from detect import faceDetection

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam!")
        return

    cnt = 0
    while True:
        cnt = faceDetection(cap, cnt)
        if cnt == 2:
            break

        time.sleep(5)

    cap.release()

if __name__ == "__main__":
    main()
