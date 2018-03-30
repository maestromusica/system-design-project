class Controller:
    def __init__(self):
        # will keep the action queues
        # (either from vision or from the controller)
        self.actionQueues = {}
        # keeps information about the current execution thread
        self.currentExecThreadTag = None
        self.visionState = {
            "processingImg": False,
            "sorting": False
        }

    def addActionQueue(self, tag, actionQueue):
        if tag in self.actionQueues:
            # raise an exception here
            print("tag already in action queues")
            return

        self.actionQueues[tag] = actionQueue

    def changeExecutionQueue(self, tag):
        if tag not in self.actionQueues:
            print("please give a valid tag")
            return False
        self.currentExecThreadTag = tag
        self.actionQueues[tag].putOnExecutionThread()

        for _tag in self.actionQueues:
            if not _tag == tag:
                self.actionQueues[_tag].removeFromExecutionThread()

        return True

    def lockCurrentExecutionThread(self):
        tag = self.currentExecThreadTag
        self.actionQueues[tag].lock()

    def unlockCurrentExecutionThread(self):
        tag = self.currentExecThreadTag
        self.actionQueues[tag].unlock()

    def nextAction(self):
        tag = self.currentExecThreadTag
        if self.actionQueues[tag].empty():
            return None
        else:
            return self.actionQueues[tag].queue[0]

    def removeFirstAction(self):
        tag = self.currentExecThreadTag
        if self.actionQueues[tag].empty():
            # should return an error
            return
        else:
            self.actionQueues[tag].removeFirstElement()
            return

    def currentExecutionThread(self):
        if self.currentExecThreadTag is None:
            return None
        elif self.currentExecThreadTag in self.actionQueues:
            return self.actionQueues[self.currentExecThreadTag]
