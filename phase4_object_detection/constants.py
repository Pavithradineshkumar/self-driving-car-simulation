# ================================================================
# Phase 4 constants — object detection only
# Phase 3 constants (BLUR_KERNEL, CANNY etc.) stay in
# phase3_lane_detection/constants.py and are never imported here
# ================================================================

# ── Video source ────────────────────────────────────────────────
VIDEO_SOURCE  = 0               # 0 = webcam, or a file path string
FRAME_WIDTH   = 960
FRAME_HEIGHT  = 540

# ── YOLOv8 ──────────────────────────────────────────────────────
# yolov8n.pt = nano (fastest, ~6MB, auto-downloaded on first run)
# yolov8s.pt = small (more accurate, ~22MB)
YOLO_MODEL       = "yolov8n.pt"
CONF_THRESHOLD   = 0.40        # Minimum confidence to show a box
IOU_THRESHOLD    = 0.45        # NMS overlap threshold

# ── COCO class IDs we care about ────────────────────────────────
# These IDs are from the COCO 2017 dataset spec.
# Verify against your model at: https://docs.ultralytics.com
TARGET_CLASSES = {
    0:  "person",
    1:  "bicycle",
    2:  "car",
    3:  "motorcycle",
    5:  "bus",
    7:  "truck",
    9:  "traffic light",
    11: "stop sign",
}

# ── Danger zone ──────────────────────────────────────────────────
# Object bottom edge below this fraction = "close / danger"
DANGER_ZONE_Y    = 0.75

# ── Box drawing ──────────────────────────────────────────────────
# Colors in BGR (OpenCV format)
BOX_COLORS = {
    "person":        (0,   165, 255),  # orange
    "bicycle":       (255, 100,   0),  # blue
    "car":           (0,   220,  80),  # green
    "motorcycle":    (255, 100,   0),  # blue
    "bus":           (0,   220, 255),  # yellow
    "truck":         (0,   200, 240),  # yellow
    "traffic light": (0,   255, 255),  # bright yellow
    "stop sign":     (0,     0, 220),  # red
}
DEFAULT_BOX_COLOR = (200, 200, 200)
BOX_THICKNESS     = 2
LABEL_FONT_SCALE  = 0.55
LABEL_THICKNESS   = 1