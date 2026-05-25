import cv2


def draw_telemetry(frame, metadata, fps):
    """Render lane detection stats onto the frame."""
    offset  = metadata.get("center_offset", 0)
    left_ok = metadata.get("left_line")  is not None
    right_ok= metadata.get("right_line") is not None

    direction = "CENTER"
    if offset >  30: direction = f"<-- LEFT  {abs(offset)}px"
    if offset < -30: direction = f"RIGHT --> {abs(offset)}px"

    lines = [
        f"FPS       : {fps:.1f}",
        f"Left lane : {'OK' if left_ok  else 'NOT FOUND'}",
        f"Right lane: {'OK' if right_ok else 'NOT FOUND'}",
        f"Offset    : {offset:+d} px",
        f"Guidance  : {direction}",
    ]

    # Semi-transparent panel
    panel_h = 20 + len(lines) * 24
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (310, panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    for i, text in enumerate(lines):
        color = (80, 220, 100) if "OK" in text or "CENTER" in text else (80, 180, 255)
        cv2.putText(frame, text, (18, 36 + i * 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)