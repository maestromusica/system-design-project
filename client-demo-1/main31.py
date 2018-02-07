#! /usr/bin/env python3
from motors31 import *

upTurn = True
downTurn = False

while True:
    print(touchUp.is_pressed)
    print(touchDown.is_pressed)
    if touchUp.is_pressed and upTurn:
        moveX(-1200, 300)
        waitFor(xax1)
        upTurn = False
        downTurn = True
    elif touchDown.is_pressed and downTurn:
        moveX(0, 300)
        waitFor(xax1)
        downTurn = False
        upTurn = True
