class AnalyticsEngine:

    def __init__(self):

        self.speed_history = []
        self.steer_history = []
        self.throttle_history = []
        self.brake_history = []

    def update(
        self,
        speed,
        steer,
        throttle,
        brake
    ):

        self.speed_history.append(speed)
        self.steer_history.append(steer)
        self.throttle_history.append(throttle)
        self.brake_history.append(brake)

        max_points = 300

        if len(self.speed_history) > max_points:
            self.speed_history.pop(0)

        if len(self.steer_history) > max_points:
            self.steer_history.pop(0)

        if len(self.throttle_history) > max_points:
            self.throttle_history.pop(0)

        if len(self.brake_history) > max_points:
            self.brake_history.pop(0)

    def latest(self):

        return {
            "speed": self.speed_history[-1]
                     if self.speed_history else 0,

            "steer": self.steer_history[-1]
                     if self.steer_history else 0,

            "throttle": self.throttle_history[-1]
                        if self.throttle_history else 0,

            "brake": self.brake_history[-1]
                     if self.brake_history else False
        }