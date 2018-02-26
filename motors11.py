import ev3dev.ev3 as ev3
from utils.motors import *

yax1 = ev3.LargeMotor(ev3.OUTPUT_A)
yax2 = ev3.LargeMotor(ev3.OUTPUT_B)
zax = ev3.MediumMotor(ev3.OUTPUT_D)
grabber = ev3.LargeMotor(ev3.OUTPUT_C)

yTouchSensor = ev3.TouchSensor(ev3.INPUT_1)
zTouchSensor = ev3.TouchSensor(ev3.INPUT_2)

def resetYAxis():
    pos = 0
    while True:
        if yTouchSensor.value():
            yax1.stop()
            yax2.stop()
            yax1.reset()
            yax2.reset()
            break
        pos -= 100
        moveY(pos, 100)

def resetZAxis():
    zax.run_forever(speed_sp=-100)

    while True:
        # check if stalled is in zax state because the zax could
        # hit something along the Z axis.
        if not zTouchSensor.value() or "stalled" in zax.state:
            zax.stop()
            zax.reset()
            break

def moveGrabber(pos, speed):
    moveAbsolute(grabber, pos, speed, stop='hold')

def moveY(pos, speed):
    moveAbsolute(yax1, pos, speed)
    moveAbsolute(yax2, -1*pos, speed)

def moveZ(pos, speed):
    moveAbsolute(zax, pos, speed)
