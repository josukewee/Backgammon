from collections import deque


class eventHandler:
    def __init__(self):
        self.queue = []

    def append(self, event):
        if event is not None:  # avoid appending None
            self.queue.append(event)

    def pop_event(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def empty_events(self):
        return len(self.queue) == 0


