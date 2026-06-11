from phase11_analytics.event_logger import EventLogger

logger = EventLogger()

logger.log({
    "event": "lane_detected"
})

logger.log({
    "event": "obstacle_detected"
})

logger.log({
    "event": "emergency_brake"
})

print("Events logged.")