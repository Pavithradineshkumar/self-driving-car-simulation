# ── Screen ──────────────────────────────────────────────
SCREEN_WIDTH  = 900        # Window width in pixels
SCREEN_HEIGHT = 600        # Window height in pixels
FPS           = 60         # Frames per second (game loop speed)
TITLE         = "Self-Driving Car Simulation – Phase 1"

# ── Colors (RGB tuples) ─────────────────────────────────
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
GRAY        = (50,  50,  50)    # Road surface
DARK_GRAY   = (30,  30,  30)    # Road shoulder
YELLOW      = (255, 200,  0)    # Center lane divider
WHITE_LINE  = (220, 220, 220)   # Side lane markings
RED         = (220,  50,  50)   # Car body
BLUE        = (50,  120, 220)   # Car windshield
GREEN       = (50,  200, 100)   # HUD OK color

# ── Road ────────────────────────────────────────────────
ROAD_LEFT   = 150          # X pixel where road starts
ROAD_RIGHT  = 750          # X pixel where road ends
ROAD_WIDTH  = ROAD_RIGHT - ROAD_LEFT   # = 600px
NUM_LANES   = 3
LANE_WIDTH  = ROAD_WIDTH // NUM_LANES  # = 200px per lane

# Dashed center line parameters
DASH_LENGTH = 40           # Length of each dash in pixels
DASH_GAP    = 30           # Gap between dashes

# ── Car ─────────────────────────────────────────────────
CAR_WIDTH   = 40           # Pixels wide
CAR_HEIGHT  = 70           # Pixels tall
CAR_START_X = SCREEN_WIDTH  // 2   # Center of screen horizontally
CAR_START_Y = SCREEN_HEIGHT // 2   # Center of screen vertically

# Movement
MAX_SPEED       = 8        # Maximum forward/backward speed (px/frame)
ACCELERATION    = 0.3      # Speed gained per frame when key held
DECELERATION    = 0.15     # Speed lost per frame (natural friction)
BRAKE_FORCE     = 0.5      # Extra deceleration when braking
STEERING_SPEED  = 3.5      # Degrees turned per frame at max speed

# ── (all Phase 1 constants remain — add these below) ────────────

# ── Sensors ─────────────────────────────────────────────────────
NUM_RAYS        = 7          # Number of sensor rays cast from car
RAY_LENGTH      = 200        # Max detection distance in pixels
# Spread of rays in degrees (symmetric around car's heading)
# e.g. [-90, -60, -30, 0, 30, 60, 90] for NUM_RAYS=7
RAY_SPREAD      = 180        # Total angular spread across all rays
RAY_COLOR       = (0, 255, 100)   # Green when clear
RAY_HIT_COLOR   = (255, 60,  60)  # Red when hitting something
SHOW_SENSORS    = True       # Toggle sensor visualisation on/off

# ── Obstacles ───────────────────────────────────────────────────
OBSTACLE_WIDTH  = 44
OBSTACLE_HEIGHT = 70
OBSTACLE_COLOR  = (255, 165,  0)   # Orange
OBSTACLE_SPEED  = 3                # Pixels/frame (moves toward player)
MAX_OBSTACLES   = 5                # Max on screen at once
SPAWN_INTERVAL  = 90               # Frames between spawns (~1.5s at 60fps)

# ── AI driver ───────────────────────────────────────────────────
AI_TARGET_SPEED     = 5.0    # px/frame the AI tries to maintain
AI_BRAKE_THRESHOLD  = 80     # px — if obstacle closer than this, brake
AI_STEER_THRESHOLD  = 150    # px — if obstacle closer than this, steer