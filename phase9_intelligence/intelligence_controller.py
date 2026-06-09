class IntelligenceController:

    def __init__(self):
        self.traffic_light = "GREEN"
        self.speed_limit = 60
        self.emergency = False

    def update(self,
               traffic_light=None,
               speed_limit=None,
               emergency=None):

        if traffic_light is not None:
            self.traffic_light = traffic_light

        if speed_limit is not None:
            self.speed_limit = speed_limit

        if emergency is not None:
            self.emergency = emergency

    def get_state(self):

        return {
            "traffic_light": self.traffic_light,
            "speed_limit": self.speed_limit,
            "emergency": self.emergency
        }