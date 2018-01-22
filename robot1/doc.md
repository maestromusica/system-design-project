1. SSH to the robot (on DICE):

`ssh robot@ev3dev`

1. Move robot1 folder to EV3 (on DICE):

`scp -r robot1 robot@ev3dev:/robot/home`

1. and run main.py (on the SSH-ed EV3)

`./robot1/main.py`

1. (if main.py is not executable `chmod +x ./robot1/main.py`)

---

`main.py` only runs the functions defined in `motors.py`.
`motors.py` defines several functions to manipulate the robotic arm
(grab, release, rotate, moveAngle etc.). Read the docs from each function to get familiar with them.
