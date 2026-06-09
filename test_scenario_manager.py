from phase9_intelligence.scenario_manager import ScenarioManager

manager = ScenarioManager()

for scenario in manager.get_scenarios():
    print(scenario)