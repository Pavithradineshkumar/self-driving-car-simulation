from phase9_intelligence.intelligence_controller import IntelligenceController

controller = IntelligenceController()

controller.update(
    traffic_light="RED",
    speed_limit=40,
    emergency=True
)

print(controller.get_state())