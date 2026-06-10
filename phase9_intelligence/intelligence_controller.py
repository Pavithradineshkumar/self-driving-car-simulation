from phase9_intelligence.emergency_system import EmergencySystem
from phase9_intelligence.decision_engine import DecisionEngine


class IntelligenceController:

    def __init__(self):
        self.emergency_system = EmergencySystem()
        self.decision_engine = DecisionEngine()

    def process(self, distance):

        emergency = self.emergency_system.evaluate(distance)

        decision = self.decision_engine.decide(distance)

        return {
            "emergency": emergency["emergency"],
            "brake": emergency["brake"],
            "decision": decision,
            "nearest_distance": distance
        }

    def update(self, distance):
        return self.process(distance)