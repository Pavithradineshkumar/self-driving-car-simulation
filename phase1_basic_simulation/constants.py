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