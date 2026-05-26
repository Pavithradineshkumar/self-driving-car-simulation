import cv2

# Package-qualified imports — Python always finds the right module
from phase3_lane_detection.lane_detector     import LaneDetector
from phase4_object_detection.object_detector import ObjectDetector
from phase4_object_detection.constants       import (
    BOX_COLORS, DEFAULT_BOX_COLOR,
    BOX_THICKNESS, LABEL_FONT_SCALE, LABEL_THICKNESS
)


class PerceptionPipeline:
    """
    Unified perception: lane detection (Phase 3) + object detection (Phase 4).

    Usage:
        pipeline = PerceptionPipeline()
        annotated_frame, perception_data = pipeline.process(frame)

    perception_data keys:
        lanes   → dict  (left_line, right_line, center_offset)
        objects → list  (detection dicts from ObjectDetector)
        warnings→ list  (plain-English alert strings)
    """

    def __init__(self):
        self.lane_detector   = LaneDetector()
        self.object_detector = ObjectDetector()

    def process(self, frame, run_detection=True):
        """
        run_detection=False skips YOLO for that frame.
        Useful for performance: run YOLO every 2nd frame,
        lanes every frame.
        """
        # ── 1. Lane detection (Phase 3 pipeline) ────────────────
        lane_frame, lane_meta = self.lane_detector.process_frame(frame)

        # ── 2. Object detection (YOLOv8) ────────────────────────
        detections = []
        if run_detection:
            detections = self.object_detector.detect(lane_frame)

        # ── 3. Draw bounding boxes on top of lane overlay ────────
        annotated = self._draw_detections(lane_frame, detections)

        # ── 4. Generate plain-English warnings ──────────────────
        warnings = self._generate_warnings(lane_meta, detections)

        return annotated, {
            "lanes":    lane_meta,
            "objects":  detections,
            "warnings": warnings,
        }

    # ── Private helpers ─────────────────────────────────────────

    def _draw_detections(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det["box"]
            name   = det["class_name"]
            conf   = det["confidence"]
            dist   = det["distance_m"]
            danger = det["in_danger"]

            color     = BOX_COLORS.get(name, DEFAULT_BOX_COLOR)
            thickness = BOX_THICKNESS + 2 if danger else BOX_THICKNESS

            # Bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

            # Label text: "car 0.87 | 8.3m"
            label = f"{name} {conf:.2f}"
            if dist is not None:
                label += f" | {dist}m"

            # Filled label background
            (tw, th), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                LABEL_FONT_SCALE,
                LABEL_THICKNESS
            )
            cv2.rectangle(frame,
                          (x1, y1 - th - 8),
                          (x1 + tw + 6, y1),
                          color, -1)
            cv2.putText(frame, label,
                        (x1 + 3, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        LABEL_FONT_SCALE,
                        (0, 0, 0),
                        LABEL_THICKNESS,
                        cv2.LINE_AA)

            # Red DANGER badge below box
            if danger:
                cv2.putText(frame, "! DANGER",
                            (x1, y2 + 18),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.55, (0, 0, 255), 2, cv2.LINE_AA)

        return frame

    def _generate_warnings(self, lane_meta, detections):
        warnings = []

        if lane_meta.get("left_line")  is None:
            warnings.append("LEFT LANE NOT DETECTED")
        if lane_meta.get("right_line") is None:
            warnings.append("RIGHT LANE NOT DETECTED")

        offset = lane_meta.get("center_offset", 0)
        if abs(offset) > 80:
            side = "RIGHT" if offset < 0 else "LEFT"
            warnings.append(f"DRIFTING {side} — {abs(offset)}px off center")

        for det in detections:
            if det["in_danger"]:
                dist_str = f"{det['distance_m']}m" if det["distance_m"] else "very close"
                warnings.append(
                    f"{det['class_name'].upper()} AHEAD — {dist_str}"
                )

        return warnings