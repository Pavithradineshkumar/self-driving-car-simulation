import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from phase8_deployment.ipc.publisher import publisher

sample = {
    "speed": 25.0,
    "steer": 0.2,
    "throttle": 0.7,
    "brake": False,
    "odometer": 123.4
}

publisher.publish(sample)

print("Telemetry test message sent.")