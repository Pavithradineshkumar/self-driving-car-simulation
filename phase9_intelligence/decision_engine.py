# phase9_intelligence/decision_engine.py

class DecisionEngine:

    def decide(
        self,
        traffic_light,
        speed_limit,
        emergency
    ):

        if emergency:
            return "EMERGENCY_BRAKE"

        if traffic_light == "RED":
            return "STOP"

        if traffic_light == "YELLOW":
            return "SLOW"

        return "DRIVE"