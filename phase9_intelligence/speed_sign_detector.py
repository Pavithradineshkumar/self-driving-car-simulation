# phase9_intelligence/speed_sign_detector.py

class SpeedSignDetector:

    VALID_SPEEDS = [30, 40, 60, 80, 100]

    def detect(self, speed):

        if speed in self.VALID_SPEEDS:
            return speed

        return None