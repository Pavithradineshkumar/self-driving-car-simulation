import threading

class FrameBridge:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()

    def update(self, frame):
        with self.lock:
            self.frame = frame.copy()

    def get(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

frame_bridge = FrameBridge()