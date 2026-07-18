from collections import deque
from datetime import datetime


class EventLogger:

    def __init__(self):
        self.events = deque(maxlen=8)

    def add(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.appendleft(f"[{timestamp}] {message}")

    def get_events(self):
        return list(self.events)