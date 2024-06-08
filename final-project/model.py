import threading

from screw import screwMotorControl
from motor import motorControl

def transform(dist: float, width: float) -> float:
    return (dist - 1.5 * width) / 10

def update(_angle: float, _curAngle: tuple[float, float]) -> tuple[float, float]:
    if _angle >= 0:
        sAngle = min(_curAngle[0] + _angle, 30)
        mAngle = max(min(_curAngle[1] - max(0, _curAngle[0] + _angle - 30), 45), sAngle)

    else:
        mAngle = min(_curAngle[1] - _angle, 45)
        sAngle = max(min(_curAngle[0] - max(0, _curAngle[1] - _angle - 45), 30 - mAngle), 0)

    if abs(sAngle - _curAngle[0]) <= 3 and abs(mAngle - _curAngle[1]) <= 3:
        return _curAngle

    modify(_curAngle, (sAngle, mAngle))

    return sAngle, mAngle

def modify(angleI: tuple[float], angelF: tuple[float]) -> None:

    screwThread = threading.Thread(target = screwMotorControl, args = (angleI[0], angelF[0]))
    motorThread = threading.Thread(target = motorControl, args = (angleI[1], angelF[1]))

    screwThread.start()
    motorThread.start()

    screwThread.join()
    motorThread.join()
