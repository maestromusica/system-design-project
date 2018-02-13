import time
import ev3dev.ev3 as ev3
from utils.motors import *

xax1 = ev3.LargeMotor(ev3.OUTPUT_A)
xax2 = ev3.LargeMotor(ev3.OUTPUT_D)
touchSensor = ev3.TouchSensor(ev3.INPUT_1)

# def moveA(pos, speed=400):
#     a.run_to_abs_pos(position_sp=pos, speed_sp=speed, stop_action='hold')
#
# def moveB(pos, speed=400):
#     b.run_to_abs_pos(position_sp=pos, speed_sp=speed, stop_action='hold')

def resetXAxis():
    pos = 0
    while True:
        if touchSensor.is_pressed == 1:
            xax1.stop()
            xax2.stop()
            xax1.reset()
            xax2.reset()
            break
        pos -= 100
        moveX(pos,300)

def moveX(pos, speed):
    moveAbsolute(xax1, pos, speed)
    moveAbsolute(xax2, pos, speed)
#
# def moveTimed(motor, time, speed):
#     motor.run_timed(time_sp=time, speed_sp=speed)
#
# def resetXAxis():
#     while True:
#         if motorStopper.input():
#             a.stop()
#             b.stop()
#             break
#         moveTimed(a, 10, 400)
#         moveTimed(b, 10, 400)
#         time.wait(5)
