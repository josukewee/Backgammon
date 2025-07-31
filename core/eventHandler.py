from collections import deque


class eventHandler:
    def __init__(self):
        self._queue = deque()

    def pop_event(self):
        self._queue.pop()

    def append(self, event):
        self._queue.append(event)
        

