#! /usr/env/bin python3
from robot import Robot
from utils.types import MotorTypes

r = Robot("version_1.2")

def x():
    r.setAsMotor("grabMotor", MotorTypes.MEDIUM, 'outA')
    r.setAsMotor("angleMotor", MotorTypes.LARGE, 'outB')
    r.setAsMotor("rotateMotor", MotorTypes.LARGE, 'outC')
