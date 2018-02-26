from queue import Queue

class ActionQueue(Queue):
    """Defines the class to be used in the controller to store actions.
    Actions are performed on the EV3. The state of the action queue reflects
    the state of the EV3 robot.

    Possible states:
    - RUNNING: the current queue is on the main execution thread. The ev3 will
    perform actions from this queue
    - STOPPED: the queue is locked, and the ev3 doesn't perform any actions
    - PENDING: the queue will send an action to the ev3 immediately after the
    current one finishes
    - WAITING: the queue waits for the current action that performs on the ev3
    to finish

    Two execution modes:
    - CASCADE: when the ev3 finished an action, if the queue is not STOPPED,
    the next action is sent immediately
    - CONTINUOUS: the next action is only sent if "next" is pressed on the client
    """
    def __init__(self, running=False, locked=False, pending=True, waiting=False):
        super(ActionQueue, self).__init__()
        # init the state dictionary (could be just an array)
        # but it is simpler in the future to store it as a dict
        self.state = ActionQueueState(
            running=running,
            locked=locked,
            waiting=waiting,
            pending=pending)


    def locked(self):
        return self.state.locked

    def running(self):
        return self.state.running

    def pending(self):
        return self.state.pending

    def waiting(self):
        return self.state.waiting

    def lock(self):
        self.state.locked = True

    def unlock(self):
        self.state.locked = False

    def putOnExecutionThread(self):
        self.state.running = True

    def removeFromExecutionThread(self):
        self.state.running = False

    def get(self):
        if self.state.locked:
            raise ActionQueueLockedException
        else:
            return super(ActionQueue, self).get()

    def removeFirstElement(self):
        # call get from super class because this removes
        # the first element regardless if the queue is locked or not!
        super(ActionQueue, self).get()

    def remove(self, position):
        if position < 0 or position >= self.__len__():
            return None
        else:
            i = 0
            elementsBefore = Queue()
            # remove elements before position
            while i < position:
                el = super(ActionQueue, self).get()
                elementsBefore.put(el)
                i += 1
            super(ActionQueue, self).get()
            # remove elements after position
            while self.__len__() > 0:
                el = super(ActionQueue, self).get()
                elementsBefore.put(el)
            # add elements back in the queue
            # the queue, by now, should be empty
            while len(elementsBefore.queue) > 0:
                el = elementsBefore.get()
                super(ActionQueue, self).put(el)

            return True

    def __str__(self):
        return self.queue.__str__()

    def __len__(self):
        return self.queue.__len__()


class ActionQueueState():
    # # action queue is stopped from executing
    # STOPPED = "STOPPED"
    # # action queue is on the current execution thread
    # RUNNING = "RUNNING"
    # # action queue should send next action after the current one is finished
    # PENDING = "PENDING"
    # # action queue waits for ev3 to finish current action
    # WAITING = "WAITING"
    def __init__(self, running, locked, waiting, pending):
        self.running = running
        self.locked = locked
        self.waiting = waiting
        self.pending = pending

    def __str__(self):
        str = "["
        if self.running:
            str += "RUNNING, "
        if self.locked:
            str += "LOCKED, "
        if self.waiting:
            str += "WAITING, "
        if self.pending:
            str += "PENDING"
        str += "]"
        return str

class ActionQueueLockedException(Exception):
    pass
