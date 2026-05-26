import cv2
import numpy as np
import math
from phase3_lane_detection.constants import*

class LaneDetector:
    """
    Detects left and right lane lines in a single frame.

    Pipeline:
        frame → grayscale → blur → Canny edges
              → ROI mask → Hough lines → average lines
              → draw overlay → return annotated frame

    The class is stateless per-frame but stores the previous
    detected lines for temporal smoothing (prevents flickering).
    """

    def __init__(self):
        # Exponential moving average of previous line coordinates
        # Prevents flickering when detection briefly fails
        self._prev_left  = None   # (x1, y1, x2, y2)
        self._prev_right = None
        self._smoothing  = 0.85   # 0=no memory, 1=never updates

    # ── Public API ─────────────────────────────────────────────────

    def process_frame(self, frame):
        """
        Full pipeline. Returns the original frame with lane overlay.
        Also returns a dict of metadata (lane positions, center offset).
        """
        h, w = frame.shape[:2]

        # Step 1: Convert to grayscale — Canny works on single-channel
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Step 2: Gaussian blur — reduces noise before edge detection
        blurred = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)

        # Step 3: Canny edge detection
        edges = cv2.Canny(blurred, CANNY_LOW, CANNY_HIGH)

        # Step 4: Apply ROI mask — keep only the road triangle
        masked = self._apply_roi(edges, h, w)

        # Step 5: Hough Transform — find line segments in edge image
        raw_lines = cv2.HoughLinesP(
            masked,
            rho            = HOUGH_RHO,
            theta          = np.pi / 180 * HOUGH_THETA,
            threshold      = HOUGH_THRESHOLD,
            minLineLength  = HOUGH_MIN_LENGTH,
            maxLineGap     = HOUGH_MAX_GAP
        )

        # Step 6: Separate, filter, and average into two full-height lines
        left_line, right_line = self._average_lines(raw_lines, h, w)

        # Step 7: Temporal smoothing against previous frame
        left_line  = self._smooth(left_line,  "_prev_left")
        right_line = self._smooth(right_line, "_prev_right")

        # Step 8: Draw overlay onto a copy of the frame
        annotated = frame.copy()
        if left_line  is not None: self._draw_line(annotated, left_line)
        if right_line is not None: self._draw_line(annotated, right_line)

        # Draw filled lane polygon between the two lines
        if left_line is not None and right_line is not None:
            self._draw_lane_fill(annotated, left_line, right_line)

        # Step 9: Draw center guidance line
        center_offset = self._draw_center(annotated, left_line, right_line, w)

        # Step 10: Draw debug overlays
        self._draw_debug(annotated, masked, edges)

        metadata = {
            "left_line":     left_line,
            "right_line":    right_line,
            "center_offset": center_offset,  # Pixels: +ve = car right of lane center
        }

        return annotated, metadata

    # ── Private helpers ────────────────────────────────────────────

    def _apply_roi(self, image, h, w):
        """
        Zero out everything outside the road triangle.
        The triangle is defined by three vertices.
        """
        # Triangle vertices — tuned for a forward-facing dashcam
        apex_y = int(h * ROI_APEX_HEIGHT)
        vertices = np.array([[
            (0,          h),              # Bottom-left
            (w // 2,     apex_y),         # Apex (horizon level)
            (w,          h),              # Bottom-right
        ]], dtype=np.int32)

        # Create a black mask the same size as the image
        mask = np.zeros_like(image)

        # Fill the triangle with white (255)
        cv2.fillPoly(mask, vertices, 255)

        # AND the mask with the edge image:
        # only pixels inside the triangle survive
        return cv2.bitwise_and(image, mask)

    def _average_lines(self, lines, h, w):
        """
        Separate Hough lines into left/right by slope sign,
        filter out noise, then average into one representative line each.

        Returns (left_coords, right_coords) where each is (x1,y1,x2,y2)
        spanning from the bottom of the frame to the ROI apex.
        """
        left_fits  = []   # Will hold (slope, intercept) pairs
        right_fits = []

        if lines is None:
            return None, None

        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Avoid division by zero for vertical lines
            if x2 == x1:
                continue

            slope     = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1

            # Filter out near-horizontal lines (road markings, not lanes)
            if abs(slope) < MIN_SLOPE or abs(slope) > MAX_SLOPE:
                continue

            # Negative slope → line goes up-left = LEFT lane
            # Positive slope → line goes up-right = RIGHT lane
            # (Remember: y increases downward in image coordinates)
            if slope < 0:
                left_fits.append((slope, intercept))
            else:
                right_fits.append((slope, intercept))

        left_line  = self._fit_to_coords(left_fits,  h) if left_fits  else None
        right_line = self._fit_to_coords(right_fits, h) if right_fits else None

        return left_line, right_line

    def _fit_to_coords(self, fits, h):
        """
        Average a list of (slope, intercept) pairs into one line,
        then compute pixel endpoints spanning from y=h (bottom)
        to y=ROI apex.

        Line equation:  x = (y - intercept) / slope
        """
        avg_slope, avg_intercept = np.mean(fits, axis=0)

        y1 = h                            # Bottom of frame
        y2 = int(h * ROI_APEX_HEIGHT)     # Top of lane detection zone

        # Solve for x at both y positions
        x1 = int((y1 - avg_intercept) / avg_slope)
        x2 = int((y2 - avg_intercept) / avg_slope)

        return (x1, y1, x2, y2)

    def _smooth(self, new_line, attr_name):
        """
        Exponential moving average between previous and current line.
        Eliminates single-frame jitter.

        new_value = α × old + (1-α) × new
        """
        prev = getattr(self, attr_name)

        if new_line is None:
            # No detection this frame: hold previous
            return prev

        if prev is None:
            # First detection: accept directly
            setattr(self, attr_name, new_line)
            return new_line

        alpha = self._smoothing
        smoothed = tuple(
            int(alpha * p + (1 - alpha) * n)
            for p, n in zip(prev, new_line)
        )
        setattr(self, attr_name, smoothed)
        return smoothed

    def _draw_line(self, frame, coords):
        """Draw a single thick lane line."""
        x1, y1, x2, y2 = coords
        cv2.line(frame, (x1, y1), (x2, y2), LANE_COLOR, LANE_THICKNESS)

    def _draw_lane_fill(self, frame, left, right):
        """
        Fill the area between left and right lane lines
        with a semi-transparent green polygon.
        """
        lx1, ly1, lx2, ly2 = left
        rx1, ry1, rx2, ry2 = right

        # Four corners of the lane polygon
        pts = np.array([[lx1, ly1], [lx2, ly2],
                        [rx2, ry2], [rx1, ry1]], dtype=np.int32)

        overlay = frame.copy()
        cv2.fillPoly(overlay, [pts], (0, 200, 80))

        # Blend with original: 20% fill opacity
        cv2.addWeighted(overlay, 0.20, frame, 0.80, 0, frame)

    def _draw_center(self, frame, left, right, w):
        """
        Draw a center guidance line between the two lanes.
        Returns the pixel offset of car from lane center (+ve = right).
        """
        if left is None or right is None:
            return 0

        h = frame.shape[0]

        # Midpoint at bottom of frame
        bottom_mid_x = (left[0] + right[0]) // 2
        # Midpoint at top of detection zone
        top_mid_x    = (left[2] + right[2]) // 2

        cv2.line(frame,
                 (bottom_mid_x, h),
                 (top_mid_x,    int(h * ROI_APEX_HEIGHT)),
                 CENTER_COLOR, CENTER_THICKNESS)

        # Offset: positive = car is right of center
        car_x = w // 2
        offset = car_x - bottom_mid_x

        return offset

    def _draw_debug(self, frame, masked_edges, raw_edges):
        """
        Embed small debug windows in the corner of the frame.
        Shows the raw Canny output and the masked ROI.
        """
        h, w = frame.shape[:2]
        thumb_w, thumb_h = w // 5, h // 5

        # Convert single-channel to 3-channel for display
        edge_bgr  = cv2.cvtColor(raw_edges,    cv2.COLOR_GRAY2BGR)
        mask_bgr  = cv2.cvtColor(masked_edges, cv2.COLOR_GRAY2BGR)

        edge_thumb = cv2.resize(edge_bgr,  (thumb_w, thumb_h))
        mask_thumb = cv2.resize(mask_bgr,  (thumb_w, thumb_h))

        # Place in top-right corner
        frame[0:thumb_h, w-thumb_w:w]             = edge_thumb
        frame[thumb_h:thumb_h*2, w-thumb_w:w]     = mask_thumb