import cv2
import time
from phase4_object_detection.constants  import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT
from phase4_object_detection.perception import PerceptionPipeline
from phase4_object_detection.utils      import draw_hud


def main():
    pipeline   = PerceptionPipeline()
    cap        = cv2.VideoCapture(VIDEO_SOURCE)
    prev_time  = time.time()
    frame_num  = 0

    if not cap.isOpened():
        print("ERROR: Cannot open video source.")
        return

    print("Running. Q = quit, S = screenshot.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame     = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame_num += 1

        # Run YOLO every 2nd frame for performance on CPU
        run_yolo  = (frame_num % 2 == 0)
        annotated, perception = pipeline.process(frame, run_detection=run_yolo)

        now       = time.time()
        fps       = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now

        draw_hud(annotated, perception, fps)
        cv2.imshow("Phase 4 — Perception Pipeline", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            cv2.imwrite("screenshot.png", annotated)
            print("Saved screenshot.png")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()