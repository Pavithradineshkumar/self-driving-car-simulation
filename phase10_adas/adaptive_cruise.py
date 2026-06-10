class AdaptiveCruiseControl:

    def get_target_speed(self, distance):

        if distance is None:
            return 5.0

        if distance > 40:
            return 5.0

        if distance > 25:
            return 3.5

        if distance > 15:
            return 2.0

        if distance > 8:
            return 1.0

        return 0.0