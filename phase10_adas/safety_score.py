class SafetyScore:

    def calculate(
        self,
        collision_state,
        lane_warning,
        emergency
    ):

        score = 100

        if collision_state == "WARNING":
            score -= 20

        elif collision_state == "CRITICAL":
            score -= 40

        if lane_warning:
            score -= 15

        if emergency:
            score -= 25

        return max(score, 0)