# import ev3dev.ev3 as ev3
from utils.map import Map
from utils.types import MotorTypes

class Robot:

    def __init__(self, fileName):
        self.__fileName = fileName + ".txt"
        self.motors = Map()
        self.peripherals = Map()
        self.sensors = Map()

        try:
            f = open(self.__fileName, "r+")
            f.close()
        except:
            fCreate = open(self.__fileName, "w+")
            fCreate.close()

    def setFile(self, fileName):
        self.__fileName = fileName

    def setAsMotor(self, motorName, motorType, motorOutput):
        self.motors[motorName] = motorOutput
        self.peripherals[motorName] = motorOutput

        self.__addDefaultRotation(motorName, 0)

    def setAsSensor(self, sensorName, sensourOutput):
        self.sensors[sensorName] = sensorOutput
        self.peripherals[sensorName] = sensorOutput

    def __addMotorRotation(
        self,
        motorName,
        rotationValue,
        isDefault,
        shouldReplace
    ):
        f = open(self.__fileName, "r+")
        contents = f.read().split('\n')
        output = []
        attributeAdded = False

        for line in contents:
            splitted = line.split(' ')

            if splitted[0] == motorName:
                # if it's default and should replace
                if(splitted[1] == "def" and isDefault and shouldReplace):
                    attributeAdded = True
                    output.append(' '.join(
                        [motorName, "def", str(rotationValue)]
                    ))
                # if it's not default and should replace
                elif(not splitted[1] == "def" and not isDefault and shouldReplace):
                    attributeAdded = True
                    output.append(' '.join([motorName, str(rotationValue)]))
                else:
                    output.append(line)

            else:
                output.append(line)

        if not attributeAdded and isDefault and shouldReplace:
            output.append(' '.join([motorName, "def", str(rotationValue)]))
        elif not attributeAdded and not isDefault and shouldReplace:
            output.append(' '.join([motorName, str(rotationValue)]))

        # put pointer to 0 position
        f.seek(0)
        # delete file contents
        f.truncate()
        # rewrite file contents
        f.write('\n'.join(output))
        f.close()

    def __addNewRotation(self, motorName, rotationValue):
        self.__addMotorRotation(motorName, rotationValue, False, True)

    def __addDefaultRotation(self, motorName, rotationValue):
        self.__addMotorRotation(motorName, rotationValue, True, False)

    def __resetDefaultRotation(self, motorName, rotationValue):
        self.__addMotorRotation(motorName, rotationValue, True, True)

    def moveAngle(self, motorName, moveToAngle):
        newAngle = self.__calculateAngle(motorName, moveToAngle)
        self.__addNewRotation(motorName, moveToAngle)
        print(newAngle)

    def __calculateAngle(self, motorName, moveToAngle):
        f = open(self.__fileName, 'r')
        contents = f.read().split('\n')
        initialValue = None
        lastPosition = None

        # take the current position and calculate where to go To
        for line in contents:
            splitted = line.split(' ')
            if splitted[0] == motorName:
                if splitted[1] == 'def':
                    initialValue = splitted[2]
                else:
                    lastPosition = splitted[1]

        if lastPosition == None:
            newAngle = moveToAngle - int(initialValue)
        else:
            newAngle = moveToAngle - int(lastPosition)

        f.close()
        return newAngle
