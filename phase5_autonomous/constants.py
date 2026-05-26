# ================================================================
# Phase 5 — Autonomous navigation constants
# ================================================================

# ── PID: Lane keeping ────────────────────────────────────────────
# Input : center_offset (pixels, +ve = car right of lane center)
# Output: steering correction (degrees)
LANE_KP =  0.04    # Proportional gain
LANE_KI =  0.001   # Integral gain (small — prevents windup)
LANE_KD =  0.02    # Derivative gain (dampens oscillation)

# Maximum steering correction the PID can command (degrees/frame)
MAX_STEER_CORRECTION = 4.0

# ── PID: Speed control ───────────────────────────────────────────
# Input : speed_error = target_speed − current_speed
# Output: throttle adjustment (px/frame²)
SPEED_KP = 0.3
SPEED_KI = 0.01
SPEED_KD = 0.05

# ── Behavior planner speeds (px/frame) ──────────────────────────
SPEED_CRUISE     = 5.0    # Normal open-road speed
SPEED_CAUTIOUS   = 3.0    # Near an obstacle or turn
SPEED_SLOW       = 1.5    # Very close to obstacle
SPEED_STOP       = 0.0    # Full stop

# Distance thresholds (metres) from ObjectDetector estimates
DIST_CAUTION     = 20.0   # Start slowing
DIST_SLOW        = 10.0   # Slow significantly
DIST_STOP        =  5.0   # Emergency stop

# ── A* grid ──────────────────────────────────────────────────────
GRID_COLS        = 20     # Horizontal grid cells
GRID_ROWS        = 30     # Vertical grid cells
# Each cell represents (FRAME_WIDTH/GRID_COLS) × (FRAME_HEIGHT/GRID_ROWS) px

# ── Integral windup clamp ────────────────────────────────────────
PID_INTEGRAL_MAX = 50.0   # Clamp accumulated integral to prevent windup

# ── Behavior states ─────────────────────────────────────────────
STATE_CRUISE     = "CRUISE"
STATE_CAUTION    = "CAUTION"
STATE_SLOW       = "SLOW"
STATE_STOP       = "STOP"
STATE_AVOID      = "AVOID"
STATE_TRAFFIC    = "TRAFFIC_LIGHT_STOP"