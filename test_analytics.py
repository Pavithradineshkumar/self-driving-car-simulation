from phase11_analytics.analytics_engine import AnalyticsEngine

engine = AnalyticsEngine()

engine.update(
    speed=5,
    steer=-2,
    throttle=0.4,
    brake=False
)

engine.update(
    speed=6,
    steer=-1,
    throttle=0.5,
    brake=False
)

print(engine.latest())