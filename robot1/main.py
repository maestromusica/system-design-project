#! /usr/bin/env python3
import utils.motors as motorUtils
import ev3dev.ev3 as ev3

motorA = ev3.LargeMotor(ev3.OUTPUT_A)
motorB = ev3.LargeMotor(ev3.OUTPUT_B)
