import ev3dev.ev3 as ev3
from robot import Robot
from utils.types import MotorTypes
from utils import motors as motorUtils

r = Robot("version_1.1")

r.setAsMotor("rotateMotor", MotorTypes, "outB")
rotateMotor = ev3.LargeMotor("outB")

def rotate(pos, speed=300, stop='brake'):
    newPos = r.moveAngle("rotateMotor", pos)
    rotateMotor.run_to_abs_pos(
        position_sp=newPos,
        speed_sp=speed,
        stop_action=stop
    )
    motorUtils.waitFor(rotateMotor)
