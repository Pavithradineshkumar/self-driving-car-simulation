from phase7_dashboard.backend.data_bridge import bridge

bridge.update({
    "emergency": True,
    "decision": "EMERGENCY_BRAKE",
    "nearest_distance": 2.3
})

print(bridge.snapshot())