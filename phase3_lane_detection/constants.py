# ── Image / video ───────────────────────────────────────────────
# Set to 0 for webcam, or a file path string for video
VIDEO_SOURCE = "test_assets/drive.mp4"

# Resize every frame to this resolution before processing
# Smaller = faster; larger = more accurate
FRAME_WIDTH  = 960
FRAME_HEIGHT = 540

# ── Gaussian blur ───────────────────────────────────────────────
# Kernel size must be odd. Larger = more smoothing = less noise
# but also blurs fine lane edges at a distance
BLUR_KERNEL = (5, 5)

# ── Canny edge detection ────────────────────────────────────────
CANNY_LOW  = 50     # Weak edges below this are discarded
CANNY_HIGH = 150    # Edges above this are definitely kept
# Edges between LOW and HIGH are kept only if connected to a strong edge

# ── Region of interest ──────────────────────────────────────────
# Fraction of frame height where the ROI apex sits
# 0.55 = apex 55% down from the top (good for most dashcam angles)
ROI_APEX_HEIGHT = 0.55

# ── Hough Transform ─────────────────────────────────────────────
HOUGH_RHO         = 1          # Distance resolution (pixels)
HOUGH_THETA       = 1          # Angle resolution (degrees — converted in code)
HOUGH_THRESHOLD   = 40         # Minimum votes to register a line
HOUGH_MIN_LENGTH  = 80         # Minimum line segment length (pixels)
HOUGH_MAX_GAP     = 60         # Max gap to bridge in a broken line

# ── Lane line drawing ───────────────────────────────────────────
LANE_COLOR        = (0, 255, 100)   # BGR green
LANE_THICKNESS    = 8
CENTER_COLOR      = (0, 200, 255)   # BGR yellow-ish
CENTER_THICKNESS  = 3

# Slope filter: discard near-horizontal lines (noise)
# Lane lines typically have |slope| between 0.4 and 2.5
MIN_SLOPE = 0.4
MAX_SLOPE = 2.5