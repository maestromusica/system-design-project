import time
import ev3dev.ev3 as ev3

a = ev3.LargeMotor(ev3.OUTPUT_A)
b = ev3.LargeMotor(ev3.OUTPUT_B)

motorStopper = ev3.TouchSensor(ev3.INPUT_1)

def moveA(pos, speed=400):
    a.run_to_abs_pos(position_sp=pos, speed_sp=speed, stop_action='hold')

def moveB(pos, speed=400):
    b.run_to_abs_pos(position_sp=pos, speed_sp=speed, stop_action='hold')

def moveX(pos, speed):
    moveA(pos, speed)
    moveB(pos, speed)

def moveTimed(motor, time, speed):
    motor.run_timed(time_sp=time, speed_sp=speed)

def resetXAxis():
    while True:
        if motorStopper.input():
            a.stop()
            b.stop()
            break
        moveTimed(a, 10, 400)
        moveTimed(b, 10, 400)
        time.wait(5)
