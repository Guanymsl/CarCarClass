import time
import spidev
import numpy as np
import RPi.GPIO as GPIO

from model import Angle, modify

SW_PIN = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def readAdc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def readJoystick():
    xVal = readAdc(0)
    yVal = readAdc(1)
    swVal = GPIO.input(SW_PIN)
    return xVal, yVal, swVal

def manualControl(cur: Angle):
    try:
        x, y, sw = readJoystick()
        if np.abs(x - 512) < 10 and np.abs(y - 512) < 10 and sw == 0:
            modify(0, 0)
            time.sleep(0.5)

        else:
            screwMotorAngle, motorAngle = cur.getCurAngle()
            modify(screwMotorAngle + (x - 512) / 256, motorAngle + (y - 512) / 256, cur)
            time.sleep(0.1)

    finally:
        GPIO.cleanup()
