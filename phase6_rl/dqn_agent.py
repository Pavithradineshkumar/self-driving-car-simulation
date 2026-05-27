import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os

from phase6_rl.replay_buffer import ReplayBuffer
from phase6_rl.constants import (
    STATE_SIZE, ACTION_SIZE, HIDDEN_SIZE,
    LEARNING_RATE, GAMMA, BATCH_SIZE,
    REPLAY_CAPACITY, MIN_REPLAY_SIZE,
    EPSILON_START, EPSILON_END, EPSILON_DECAY,
    TARGET_UPDATE_FREQ, MODEL_DIR, MODEL_FILE
)


class DQNNetwork(nn.Module):
    """
    Fully connected Q-network.

    Architecture:
        Input  (STATE_SIZE=9)
          → Linear(9, 128) → ReLU
          → Linear(128, 128) → ReLU
          → Linear(128, ACTION_SIZE=4)
        Output: one Q-value per action

    No softmax — raw Q-values are compared directly.
    The action with the highest Q-value is chosen greedily.
    """

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(STATE_SIZE,  HIDDEN_SIZE),
            nn.ReLU(),
            nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE),
            nn.ReLU(),
            nn.Linear(HIDDEN_SIZE, ACTION_SIZE),
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    """
    DQN agent: selects actions, stores experience, trains the network.

    Two networks:
        online_net  — trained every step, used for action selection
        target_net  — copy of online_net, updated every TARGET_UPDATE_FREQ steps
                      used to compute stable TD targets

    Training uses the Bellman equation:
        loss = MSE( Q_online(s,a),  r + γ · max_a' Q_target(s', a') )
    """

    def __init__(self):
        # Detect GPU — falls back to CPU silently
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        print(f"[DQNAgent] Using device: {self.device}")

        self.online_net = DQNNetwork().to(self.device)
        self.target_net = DQNNetwork().to(self.device)

        # Target starts identical to online
        self.target_net.load_state_dict(self.online_net.state_dict())
        self.target_net.eval()   # Target never trains directly

        self.optimizer = optim.Adam(
            self.online_net.parameters(), lr=LEARNING_RATE
        )
        self.loss_fn = nn.MSELoss()

        self.memory  = ReplayBuffer(REPLAY_CAPACITY)
        self.epsilon = EPSILON_START
        self.steps   = 0          # Total frames trained on

    # ── Action selection ──────────────────────────────────────────

    def select_action(self, state, training=True):
        """
        Epsilon-greedy action selection.

        With probability epsilon → random action (exploration)
        Otherwise → greedy action from Q-network (exploitation)

        During evaluation (training=False) always use greedy.
        """
        if training and np.random.random() < self.epsilon:
            return np.random.randint(ACTION_SIZE)

        state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.online_net(state_t)
        return int(q_values.argmax().item())

    # ── Training step ─────────────────────────────────────────────

    def train_step(self):
        """
        Sample a mini-batch from replay buffer and perform one
        gradient descent step on the Bellman loss.

        Returns the loss value (float) for logging.
        Returns None if buffer not ready yet.
        """
        if len(self.memory) < MIN_REPLAY_SIZE:
            return None

        states, actions, rewards, next_states, dones = \
            self.memory.sample(BATCH_SIZE)

        # Convert numpy arrays to tensors
        states_t      = torch.FloatTensor(states).to(self.device)
        actions_t     = torch.LongTensor(actions).to(self.device)
        rewards_t     = torch.FloatTensor(rewards).to(self.device)
        next_states_t = torch.FloatTensor(next_states).to(self.device)
        dones_t       = torch.FloatTensor(dones).to(self.device)

        # ── Current Q-values ─────────────────────────────────────
        # online_net(states_t) → shape (batch, ACTION_SIZE)
        # .gather(1, actions_t.unsqueeze(1)) → Q(s, a) for chosen action
        current_q = self.online_net(states_t).gather(
            1, actions_t.unsqueeze(1)
        ).squeeze(1)

        # ── Target Q-values (Bellman) ─────────────────────────────
        with torch.no_grad():
            # max Q-value in next state from target network
            next_q = self.target_net(next_states_t).max(1)[0]
            # If done=1 (episode ended), future reward is 0
            target_q = rewards_t + GAMMA * next_q * (1.0 - dones_t)

        # ── Gradient descent ──────────────────────────────────────
        loss = self.loss_fn(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()

        # Gradient clipping prevents exploding gradients
        torch.nn.utils.clip_grad_norm_(self.online_net.parameters(), 1.0)
        self.optimizer.step()

        # ── Update target network periodically ───────────────────
        self.steps += 1
        if self.steps % TARGET_UPDATE_FREQ == 0:
            self.target_net.load_state_dict(self.online_net.state_dict())

        return float(loss.item())

    # ── Epsilon decay ─────────────────────────────────────────────

    def decay_epsilon(self):
        """Call once per episode to reduce exploration over time."""
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

    # ── Save / Load ───────────────────────────────────────────────

    def save(self, episode=None):
        os.makedirs(MODEL_DIR, exist_ok=True)
        path = os.path.join(MODEL_DIR, MODEL_FILE)
        torch.save({
            "online_net":  self.online_net.state_dict(),
            "target_net":  self.target_net.state_dict(),
            "optimizer":   self.optimizer.state_dict(),
            "epsilon":     self.epsilon,
            "steps":       self.steps,
            "episode":     episode,
        }, path)
        print(f"[DQNAgent] Saved to {path} (episode {episode})")

    def load(self):
        path = os.path.join(MODEL_DIR, MODEL_FILE)
        if not os.path.exists(path):
            print(f"[DQNAgent] No saved model at {path}")
            return False
        ckpt = torch.load(path, map_location=self.device)
        self.online_net.load_state_dict(ckpt["online_net"])
        self.target_net.load_state_dict(ckpt["target_net"])
        self.optimizer.load_state_dict(ckpt["optimizer"])
        self.epsilon = ckpt["epsilon"]
        self.steps   = ckpt["steps"]
        print(f"[DQNAgent] Loaded from episode {ckpt.get('episode')}")
        return True