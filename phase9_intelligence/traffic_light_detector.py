# phase9_intelligence/traffic_light_detector.py

class TrafficLightDetector:

    def detect(self, state):

        state = state.upper()

        if state not in ["RED", "YELLOW", "GREEN"]:
            state = "UNKNOWN"

        return state