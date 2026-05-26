import cv2
import time
import sys
import os

from phase4_object_detection.perception  import PerceptionPipeline
from phase4_object_detection.constants   import (
    VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT
)
from phase5_autonomous.autonomous_driver import AutonomousDriver
from phase5_autonomous.utils             import (
    draw_autonomous_hud, draw_path, draw_grid_overlay
)


def main():
    pipeline = PerceptionPipeline()
    driver   = AutonomousDriver(FRAME_WIDTH, FRAME_HEIGHT)
    cap      = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        print("ERROR: Cannot open video source.")
        return

    prev_time  = time.time()
    frame_num  = 0
    show_grid  = False    # Press G to toggle grid overlay

    print("Phase 5 running. Q=quit, S=screenshot, G=grid overlay")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame     = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame_num += 1

        # ── Perception (YOLO every 2nd frame for CPU performance) ─
        run_yolo  = (frame_num % 2 == 0)
        annotated, perception = pipeline.process(frame, run_detection=run_yolo)

        # ── Autonomous decision ──────────────────────────────────
        steer, throttle, brake, debug = driver.decide(perception)

        # ── Visualize path + grid ────────────────────────────────
        if show_grid:
            draw_grid_overlay(annotated, driver.grid)
        if driver.current_path:
            draw_path(annotated, driver.current_path, driver.grid)

        # ── HUD ──────────────────────────────────────────────────
        now       = time.time()
        fps       = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now

        draw_autonomous_hud(annotated, debug, perception, fps)

        # ── Steering indicator (bottom center) ───────────────────
        cx    = FRAME_WIDTH  // 2
        cy    = FRAME_HEIGHT - 30
        steer_px = int(steer * 30)          # Scale for display
        cv2.arrowedLine(annotated,
                        (cx, cy),
                        (cx + steer_px, cy),
                        (0, 255, 200), 3, tipLength=0.4)
        cv2.putText(annotated,
                    f"steer: {steer:+.2f}  throttle: {throttle:.2f}  brake: {brake}",
                    (cx - 180, cy + 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (200, 200, 200), 1, cv2.LINE_AA)

        cv2.imshow("Phase 5 — Autonomous Navigation", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            cv2.imwrite(f"phase5_frame_{frame_num}.png", annotated)
            print(f"Saved frame {frame_num}")
        if key == ord('g'):
            show_grid = not show_grid

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()