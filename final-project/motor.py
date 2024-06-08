from gpiozero import Servo

MSERVOPIN = 17
mservo = Servo(MSERVOPIN)

def setAngle(_angle) -> None:
    mservo.value = (_angle / 45) - 1

def motorControl(_angleI, _angleF) -> None:
    setAngle(_angleF)

def mclose() -> None:
    setAngle(0)
    mservo.detach()
