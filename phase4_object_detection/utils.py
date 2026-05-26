import cv2


def draw_hud(frame, perception, fps):
    offset   = perception["lanes"].get("center_offset", 0)
    warnings = perception.get("warnings", [])
    n_obj    = len(perception.get("objects", []))

    lines = [
        f"FPS        : {fps:.1f}",
        f"Objects    : {n_obj} detected",
        f"Lane offset: {offset:+d} px",
    ]
    for w in warnings[:4]:
        lines.append(f"! {w}")

    panel_h = 20 + len(lines) * 24
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (380, panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    for i, text in enumerate(lines):
        color = (60, 60, 255) if text.startswith("!") else (80, 220, 100)
        cv2.putText(frame, text, (18, 36 + i * 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    color, 1, cv2.LINE_AA)