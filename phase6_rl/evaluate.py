from phase6_rl.driving_env import DrivingEnvironment
from phase6_rl.dqn_agent   import DQNAgent
from phase6_rl.constants   import MAX_STEPS_EP


def evaluate(num_episodes=5):
    """
    Run the trained agent with no exploration (epsilon=0).
    Shows the Pygame window so you can watch it drive.
    """
    env   = DrivingEnvironment(render=True)
    agent = DQNAgent()

    loaded = agent.load()
    if not loaded:
        print("No trained model found. Train first with run_phase6_train.py")
        return

    # No exploration during evaluation
    agent.epsilon = 0.0

    for ep in range(1, num_episodes + 1):
        state        = env.reset()
        total_reward = 0.0

        for step in range(MAX_STEPS_EP):
            action = agent.select_action(state, training=False)
            state, reward, done, _ = env.step(action)
            total_reward += reward
            if done:
                break

        print(f"Eval episode {ep}: total reward = {total_reward:.2f}")

    print("Evaluation complete.")


if __name__ == "__main__":
    evaluate()