from phase9_intelligence.traffic_light_detector import TrafficLightDetector

detector = TrafficLightDetector()

print(detector.detect("red"))
print(detector.detect("yellow"))
print(detector.detect("green"))
print(detector.detect("blue"))