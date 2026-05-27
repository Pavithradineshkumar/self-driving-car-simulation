import sys
import os
import numpy as np

from phase6_rl.driving_env  import DrivingEnvironment, _agent_epsilon
from phase6_rl.dqn_agent    import DQNAgent
from phase6_rl.constants    import (
    MAX_EPISODES, MAX_STEPS_EP,
    SAVE_EVERY, MIN_REPLAY_SIZE
)
import phase6_rl.driving_env as env_module


def train(render=True):
    """
    Main training loop.

    render=True  : shows Pygame window (slower, good for watching)
    render=False : headless mode (faster, good for long runs)
    """
    env   = DrivingEnvironment(render=render)
    agent = DQNAgent()

    # Resume from checkpoint if one exists
    agent.load()

    episode_rewards = []
    episode_losses  = []

    print(f"Training for {MAX_EPISODES} episodes. Ctrl+C to stop early.")
    print(f"Model will be saved every {SAVE_EVERY} episodes.\n")

    for episode in range(1, MAX_EPISODES + 1):

        state        = env.reset()
        total_reward = 0.0
        total_loss   = 0.0
        loss_count   = 0

        # Share epsilon with renderer
        env_module._agent_epsilon = agent.epsilon

        for step in range(MAX_STEPS_EP):

            # ── Agent selects action ──────────────────────────────
            action = agent.select_action(state, training=True)

            # ── Environment step ──────────────────────────────────
            next_state, reward, done, info = env.step(action)

            # ── Store experience ──────────────────────────────────
            agent.memory.push(state, action, reward, next_state, done)

            # ── Train one step ────────────────────────────────────
            loss = agent.train_step()
            if loss is not None:
                total_loss  += loss
                loss_count  += 1

            total_reward += reward
            state         = next_state

            if done:
                break

        # ── End of episode ─────────────────────────────────────────
        agent.decay_epsilon()
        episode_rewards.append(total_reward)

        avg_loss = total_loss / max(loss_count, 1)
        episode_losses.append(avg_loss)

        # Rolling average over last 20 episodes
        avg_reward = np.mean(episode_rewards[-20:])

        print(
            f"Ep {episode:4d}/{MAX_EPISODES}  "
            f"reward: {total_reward:7.2f}  "
            f"avg(20): {avg_reward:7.2f}  "
            f"ε: {agent.epsilon:.3f}  "
            f"loss: {avg_loss:.4f}  "
            f"buffer: {len(agent.memory)}"
        )

        if episode % SAVE_EVERY == 0:
            agent.save(episode=episode)

    # Final save
    agent.save(episode=MAX_EPISODES)
    print("\nTraining complete.")
    return episode_rewards, episode_losses


if __name__ == "__main__":
    # Pass --headless to train without Pygame window
    headless = "--headless" in sys.argv
    train(render=not headless)