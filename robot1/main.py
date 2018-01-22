#! /usr/bin/env python3
import motors

motors.initMotors()

print(">>> Adjusting robot arm (top position)")
motors.moveUpwards()
print(">>> returning to main position")
motors.rotateInitialPos()
print(">>> Releasing the grabber")
motors.release()

print(">>> adjusting robot arm (bottom position)")
motors.moveDownwards()
print(">>> Grabbing item")
motors.grab()

print(">>> adjusting robot arm (top position)")
motors.moveUpwards()
print(">>> rotating to releasing position")
motors.rotateFinalPos()

print(">>> adjusting robot arm (bottom position)")
motors.moveDownwards()
print(">>> releasing the robot arm")
motors.release()
