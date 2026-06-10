from phase10_adas.adaptive_cruise import AdaptiveCruiseControl

acc = AdaptiveCruiseControl()

for d in [None, 50, 30, 20, 10, 5]:
    print(d, "->", acc.get_target_speed(d))