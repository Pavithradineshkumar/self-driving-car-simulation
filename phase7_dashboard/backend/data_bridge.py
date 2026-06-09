# phase7_dashboard/backend/data_bridge.py

import threading
import time
import numpy as np

class DataBridge:
    """
    Thread-safe shared state between:
      - The perception/RL pipeline (writer)
      - The FastAPI WebSocket broadcaster (reader)

    Uses a lock so reads never see a half-written update.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._state = self._default_state()

    def _default_state(self):
        return {
            # Car telemetry
            "speed":          0.0,
            "steer":          0.0,
            "throttle":       0.0,
            "brake":          False,
            "odometer":       0.0,

            # Behavior
            "behavior_state": "IDLE",
            "target_speed":   0.0,

            # Lane
            "center_offset":  0,
            "left_lane":      False,
            "right_lane":     False,

            # Sensors (7 rays, normalized 0–1)
            "sensor_readings": [1.0] * 7,

            # Objects detected
            "detections":     [],

            # Warnings
            "warnings":       [],

            # Phase 9 Intelligence
            "emergency": False,
            "decision": "DRIVE",
            "nearest_distance": None,

            # RL agent
            "epsilon":        1.0,
            "episode":        0,
            "episode_reward": 0.0,
            "q_values":       [0.0, 0.0, 0.0, 0.0],

            # Analytics history (last 200 frames)
            "speed_history":  [],
            "reward_history": [],
            "loss_history":   [],

            # Timestamp
            "ts": time.time(),
        }

    def update(self, patch: dict):
        """Write a partial update. Only provided keys are changed."""
        with self._lock:
            self._state.update(patch)
            self._state["ts"] = time.time()

            # Keep history arrays bounded
            for key in ("speed_history", "reward_history", "loss_history"):
                if key in patch:
                    self._state[key] = self._state[key][-200:]

    def snapshot(self) -> dict:
        """Return a full copy of current state (safe for JSON)."""
        with self._lock:
            return dict(self._state)


# Singleton shared across the entire backend process
bridge = DataBridge()