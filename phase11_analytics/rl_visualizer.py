class RLVisualizer:

    def __init__(self):

        self.episode = 0
        self.reward = 0.0
        self.epsilon = 1.0
        self.q_values = []

    def update(
        self,
        episode,
        reward,
        epsilon,
        q_values
    ):

        self.episode = episode
        self.reward = reward
        self.epsilon = epsilon
        self.q_values = q_values

    def snapshot(self):

        return {
            "episode": self.episode,
            "reward": self.reward,
            "epsilon": self.epsilon,
            "q_values": self.q_values
        }