import random
import numpy as np
from collections import deque


class ReplayBuffer:
    """
    Circular experience replay buffer.

    Stores (state, action, reward, next_state, done) tuples.
    Samples random mini-batches for training — this breaks the
    temporal correlation between consecutive frames that would
    otherwise make gradient updates noisy and unstable.

    Uses a deque with maxlen so old experiences are automatically
    discarded when the buffer is full.
    """

    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Store one experience tuple."""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """
        Sample a random mini-batch.
        Returns five numpy arrays: states, actions, rewards,
        next_states, dones — each of length batch_size.
        """
        batch = random.sample(self.buffer, batch_size)

        # Unzip list of tuples into separate arrays
        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            np.array(states,      dtype=np.float32),
            np.array(actions,     dtype=np.int64),
            np.array(rewards,     dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones,       dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)