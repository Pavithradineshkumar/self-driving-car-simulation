from phase10_adas.safety_score import SafetyScore

ss = SafetyScore()

print(ss.calculate("SAFE", False, False))
print(ss.calculate("WARNING", False, False))
print(ss.calculate("CRITICAL", True, False))
print(ss.calculate("CRITICAL", True, True))