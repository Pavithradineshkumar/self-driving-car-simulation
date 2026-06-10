from phase10_adas.lane_departure import LaneDepartureWarning

ldw = LaneDepartureWarning()

print(ldw.check(20))
print(ldw.check(90))