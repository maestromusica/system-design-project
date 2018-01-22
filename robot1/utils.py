import time

#
# {param} sensors: sensors array
# {returns} void
# asserts all sensors in sensors array are connected
#
def assertAll(*sensors):
    for sensor in sensors:
        assert sensor.connected == True, \
        "{0} at {1} is not connected".format(
            sensor.__class__.__name__,
            sensor.address()
        )
    return


def waitFor(sensor, waitForNext=True):
    time.sleep(0.1)
    while "running" in sensor.state:
        time.sleep(0.1)
    if waitForNext:
        time.sleep(0.5)
