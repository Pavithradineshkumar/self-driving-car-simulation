# phase9_intelligence/scenario_manager.py

class ScenarioManager:

    scenarios = [
        "Traffic Light Stop",
        "Pedestrian Crossing",
        "Emergency Brake",
        "Speed Limit Zone"
    ]

    def get_scenarios(self):
        return self.scenarios