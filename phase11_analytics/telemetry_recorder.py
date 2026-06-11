import json
import os
from datetime import datetime


class TelemetryRecorder:

    def __init__(self):

        self.log_file = os.path.join(
            os.path.dirname(__file__),
            "logs",
            "drive_log.json"
        )

    def record(
        self,
        speed,
        steer,
        throttle,
        brake
    ):

        entry = {
            "timestamp": datetime.now().isoformat(),
            "speed": speed,
            "steer": steer,
            "throttle": throttle,
            "brake": brake
        }

        try:

            with open(self.log_file, "r") as f:
                data = json.load(f)

        except Exception:
            data = []

        data.append(entry)

        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=4)