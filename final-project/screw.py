import numpy as np
from gpiozero import Servo

SSERVOPIN = 18
sservo = Servo(SSERVOPIN)
curX = 0

def setAngle(_dx) -> None:
    curX += _dx

def getX(_angle) -> float:
    return 15 - np.sqrt(225 - 400 * np.sin(np.radians(_angle)))

def screwMotorControl(_angleI, _angleF) -> None:
    dx = getX(_angleF) - getX(_angleI)
    setAngle(dx)

def sclose() -> None:
    setAngle(0)
    sservo.detach()
