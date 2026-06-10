class CollisionPredictor:

    def predict(self, distance, speed):

        if distance is None:
            return "SAFE"

        if speed <= 0:
            return "SAFE"

        ttc = distance / speed   # Time To Collision

        if ttc < 1:
            return "CRITICAL"

        if ttc < 3:
            return "WARNING"

        return "SAFE"