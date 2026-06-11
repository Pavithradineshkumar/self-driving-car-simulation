from phase4_object_detection import perception
from phase5_autonomous.pid_controller  import PIDController
from phase5_autonomous.path_planner    import AStarPlanner
from phase5_autonomous.behavior_planner import BehaviorPlanner
from phase5_autonomous.grid_map        import OccupancyGrid
from phase5_autonomous.constants       import (
    LANE_KP, LANE_KI, LANE_KD,
    SPEED_KP, SPEED_KI, SPEED_KD,
    MAX_STEER_CORRECTION, SPEED_CRUISE,
    GRID_COLS, GRID_ROWS
)
from phase9_intelligence.emergency_system import EmergencySystem
from phase9_intelligence.traffic_light_detector import TrafficLightDetector
from phase9_intelligence.speed_sign_detector import SpeedSignDetector
from phase10_adas.adaptive_cruise import AdaptiveCruiseControl
from phase10_adas.lane_departure import LaneDepartureWarning
from phase10_adas.collision_predictor import CollisionPredictor
from phase10_adas.safety_score import SafetyScore
from phase11_analytics.analytics_engine import AnalyticsEngine
from phase11_analytics.alert_manager import AlertManager

class AutonomousDriver:
    """
    Top-level autonomous controller.

    Each frame:
    1. BehaviorPlanner reads perception → decides state + target speed
    2. A* plans a path around obstacles if needed
    3. Lane PID corrects steering from center_offset
    4. Speed PID adjusts throttle to reach target speed
    5. Returns (steer, throttle, brake) for the car actuators

    This is the class Phase 6 (RL) will replace or augment.
    """

    def __init__(self, frame_width, frame_height):
        self.fw = frame_width
        self.fh = frame_height

        self.lane_pid  = PIDController(LANE_KP,  LANE_KI,  LANE_KD)
        self.speed_pid = PIDController(SPEED_KP, SPEED_KI, SPEED_KD)

        self.behavior  = BehaviorPlanner()
        self.planner   = AStarPlanner()
        self.grid      = OccupancyGrid(frame_width, frame_height)

        self.emergency_system = EmergencySystem()

        self.current_speed = 0.0
        self.current_path  = []

        self.traffic_detector = TrafficLightDetector()
        self.speed_detector = SpeedSignDetector()

        self.current_light = "GREEN"
        self.current_speed_limit = 60

        self.acc = AdaptiveCruiseControl()
        self.ldw = LaneDepartureWarning()
        self.cp  = CollisionPredictor()

        self.safety_score = SafetyScore()
        self.analytics = AnalyticsEngine()
        self.alert_manager = AlertManager()

    def decide(self, perception):
        """
        perception : dict from PerceptionPipeline.process()

        Returns:
            steer    : float  (degrees, -ve = left, +ve = right)
            throttle : float  (px/frame to add to speed)
            brake    : bool
            debug    : dict   (for HUD and dashboard)
        """
        # ── 1. Behavior decision ─────────────────────────────────
        state, target_speed, should_avoid = self.behavior.update(perception)

        # Phase 9.3 Simulation

        self.current_light = self.traffic_detector.detect("GREEN")
        self.current_speed_limit = self.speed_detector.detect(40)

        nearest_distance = perception.get(
          "nearest_object_distance",
           999
        )

        if nearest_distance is None:
            nearest_distance = 999

        acc_speed = self.acc.get_target_speed(nearest_distance)
        target_speed = min(target_speed, acc_speed)

        emergency_info = self.emergency_system.evaluate(
          nearest_distance
        )

        lane_offset = perception["lanes"].get("center_offset", 0)
        lane_warning = self.ldw.check(lane_offset)

        collision_state = self.cp.predict(
            nearest_distance,
            max(self.current_speed, 1)
        )

        score = self.safety_score.calculate(
            collision_state,
            lane_warning,
            emergency_info["emergency"]
        )

        alerts = self.alert_manager.check(
            lane_warning=lane_warning,
            nearest_distance=nearest_distance,
            camera_ok=True
        )

        if emergency_info["emergency"]:
           target_speed = 0.0
           state = "EMERGENCY_BRAKE"

        brake    = (target_speed == 0.0)
        throttle = 0.0

        if self.current_light == "RED":
            target_speed = 0
            state = "TRAFFIC_LIGHT_STOP"
            brake = True

        elif self.current_light == "YELLOW":
            target_speed = min(target_speed, 20)
            state = "TRAFFIC_LIGHT_SLOW"

        else:
            target_speed = min(
            target_speed,
            self.current_speed_limit
        )

        # ── 2. Speed PID ─────────────────────────────────────────
        if not brake:
            speed_error = target_speed - self.current_speed
            throttle    = self.speed_pid.update(speed_error)
            throttle    = max(0.0, min(throttle, 1.0))  # Clamp 0–1
        else:
            self.speed_pid.reset()

        # ── 3. Path planning (A*) ────────────────────────────────
        path_steer = 0.0

        if should_avoid:
            detections = perception.get("objects", [])
            self.grid.update(detections)

            # Start = bottom-center cell (car position)
            start = (GRID_ROWS - 1, GRID_COLS // 2)

            # Goal = top-center cell (road ahead, centered)
            goal  = (0, GRID_COLS // 2)

            self.current_path = self.planner.find_path(
                self.grid.grid, start, goal
            )

            # Steer toward the next waypoint in the path
            if len(self.current_path) > 2:
                next_cell   = self.current_path[2]  # Skip immediately adjacent
                next_px, _  = self.grid.cell_to_pixel(next_cell[0], next_cell[1])
                # Positive offset = waypoint is right of center → steer right
                path_steer  = (next_px - self.fw // 2) * 0.02

        # ── 4. Lane-keeping PID ──────────────────────────────────
        center_offset = perception["lanes"].get("center_offset", 0)
        lane_steer    = self.lane_pid.update(-center_offset)
        lane_steer    = max(-MAX_STEER_CORRECTION,
                        min( MAX_STEER_CORRECTION, lane_steer))

        # Blend: if avoiding, path steering dominates
        if should_avoid:
            steer = 0.6 * path_steer + 0.4 * lane_steer
        else:
            steer = lane_steer

        # ── 5. Update internal speed estimate ────────────────────
        if brake:
            self.current_speed = max(0.0, self.current_speed - 0.4)
        else:
            self.current_speed = min(target_speed,
                                     self.current_speed + throttle * 0.5)
            
        self.analytics.update(
            self.current_speed,
            steer,
            throttle,
            brake
        )

        debug = {
            "state":        state,
            "traffic_light": self.current_light,
            "speed_limit": self.current_speed_limit,
            "emergency": emergency_info["emergency"],
            "target_speed": round(target_speed, 2),
            "actual_speed": round(self.current_speed, 2),
            "steer":        round(steer, 3),
            "throttle":     round(throttle, 3),
            "brake":        brake,
            "path_cells":   len(self.current_path),
            
            "emergency": emergency_info["emergency"],
            "nearest_distance": nearest_distance,
            "acc_speed": acc_speed,
            "lane_warning": lane_warning,
            "collision_state": collision_state,
            "safety_score": score,
            "alerts": alerts,
            "telemetry": self.analytics.latest(),
        }

        return steer, throttle, brake, debug