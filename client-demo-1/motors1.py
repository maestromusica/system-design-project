import ev3dev.ev3 as ev3

a = ev3.MediumMotor(ev3.OUTPUT_A) # Z-axis
b = ev3.LargeMotor(ev3.OUTPUT_B) # grabber
c = ev3.LargeMotor(ev3.OUTPUT_C) # Y-axis
d = ev3.LargeMotor(ev3.OUTPUD_D) # Y-axis

def moveAbsolute(motor, pos, speed, stop='hold'):
    motor.run_to_abs_pos(position_sp=pos, speed_sp=speed, stop_action=stop)

def moveA(pos, speed): moveAbsolute(a, pos, speed)
def moveB(pos, speed): moveAbsolute(b, pos, speed)
def moveC(pos, speed): moveAbsolute(c, pos, speed)
def moveD(pos, speed): moveAbsolute(d, pos, speed)

def moveY(pos, speed):
    moveC(pos, speed)
    moveD(-1*pos, speed)
