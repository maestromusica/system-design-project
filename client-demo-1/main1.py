#! /usr/bin/env python3

from motors1 import *

shouldGrab = True
shouldRelease = False

print("Hello World")

def grab():
    global shouldGrab
    global shouldRelease
    moveY(300, 300)
    waitFor(yax1)
    moveZ(-500, 300)
    waitFor(zax)
    moveAbsolute(grabber, -50, 100)
    waitForStalled(grabber)
    moveZ(0, 300)
    waitFor(zax)
    moveY(-300, 300)
    waitFor(yax1)
    shouldGrab = False
    shouldRelease = True

def release():
    global shouldGrab
    global shouldRelease
    moveZ(-500, 300)
    waitFor(zax)
    moveAbsolute(grabber, 0, 100)
    waitFor(grabber)
    moveZ(0, 300)
    waitFor(zax)
    moveY(0, 300)
    waitFor(yax1)
    shouldRelease = False
    shouldGrab = True

while True:
    if touchGrab.is_pressed and shouldGrab:
        grab()
    if touchRelease.is_pressed and shouldRelease:
        release()
