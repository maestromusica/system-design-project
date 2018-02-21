from action_queue import ActionQueue, ActionQueueLockedException

class Controller:
    def __init__(self):
        # will keep the action queues
        # (either from vision or from the controller)
        self.actionQueues = {}
        # keeps information about the current execution aciton queue
        self.currentExecutionQueue = None

    def addActionQueue(self, tag, actionQueue):
        if tag in self.actionQueues:
            # raise an exception here
            print("tag already in action queues")
            return

        self.actionQueues[tag] = actionQueue

    def changeExecutionQueue(self, tag):
        if tag not in self.actionQueues.keys():
            print("please give a valid tag")
            return
        self.currentExecutionQueue = tag

    def lockCurrentExecutionQueue(self):
        tag = self.currentExecutionQueue
        self.actionQueues[tag].lock()

    def unlockCurrentExecutionQueue(self):
        tag = self.currentExecutionQueue
        self.actionQueues[tag].unlock()

    def nextAction(self):
        tag = self.currentExecutionQueue
        if self.actionQueues[tag].empty():
            return None
        else:
            return self.actionQueues[tag].get()
