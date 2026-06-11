from phase11_analytics.rl_visualizer import RLVisualizer

rl = RLVisualizer()

rl.update(
    episode=25,
    reward=145.8,
    epsilon=0.12,
    q_values=[0.4, 0.8, 0.1, 0.6]
)

print(rl.snapshot())