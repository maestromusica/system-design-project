import time

#
# {param} sensors: sensors array
# {returns} void
# asserts all sensors in sensors array are connected
#
def assertAll(*sensors):
    """ Asserts all sensors / motors are connected.

    Arguments:
    *sensors -- variable list of arguments of sensors / motors
    """
    for sensor in sensors:
        assert sensor.connected == True, \
        "{0} at {1} is not connected".format(
            sensor.__class__.__name__,
            sensor.address()
        )
    return


def waitFor(sensor, waitForNext=True):
    """ Waits for motor / sensor to stop running.
    If waitForNext is False, after the motor stops, it doesn't wait for 0.5 sec

    Arguments:
    sensor -- specifies for what sensor / motor to be waiting for 
    waitForNext -- specifies if function should wait 0.5 sec after
    the motor stops. (def True)
    """

    time.sleep(0.1)
    while "running" in sensor.state:
        time.sleep(0.1)
    if waitForNext:
        time.sleep(0.5)
