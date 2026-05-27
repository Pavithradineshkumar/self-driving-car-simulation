import matplotlib
matplotlib.use('Agg')   # Non-interactive backend — works without display
import matplotlib.pyplot as plt
import os


def plot_training(rewards, losses, save_dir="phase6_rl/saved_models"):
    """Save training curves to PNG files."""
    os.makedirs(save_dir, exist_ok=True)

    # ── Reward curve ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rewards, alpha=0.4, color='steelblue', label='Episode reward')

    # Rolling average
    window = 20
    if len(rewards) >= window:
        avg = [
            sum(rewards[max(0, i-window):i]) / min(i, window)
            for i in range(1, len(rewards)+1)
        ]
        ax.plot(avg, color='navy', linewidth=2, label=f'{window}-ep average')

    ax.set_xlabel("Episode")
    ax.set_ylabel("Total reward")
    ax.set_title("DQN Training — Episode Rewards")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(save_dir, "rewards.png"), dpi=120)
    plt.close(fig)

    # ── Loss curve ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(losses, alpha=0.5, color='coral', label='Avg loss per episode')
    ax.set_xlabel("Episode")
    ax.set_ylabel("MSE Loss")
    ax.set_title("DQN Training — Bellman Loss")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(save_dir, "loss.png"), dpi=120)
    plt.close(fig)

    print(f"Plots saved to {save_dir}/")