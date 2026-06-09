# phase9_intelligence/emergency_system.py

class EmergencySystem:

    SAFE_DISTANCE = 40

    def evaluate(self, object_distance):

        if object_distance < self.SAFE_DISTANCE:
            return {
                "emergency": True,
                "brake": True
            }

        return {
            "emergency": False,
            "brake": False
        }