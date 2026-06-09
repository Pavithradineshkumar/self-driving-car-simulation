from phase9_intelligence.traffic_light_detector import TrafficLightDetector
from phase9_intelligence.speed_sign_detector import SpeedSignDetector
from phase9_intelligence.emergency_system import EmergencySystem
from phase9_intelligence.decision_engine import DecisionEngine

light = TrafficLightDetector()
speed = SpeedSignDetector()
emergency = EmergencySystem()
decision = DecisionEngine()

traffic = light.detect("RED")
limit = speed.detect(60)
danger = emergency.evaluate(100)

result = decision.decide(
    traffic,
    limit,
    danger["emergency"]
)

print("Traffic:", traffic)
print("Speed Limit:", limit)
print("Emergency:", danger)
print("Decision:", result)