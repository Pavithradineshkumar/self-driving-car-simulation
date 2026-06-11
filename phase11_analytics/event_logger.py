import json
import os


class EventLogger:

    def __init__(self):

        self.log_file = os.path.join(
            os.path.dirname(__file__),
            "logs",
            "events.json"
        )

        if not os.path.exists(self.log_file):

            with open(self.log_file, "w") as f:
                json.dump([], f)

    def log(self, event):

        try:

            with open(self.log_file, "r") as f:
                data = json.load(f)

        except:
            data = []

        data.append(event)

        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=4)