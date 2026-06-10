class DecisionEngine:

    def decide(self, distance):

        if distance is None:
            return "DRIVE"

        if distance < 5:
            return "EMERGENCY_BRAKE"

        if distance < 8:
            return "STOP"

        if distance < 15:
            return "SLOW_DOWN"

        return "DRIVE"