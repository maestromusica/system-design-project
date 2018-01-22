import ev3dev.ev3 as ev3
import utils as utils

touchSensor = None
colorSensor = None
grabMotor = None
angleMotor = None
rotateMotor = None

motorsInit = False

def checkInit():
    if not motorsInit:
        initMotors()

def initMotors():
    global touchSensor
    global colorSensor
    global grabMotor
    global angleMotor
    global rotateMotor
    global motorsInit

    touchSensor = ev3.TouchSensor(ev3.INPUT_1)
    colorSensor = ev3.ColorSensor(ev3.INPUT_3)

    grabMotor = ev3.MediumMotor('outA')
    angleMotor = ev3.LargeMotor('outB')
    rotateMotor = ev3.LargeMotor('outC')

    utils.assertAll(
        touchSensor,
        colorSensor,
        grabMotor,
        angleMotor,
        rotateMotor
    )

    motorsInit = True

def grab(pos=-50, speed=300, stop='hold'):
    checkInit()
    grabMotor.run_to_abs_pos(
        position_sp= -50,
        speed_sp=300,
        stop_action='hold'
    )
    utils.waitFor(grabMotor)

def release(pos=20, speed=300, stop='hold'):
    checkInit()
    grabMotor.run_to_abs_pos(
        position_sp=pos,
        speed_sp=speed,
        stop_action=stop
    )
    utils.waitFor(grabMotor)

def rotate(pos=0, speed=300, stop='brake'):
    checkInit()
    rotateMotor.run_to_abs_pos(
        position_sp=pos,
        speed_sp=speed,
        stop_action=stop
    )
    utils.waitFor(rotateMotor)

def rotateInitialPos():
    rotate(pos=45, speed=300, stop='hold')

def rotateFinalPos():
    rotate(pos=-420, stop='hold')

def moveAngle(pos=0, speed=300, stop='brake'):
    checkInit()
    angleMotor.run_to_abs_pos(
        position_sp=pos,
        speed_sp=speed,
        stop_action=stop
    )
    utils.waitFor(angleMotor)

def moveUpwards():
    moveAngle(pos=-90, stop='hold')

def moveDownwards():
    moveAngle(pos=180, stop='hold')
