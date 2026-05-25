import cv2
import time
from constants    import *
from lane_detector import LaneDetector
from utils         import draw_telemetry


def main():
    detector = LaneDetector()

    # Open webcam (0) or a video file (change VIDEO_SOURCE in constants.py)
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        print("ERROR: Could not open video source.")
        print("  → Set VIDEO_SOURCE = 0 for webcam")
        print("  → Or provide a video file path string")
        return

    prev_time = time.time()

    print("Lane Detection running. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or camera disconnected.")
            break

        # Resize for consistent processing
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        # Run the full detection pipeline
        annotated, metadata = detector.process_frame(frame)

        # Calculate FPS
        now  = time.time()
        fps  = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now

        # Overlay telemetry text
        draw_telemetry(annotated, metadata, fps)

        cv2.imshow("Lane Detection — Phase 3", annotated)

        # Q to quit, S to save a screenshot
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            cv2.imwrite("lane_screenshot.png", annotated)
            print("Screenshot saved.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()