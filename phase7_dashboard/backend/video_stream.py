# phase7_dashboard/backend/video_stream.py

import cv2
import threading
import numpy as np
from phase7_dashboard.backend.constants import MJPEG_QUALITY
from phase7_dashboard.backend.frame_bridge import frame_bridge

class VideoStream:
    """
    Captures frames from a camera or video file and serves them
    as MJPEG (Motion JPEG) — a simple format where each frame is
    sent as an individual JPEG over a persistent HTTP connection.

    The frontend <img> tag points to the /video endpoint and
    automatically displays each pushed frame.
    """

    def __init__(self, source=0):
        self.source   = source
        self.cap      = None
        self._frame   = None
        self._lock    = threading.Lock()
        self._running = False

    def start(self):
        if self.source is None:
           print("[VideoStream] Camera disabled.")
           return

        self.cap = cv2.VideoCapture(self.source)
        self._running = True

        t = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )
        t.start()

    def _capture_loop(self):
        """Continuously read frames into self._frame."""
        while self._running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                with self._lock:
                    self._frame = frame

    def get_frame(self):
        frame = frame_bridge.get()

        if frame is None:
            return None

        _, buf = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, MJPEG_QUALITY]
        )

        return buf.tobytes()

    def stop(self):
        self._running = False
        if self.cap:
            self.cap.release()


# Singleton video stream
video_stream = VideoStream(source=None)