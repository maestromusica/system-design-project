import ev3dev.ev3 as ev3
from utils.motors import *

yax1 = ev3.LargeMotor(ev3.OUTPUT_A)
yax2 = ev3.LargeMotor(ev3.OUTPUT_B)
zax = ev3.MediumMotor(ev3.OUTPUT_D)
grabber = ev3.LargeMotor(ev3.OUTPUT_C)

touchSensor = ev3.TouchSensor(ev3.INPUT_1)

# def resetYAxis():
#     pos = 0
#     while True:
#         if touchSensor.is_pressed == 1:
#             yax1.stop()
#             yax2.stop()
#             yax1.reset()
#             yax2.reset()
#             break
#         pos -= 100
#         moveY(pos,200)

def resetYAxis():
    yax1.run_forever(speed_sp=100)
    yax2.run_forever(speed_sp=-100)

    while True:
        if touchSensor.is_pressed == 1:
            yax1.stop()
            yax2.sotp()
            yax1.reset()
            yax2.reset()
            break

def moveGrabber(pos, speed):
    moveAbsolute(grabber, pos, speed, stop='hold')

def moveY(pos, speed):
    moveAbsolute(yax1, pos, speed)
    moveAbsolute(yax2, -1*pos, speed)

def moveZ(pos, speed):
    moveAbsolute(zax, pos, speed)
