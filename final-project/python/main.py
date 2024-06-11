import time
import cv2
import serial

from detect import faceDetection

'''arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(3)
def sendData(data) -> None:
    print(f"data = {data}")
    arduino.write((data + '\n').encode())

def getStr(_angle: tuple[float, float]) -> str:
    encode = int(_angle[0] * 100 + _angle[1])
    return str(encode).zfill(4)'''

def main() -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam!")
        return

    time.sleep(5)

    cnt = 0
    curAngle = (0, 30)
    #sendData("0030")
    print(f"Current Angle: {curAngle}")

    while True:
        cnt, curAngle = faceDetection(cap, cnt, curAngle)
        if cnt == 5:
            break

        #sendData(getStr(curAngle))
        print(f"Current Angle: {curAngle}")

        time.sleep(5)

    #sendData("0000")
    cap.release()
    #arduino.close()

if __name__ == "__main__":
    main()
