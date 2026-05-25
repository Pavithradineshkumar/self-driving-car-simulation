from constants import *


class AIDriver:
    """
    Rule-based autonomous controller.
    Uses the sensor readings (7 normalized values) to decide
    speed and steering each frame.

    This is intentionally simple — it's the baseline we replace
    with a neural network in Phase 5 and an RL agent in Phase 6.

    Sensor layout (NUM_RAYS = 7):
        Index:  0    1    2    3    4    5    6
        Angle: -90  -60  -30   0   +30  +60  +90
        Side:  Left                        Right

    Reading of 1.0 = clear space, 0.0 = obstacle right there.
    """

    def __init__(self):
        self.mode = "AI"    # "AI" or "MANUAL" — toggled by user in main.py

    def decide(self, sensor_readings):
        """
        Given sensor readings, return (steer, accelerate, brake).

        steer       : float, negative = left, positive = right
        accelerate  : bool
        brake       : bool
        """
        if len(sensor_readings) != NUM_RAYS:
            # Fallback: go straight
            return 0.0, True, False

        # Split rays into left half, center, right half
        mid   = NUM_RAYS // 2             # Index 3 (forward ray)
        left  = sensor_readings[:mid]     # Indices 0–2
        center = sensor_readings[mid]     # Index 3
        right = sensor_readings[mid+1:]   # Indices 4–6

        # ── 1. Emergency brake ──────────────────────────────────
        # If the forward ray is very short, stop
        forward_clear = center * RAY_LENGTH   # pixels of clearance ahead
        if forward_clear < AI_BRAKE_THRESHOLD:
            return 0.0, False, True

        # ── 2. Steering logic ───────────────────────────────────
        # Average clearance on each side
        avg_left  = sum(left)  / len(left)    # Higher = more space on left
        avg_right = sum(right) / len(right)   # Higher = more space on right

        steer = 0.0

        if forward_clear < AI_STEER_THRESHOLD:
            # Obstacle ahead — steer toward the side with more space
            if avg_left > avg_right:
                steer = -2.5   # Steer left
            elif avg_right > avg_left:
                steer = 2.5    # Steer right
            else:
                # Equal space: prefer left (arbitrary tie-break)
                steer = -1.5

        # ── 3. Lane-centering nudge ──────────────────────────────
        # Even without obstacles, gently correct if drifting to one side
        elif avg_left < 0.4:
            steer = 1.0    # Too close to left wall — nudge right
        elif avg_right < 0.4:
            steer = -1.0   # Too close to right wall — nudge left

        return steer, True, False