from phase5_autonomous.constants import (
    SPEED_CRUISE, SPEED_CAUTIOUS, SPEED_SLOW, SPEED_STOP,
    DIST_CAUTION, DIST_SLOW, DIST_STOP,
    STATE_CRUISE, STATE_CAUTION, STATE_SLOW,
    STATE_STOP, STATE_AVOID, STATE_TRAFFIC
)


class BehaviorPlanner:
    """
    High-level decision maker. Converts perception data into
    a target speed and a behavioral state.

    The PID controllers and path planner act on these decisions.

    States (in priority order):
        TRAFFIC_LIGHT_STOP — red light detected ahead
        STOP               — obstacle within DIST_STOP metres
        SLOW               — obstacle within DIST_SLOW metres
        AVOID              — obstacle in lane, needs path deviation
        CAUTION            — obstacle within DIST_CAUTION metres
        CRUISE             — clear road, full speed
    """

    def __init__(self):
        self.state        = STATE_CRUISE
        self.target_speed = SPEED_CRUISE

    def update(self, perception):
        """
        perception : dict from PerceptionPipeline.process()

        Returns (state, target_speed, should_avoid)
            state        : str  — current behavioral state
            target_speed : float — desired speed in px/frame
            should_avoid : bool — True if path planner should reroute
        """
        objects   = perception.get("objects",  [])
        warnings  = perception.get("warnings", [])

        # ── Check for red traffic light ──────────────────────────
        for obj in objects:
            if obj["class_name"] == "traffic light" and obj["in_danger"]:
                # In a real system we'd classify the light color.
                # Here we conservatively stop whenever a light is close.
                self.state        = STATE_TRAFFIC
                self.target_speed = SPEED_STOP
                return self.state, self.target_speed, False

        # ── Check stop sign ──────────────────────────────────────
        for obj in objects:
            if obj["class_name"] == "stop sign" and obj["in_danger"]:
                self.state        = STATE_STOP
                self.target_speed = SPEED_STOP
                return self.state, self.target_speed, False

        # ── Check closest obstacle distance ─────────────────────
        # Objects are pre-sorted closest-first by ObjectDetector
        closest_dist = None
        has_danger   = False

        for obj in objects:
            d = obj["distance_m"]
            if d is not None:
                if closest_dist is None or d < closest_dist:
                    closest_dist = d
            if obj["in_danger"]:
                has_danger = True

        # ── Determine state from distance ────────────────────────
        if closest_dist is not None and closest_dist <= DIST_STOP:
            self.state        = STATE_STOP
            self.target_speed = SPEED_STOP
            should_avoid      = True

        elif closest_dist is not None and closest_dist <= DIST_SLOW:
            self.state        = STATE_SLOW
            self.target_speed = SPEED_SLOW
            should_avoid      = has_danger

        elif closest_dist is not None and closest_dist <= DIST_CAUTION:
            self.state        = STATE_CAUTION
            self.target_speed = SPEED_CAUTIOUS
            should_avoid      = False

        else:
            self.state        = STATE_CRUISE
            self.target_speed = SPEED_CRUISE
            should_avoid      = False

        return self.state, self.target_speed, should_avoid