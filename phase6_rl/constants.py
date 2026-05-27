# ================================================================
# Phase 6 — DQN Reinforcement Learning hyperparameters
# ================================================================

# ── State space ──────────────────────────────────────────────────
# Input features fed to the neural network each step:
#   7 sensor ray readings (normalized 0–1)
#   1 current speed (normalized by MAX_SPEED)
#   1 lane center offset (normalized by road half-width)
# Total: 9 inputs
STATE_SIZE      = 9

# ── Action space ─────────────────────────────────────────────────
# Discrete actions the agent can choose each frame:
#   0 = go straight + accelerate
#   1 = steer left  + accelerate
#   2 = steer right + accelerate
#   3 = brake
ACTION_SIZE     = 4

# ── Neural network ───────────────────────────────────────────────
HIDDEN_SIZE     = 128    # Neurons per hidden layer
NUM_LAYERS      = 3      # Total layers including input/output

# ── Training ─────────────────────────────────────────────────────
LEARNING_RATE   = 1e-3
GAMMA           = 0.95   # Discount factor (future reward weight)
BATCH_SIZE      = 64     # Samples per training step
REPLAY_CAPACITY = 50_000 # Max experiences in replay buffer
MIN_REPLAY_SIZE = 1_000  # Don't train until buffer has this many

# ── Exploration (epsilon-greedy) ─────────────────────────────────
# Agent starts by exploring randomly, gradually shifts to learned policy
EPSILON_START   = 1.0    # 100% random at start
EPSILON_END     = 0.05   # 5% random at end (always some exploration)
EPSILON_DECAY   = 0.995  # Multiply epsilon by this each episode

# ── Target network ───────────────────────────────────────────────
TARGET_UPDATE_FREQ = 500  # Frames between target network syncs

# ── Training schedule ────────────────────────────────────────────
MAX_EPISODES    = 1_000
MAX_STEPS_EP    = 1_000   # Max frames per episode before forced reset
SAVE_EVERY      = 50      # Save model every N episodes

# ── Reward shaping ───────────────────────────────────────────────
REWARD_ALIVE         =  0.1   # Small reward each frame for surviving
REWARD_SPEED_BONUS   =  0.05  # Per unit of speed (encourages movement)
REWARD_CENTERED      =  0.2   # Reward for staying near lane center
REWARD_CRASH         = -10.0  # Large penalty for hitting anything
REWARD_BOUNDARY      = -2.0   # Penalty for touching road edge
REWARD_SLOW          = -0.05  # Penalty per frame when nearly stopped

# ── Model paths ──────────────────────────────────────────────────
MODEL_DIR       = "phase6_rl/saved_models"
MODEL_FILE      = "dqn_driving.pth"