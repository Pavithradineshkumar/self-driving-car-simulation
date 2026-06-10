from phase10_adas.collision_predictor import CollisionPredictor

cp = CollisionPredictor()

print(cp.predict(None, 5))
print(cp.predict(30, 5))
print(cp.predict(10, 5))
print(cp.predict(2, 5))