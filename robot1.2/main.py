#! /usr/env/bin python3
from framework.motors import LargeMotor, MediumMotor
from framwrok.sync import Synchroniser

sync = Synchroniser(fileName="version_0.1")
grabMotor = LargeMotor('outA', sync)
angleMotor = MediumMotor('outB', sync)
