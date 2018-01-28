
class Synchroniser:

    def __init__(self, fileName):
        self._fileName = fileName + ".txt"
        try:
            f = open(self._fileName, "r+")
            f.close()
        except OSError:
            fCreate = open(self._fileName, "w+")
            fCreate.close()

    def setFile(self, fileName):
        self._fileName = fileName + ".txt"

    def setAsMotor(self, motorName, motorType, motorOutput):
        self.motors[motorName] = motorOutput
        self.peripherals[motorName] = motorOutput

        self._addIfNotExists(motorName, 0, True)
        self._addIfNotExists(motorName, 0, False)

    def setAsSensor(self, sensorName, sensorOutput):
        self.sensors[sensorName] = sensorOutput
        self.peripherals[sensorName] = sensorOutput

    def _addIfNotExists(self, attrName, attrValue, isDefault):
        f = open(self._fileName, "r+")
        lines = f.read().split('\n')
        output = []
        found = False

        for line in lines:
            contents = line.split(' ')
            if contents[0] == attrName and (contents[1] == "def") == isDefault:
                found = True
            else:
                output.append(line)

        if not found:
            if isDefault:
                output.append(' '.join([attrName, "def", str(attrValue)]))
            else:
                output.append(' '.join([attrName, str(attrValue)]))

        f.seek(0)
        f.truncate()
        f.write('\n'.join(output))
        f.close()

    def _replaceAttr(self, attrName, attrValue, isDefault):
        f = open(self._fileName, "r+")
        lines = f.read().split('\n')
        output = []

        for line in lines:
            contents = line.split(' ')
            if contents[0] == attrName and (contents[1] == "def") == isDefault:
                # attribute is found and should replace it
                if isDefault:
                    output.append(' '.join([attrName, "def", str(attrValue)]))
                else:
                    output.append(' '.join([attrName, str(attrValue)]))
            else:
                output.append(line)

        f.seek(0)
        f.truncate()
        f.write('\n'.join(output))
        f.close()

    def _getAttributes(self, attributes):
        f = open(self._fileName, "r+")
        lines = f.read().split('\n')
        values = []

        # not the best algorithm at search, but for low N, it's ok.
        for attr in attributes:
            for line in lines:
                contents = line.split(' ')
                if(contents[0] == attr[0]
                        and (contents[1] == "def") == attr[1]):
                    if attr[1]:
                        values.append(int(contents[2]))
                    else:
                        values.append(int(contents[1]))
                    break

        f.close()
        return values

    def _calculateAngle(self, motorName, moveToAngle):
        attributes = [(motorName, True), (motorName, False)]
        vals = self._getAttributes(attributes)

        assert len(attributes) == len(vals), \
            "Error when retrieving values from file. {0} != {1}".format(
                len(attributes),
                len(vals)
            )

        newAngle = (moveToAngle - vals[0]) - vals[1]
        absolutePosition = moveToAngle - vals[0]

        self._replaceAttr(motorName, absolutePosition, isDefault=False)
        return newAngle

    def moveAngle(self, motorName, moveToAngle):
        return self._calculateAngle(motorName, moveToAngle)
