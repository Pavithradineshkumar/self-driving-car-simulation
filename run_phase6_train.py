# python run_phase6_train.py            ← with Pygame window
# python run_phase6_train.py --headless ← faster, no window
from phase6_rl.train import train
import sys

if __name__ == "__main__":
    headless = "--headless" in sys.argv
    rewards, losses = train(render=not headless)

    from phase6_rl.utils import plot_training
    plot_training(rewards, losses)