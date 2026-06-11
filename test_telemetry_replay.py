from phase11_analytics.telemetry_replay import TelemetryReplay

replay = TelemetryReplay()

for frame in replay.replay():

    print(frame)

    break