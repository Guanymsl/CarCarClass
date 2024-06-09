from gpiozero import Servo

mservo = Servo(17)

def setAngle(_angle) -> None:
    mservo.value = (_angle / 45) - 1

def motorControl(_angleI, _angleF) -> None:
    setAngle(_angleF)
    print("Setting Motor!")
    
def mclose() -> None:
    setAngle(0)
    mservo.close()
