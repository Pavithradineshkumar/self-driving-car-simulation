class AlertManager:

    def check(
        self,
        lane_warning,
        nearest_distance,
        camera_ok=True
    ):

        alerts = []

        if lane_warning:
            alerts.append("⚠ Lane Lost")

        if nearest_distance is not None and nearest_distance < 30:
            alerts.append("⚠ Obstacle Ahead")

        if not camera_ok:
            alerts.append("⚠ Camera Disconnected")

        return alerts