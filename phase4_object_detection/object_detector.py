import cv2
import numpy as np
from ultralytics import YOLO

# Explicit package import — never ambiguous
from phase4_object_detection.constants import (
    YOLO_MODEL, CONF_THRESHOLD, IOU_THRESHOLD,
    TARGET_CLASSES, DANGER_ZONE_Y
)


class ObjectDetector:
    """
    YOLOv8 wrapper for driving perception.

    detect(frame) → list of detection dicts, each containing:
        class_id    : int
        class_name  : str
        confidence  : float  (0.0 – 1.0)
        box         : (x1, y1, x2, y2) in pixels
        center      : (cx, cy) in pixels
        distance_m  : float estimate, or None
        in_danger   : bool — True if object is in lower danger zone

    Distance estimation uses the pinhole camera approximation:
        distance ≈ (reference_height_px × 10m) / box_height_px
    This is a rough proxy. Real distance needs LiDAR or stereo camera.
    """

    # Approximate bounding box heights (px) at 10 metres distance
    # Calibrated for a typical 960×540 dashcam view.
    # Adjust these if your camera angle or resolution differs.
    REF_HEIGHTS = {
        "car":           120,
        "person":         80,
        "bus":           160,
        "truck":         150,
        "bicycle":        60,
        "motorcycle":     70,
        "traffic light":  40,
        "stop sign":      35,
    }

    def __init__(self):
        print(f"[ObjectDetector] Loading {YOLO_MODEL} ...")
        self.model = YOLO(YOLO_MODEL)
        print("[ObjectDetector] Ready.")

    def detect(self, frame):
        """Run inference on one BGR frame. Returns list of detection dicts."""
        h, w = frame.shape[:2]

        results = self.model(
            frame,
            conf    = CONF_THRESHOLD,
            iou     = IOU_THRESHOLD,
            verbose = False          # Suppress per-frame console spam
        )

        detections = []

        for box in results[0].boxes:
            class_id = int(box.cls[0])

            if class_id not in TARGET_CLASSES:
                continue

            class_name = TARGET_CLASSES[class_id]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            box_h     = max(y2 - y1, 1)      # Avoid divide-by-zero
            distance  = self._estimate_distance(class_name, box_h)
            in_danger = (y2 / h) >= DANGER_ZONE_Y

            detections.append({
                "class_id":   class_id,
                "class_name": class_name,
                "confidence": confidence,
                "box":        (x1, y1, x2, y2),
                "center":     (cx, cy),
                "distance_m": distance,
                "in_danger":  in_danger,
            })

        # Sort: danger objects first, then closest first
        detections.sort(key=lambda d: (
            not d["in_danger"],
            d["distance_m"] if d["distance_m"] is not None else 999
        ))

        return detections

    def _estimate_distance(self, class_name, box_height_px):
        ref_h = self.REF_HEIGHTS.get(class_name)
        if ref_h is None or box_height_px == 0:
            return None
        return round(10.0 * (ref_h / box_height_px), 1)