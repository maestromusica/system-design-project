from queue import Queue

class ActionQueue(Queue):
    def __init__(self):
        super(ActionQueue, self).__init__()
        self._lock = False

    def locked(self):
        return self._lock

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False

    def get(self):
        if self._lock:
            raise ActionQueueLockedException
        else:
            return super(ActionQueue, self).get()



class ActionQueueLockedException(Exception):
    pass
