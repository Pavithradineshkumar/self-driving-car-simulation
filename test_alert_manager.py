from phase11_analytics.alert_manager import AlertManager

am = AlertManager()

alerts = am.check(
    lane_warning=True,
    nearest_distance=20,
    camera_ok=False
)

print(alerts)