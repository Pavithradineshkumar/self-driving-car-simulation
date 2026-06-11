from phase11_analytics.telemetry_recorder import TelemetryRecorder

rec = TelemetryRecorder()

rec.record(
    speed=5,
    steer=1.2,
    throttle=0.4,
    brake=False
)

print("Telemetry recorded.")