import ev3dev.ev3 as ev3
from utils.motors import *

yax1 = ev3.LargeMotor(ev3.OUTPUT_A)
yax2 = ev3.LargeMotor(ev3.OUTPUT_B)
zax = ev3.MediumMotor(ev3.OUTPUT_C)
grabber = ev3.LargeMotor(ev3.OUTPUT_D)

touchGrab = ev3.TouchSensor(ev3.INPUT_1)
touchRelease = ev3.TouchSensor(ev3.INPUT_2)

def moveY(pos, speed):
    moveAbsolute(yax1, pos, speed)
    moveAbsolute(yax2, -1*pos, speed)

def moveZ(pos, speed):
    moveAbsolute(zax, pos, speed)
