import threading

from screw import screwMotorControl
from motor import motorControl

class Angle():
    def __init__(self):
        self.screwMotorAngle, self.motorAngle = 0, 0
    def getCurAngle(self) -> tuple[float, float]:
        return (self.screwMotorAngle, self.motorAngle)

def transform() -> tuple[float, float]:
    raise NotImplementedError

def modify(screwMotorAngle, motorAngle, cur: Angle):
    screwMotorAngle = min(max(screwMotorAngle, 0), 30)
    motorAngle = min(max(motorAngle, 0), 30)

    screwThread = threading.Thread(target = screwMotorControl, args = (cur.screwMotorAngle, screwMotorAngle))
    motorThread = threading.Thread(target = motorControl, args = (cur.motorAngle, motorAngle))

    screwThread.start()
    motorThread.start()

    screwThread.join()
    motorThread.join()

    cur.screwMotorAngle, cur.motorAngle = screwMotorAngle, motorAngle
