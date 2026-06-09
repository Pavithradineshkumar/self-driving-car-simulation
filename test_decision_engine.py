from phase9_intelligence.decision_engine import DecisionEngine

engine = DecisionEngine()

print(engine.decide("RED", 60, False))
print(engine.decide("YELLOW", 60, False))
print(engine.decide("GREEN", 60, False))
print(engine.decide("GREEN", 60, True))