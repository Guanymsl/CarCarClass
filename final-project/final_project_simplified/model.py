import threading

from screw import screwMotorControl
from motor import motorControl

curSAngle = 0
curMAnlge = 0

def transform() -> tuple[float, float]:
    raise NotImplementedError

def modify(screwMotorAngle, motorAngle):
    screwMotorAngle = min(max(screwMotorAngle, 0), 30)
    motorAngle = min(max(motorAngle, 0), 30)

    screwThread = threading.Thread(target = screwMotorControl, args = (curSAngle, screwMotorAngle))
    motorThread = threading.Thread(target = motorControl, args = (curMAnlge, motorAngle))

    screwThread.start()
    motorThread.start()

    screwThread.join()
    motorThread.join()

    curSAngle, curMAnlge = screwMotorAngle, motorAngle
