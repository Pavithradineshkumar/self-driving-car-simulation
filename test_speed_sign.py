from phase9_intelligence.speed_sign_detector import SpeedSignDetector

detector = SpeedSignDetector()

print(detector.detect(60))
print(detector.detect(80))
print(detector.detect(25))
print(detector.detect(120))