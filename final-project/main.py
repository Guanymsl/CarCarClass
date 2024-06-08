import time
import cv2

from detect import faceDetection
from model import modify

def main() -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam!")
        return

    cnt = 0
    curAngle = (0, 0)
    modify((0, 0), (0, 0))

    time.sleep(3)
    print(f"Current Angle: {curAngle}")

    while True:
        cnt, curAngle = faceDetection(cap, cnt, curAngle)
        if cnt == 2:
            break

        print(f"Current Angle: {curAngle}")

        time.sleep(5)

    cap.release()

if __name__ == "__main__":
    main()
