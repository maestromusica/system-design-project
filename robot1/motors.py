import ev3dev.ev3 as ev3
import utils as utils

touchSensor = None
colorSensor = None
grabMotor = None
angleMotor = None
rotateMotor = None

motorsInit = False

def checkInit():
    """Checks if motors are initialised and init them if not."""
    if not motorsInit:
        initMotors()

def initMotors():
    """Initialised motors for the robot arm v1.

    Throws assertion error if one of the sensors / arm
    is not connected.
    """

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
    """ Rotates the grab motor to grab an item

    Arguments:
    pos -- absolute position of the motor (def: -50 deg)
    speed -- speed in tachions (def: 300)
    stop -- stop action to be performed after motor stops (def: 'hold')
    """

    checkInit()
    grabMotor.run_to_abs_pos(
        position_sp= -50,
        speed_sp=300,
        stop_action='hold'
    )
    utils.waitFor(grabMotor)

def release(pos=20, speed=300, stop='hold'):
    """ Rotates the grab motor to release an item

    Arguments:
    pos -- absolute position of the motor (def: 20 deg)
    speed -- speed in tachions (def: 300)
    stop -- stop action to be performed after motor stops (def: 'hold')
    """

    checkInit()
    grabMotor.run_to_abs_pos(
        position_sp=pos,
        speed_sp=speed,
        stop_action=stop
    )
    utils.waitFor(grabMotor)

def rotate(pos=0, speed=300, stop='brake'):
    """ Rotates the arm (doesn't depend on the angle of the arm) (Horizontally).
    Could result in the arm hitting an object.

    Arguments:
    pos -- absolute position of the motor angle (def: 0 deg)
    speed -- speed in tachions (def: 300)
    stop -- stop action (performed after the motor stops) (def: 'brake')
    """

    checkInit()
    rotateMotor.run_to_abs_pos(
        position_sp=pos,
        speed_sp=speed,
        stop_action=stop
    )
    utils.waitFor(rotateMotor)

def rotateInitialPos():
    """Rotates the arm to the initial position: 45 deg"""

    rotate(pos=45, speed=300, stop='hold')

def rotateFinalPos():
    """Rotate the arm to the final position: -420 deg"""

    rotate(pos=-420, stop='hold')

def moveAngle(pos=0, speed=300, stop='brake'):
    """Moves the angle of the arm (Vertically)

    Arguments:
    pos -- absolute position of the motor angle (def: 0 deg)
    speed -- speed in tachions (def: 300)
    stop -- stop action (performed after the motor stops) (def: 'brake')
    Change stop action if you want the angle to remain in place after
    the motor stops executing (stop = 'hold' does that!)
    """

    checkInit()
    angleMotor.run_to_abs_pos(
        position_sp=pos,
        speed_sp=speed,
        stop_action=stop
    )
    utils.waitFor(angleMotor)

def moveUpwards():
    """Moves the arm up vertically"""
    moveAngle(pos=-90, stop='hold')

def moveDownwards():
    """Moves the arm down vertically.

    Used before grabbing or releasing an item
    """

    moveAngle(pos=180, stop='hold')
