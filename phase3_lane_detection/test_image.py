import cv2
import sys
from lane_detector import LaneDetector
from constants     import *


def test_on_image(path):
    img      = cv2.imread(path)
    if img is None:
        print(f"Could not load image: {path}")
        sys.exit(1)

    img      = cv2.resize(img, (FRAME_WIDTH, FRAME_HEIGHT))
    detector = LaneDetector()

    result, meta = detector.process_frame(img)

    print("Detection results:")
    print(f"  Left lane:  {meta['left_line']}")
    print(f"  Right lane: {meta['right_line']}")
    print(f"  Offset:     {meta['center_offset']} px")

    cv2.imshow("Test Image — Lane Detection", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Usage: python test_image.py test_assets/road.jpg
    path = sys.argv[1] if len(sys.argv) > 1 else "test_assets/road.jpg"
    test_on_image(path)