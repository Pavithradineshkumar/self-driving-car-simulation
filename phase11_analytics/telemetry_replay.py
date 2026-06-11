import json
import os


class TelemetryReplay:

    def __init__(self):

        self.log_file = os.path.join(
            os.path.dirname(__file__),
            "logs",
            "drive_log.json"
        )

    def load(self):

        try:

            with open(self.log_file, "r") as f:
                return json.load(f)

        except Exception:

            return []

    def replay(self):

        data = self.load()

        for frame in data:

            yield frame