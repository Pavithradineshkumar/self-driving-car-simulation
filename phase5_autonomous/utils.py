import cv2
import numpy as np


def draw_autonomous_hud(frame, debug, perception, fps):
    """Full HUD showing behavior state, PID outputs, and warnings."""
    state    = debug.get("state", "?")
    t_speed  = debug.get("target_speed", 0)
    a_speed  = debug.get("actual_speed", 0)
    steer    = debug.get("steer", 0)
    warnings = perception.get("warnings", [])

    # State color coding
    state_colors = {
        "CRUISE":             (80,  220, 100),
        "CAUTION":            (0,   200, 255),
        "SLOW":               (0,   165, 255),
        "STOP":               (0,    60, 255),
        "AVOID":              (255, 160,   0),
        "TRAFFIC_LIGHT_STOP": (0,    60, 255),
    }
    s_color = state_colors.get(state, (200, 200, 200))

    lines = [
        f"FPS          : {fps:.1f}",
        f"State        : {state}",
        f"Target speed : {t_speed:.2f}",
        f"Actual speed : {a_speed:.2f}",
        f"Steer        : {steer:+.3f}",
        f"Offset       : {perception['lanes'].get('center_offset', 0):+d} px",
    ]
    for w in warnings[:3]:
        lines.append(f"! {w}")

    panel_h = 20 + len(lines) * 24
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (380, panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    for i, text in enumerate(lines):
        color = (60, 60, 255) if text.startswith("!") else (
            s_color if "State" in text else (180, 180, 180)
        )
        cv2.putText(frame, text, (18, 36 + i * 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    color, 1, cv2.LINE_AA)


def draw_path(frame, path, grid):
    """Draw the A* planned path as dots on the frame."""
    for row, col in path:
        px, py = grid.cell_to_pixel(row, col)
        cv2.circle(frame, (px, py), 4, (255, 200, 0), -1)


def draw_grid_overlay(frame, grid_obj, alpha=0.25):
    """Lightly overlay the occupancy grid for debugging."""
    h, w  = frame.shape[:2]
    rows, cols = grid_obj.grid.shape
    cw    = w // cols
    ch    = h // rows

    overlay = frame.copy()
    for r in range(rows):
        for c in range(cols):
            if grid_obj.grid[r, c] == 1:
                x1 = c * cw
                y1 = r * ch
                cv2.rectangle(overlay,
                              (x1, y1), (x1 + cw, y1 + ch),
                              (0, 0, 200), -1)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)