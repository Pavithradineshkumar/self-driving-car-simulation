import sys
import os
import numpy as np
import pygame

# Import Phase 2 simulator components
sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'phase2_sensors_ai')
))

from car      import Car
from road     import Road
from sensors  import SensorArray
from obstacle import Obstacle
import constants as sim_c

from phase6_rl.constants import (
    STATE_SIZE, ACTION_SIZE,
    REWARD_ALIVE, REWARD_SPEED_BONUS, REWARD_CENTERED,
    REWARD_CRASH, REWARD_BOUNDARY, REWARD_SLOW
)


class DrivingEnvironment:
    """
    Gym-style wrapper around the Phase 2 Pygame simulator.

    Interface mirrors OpenAI Gym:
        state          = env.reset()
        state, reward, done, info = env.step(action)

    State vector (9 floats, all normalized to roughly [-1, 1]):
        [0–6] sensor ray readings (0.0=blocked, 1.0=clear)
        [7]   current speed / MAX_SPEED
        [8]   lane center offset / (ROAD_WIDTH/2)

    Actions (integers 0–3):
        0 = straight + accelerate
        1 = left     + accelerate
        2 = right    + accelerate
        3 = brake

    render=True shows the Pygame window during training.
    Set render=False for headless/faster training.
    """

    def __init__(self, render=True):
        self.do_render = render
        self.road      = None
        self.car       = None
        self.sensors   = None
        self.obstacles = []
        self.spawn_timer = 0
        self.step_count  = 0

        if self.do_render:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (sim_c.SCREEN_WIDTH, sim_c.SCREEN_HEIGHT)
            )
            pygame.display.set_caption("Phase 6 — RL Training")
            self.clock = pygame.time.Clock()
            self.font  = pygame.font.SysFont("monospace", 13)

    def reset(self):
        """Start a new episode. Returns initial state vector."""
        self.road       = Road()
        self.car        = Car(sim_c.CAR_START_X, sim_c.CAR_START_Y)
        self.sensors    = SensorArray()
        self.obstacles  = []
        self.spawn_timer = 0
        self.step_count  = 0
        return self._get_state()

    def step(self, action):
        """
        Apply action, advance simulation one frame.
        Returns (next_state, reward, done, info).
        """
        self.step_count += 1

        # ── Handle Pygame window close ───────────────────────────
        if self.do_render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # ── Apply action ─────────────────────────────────────────
        steer, accel, brake = self._action_to_controls(action)
        self.car.apply_ai(steer, accel, brake)

        # ── Spawn and update obstacles ───────────────────────────
        self.spawn_timer += 1
        if (self.spawn_timer >= sim_c.SPAWN_INTERVAL and
                len(self.obstacles) < sim_c.MAX_OBSTACLES):
            self.spawn_timer = 0
            self.obstacles.append(
                Obstacle(self.road.get_lane_centers())
            )
        for obs in self.obstacles:
            obs.update()
        self.obstacles = [o for o in self.obstacles if o.active]

        # ── Update sensors ───────────────────────────────────────
        self.sensors.update(
            self.car.x, self.car.y,
            self.car.angle,
            self.obstacles, self.road
        )

        # ── Update car ───────────────────────────────────────────
        self.car.update(self.road)
        self.road.update(self.car.speed)

        # ── AABB collision check ─────────────────────────────────
        car_rect = pygame.Rect(
            self.car.x - self.car.width  // 2,
            self.car.y - self.car.height // 2,
            self.car.width, self.car.height
        )
        crashed = any(
            car_rect.colliderect(o.get_rect()) for o in self.obstacles
        )
        if crashed:
            self.car.is_crashed = True

        # ── Reward ───────────────────────────────────────────────
        reward, done = self._compute_reward(crashed)

        # ── Render ───────────────────────────────────────────────
        if self.do_render:
            self._render(reward)

        return self._get_state(), reward, done, {"step": self.step_count}

    # ── Private helpers ──────────────────────────────────────────

    def _action_to_controls(self, action):
        """Map integer action to (steer, accelerate, brake) tuple."""
        mapping = {
            0: (0.0,  True,  False),   # Straight
            1: (-3.0, True,  False),   # Left
            2: ( 3.0, True,  False),   # Right
            3: (0.0,  False, True),    # Brake
        }
        return mapping.get(action, (0.0, True, False))

    def _get_state(self):
        """Build normalized state vector from current simulation."""
        rays = self.sensors.readings if self.sensors.readings else [1.0] * 7

        speed_norm  = self.car.speed / sim_c.MAX_SPEED

        left_edge, right_edge = self.road.get_boundaries()
        road_half   = (right_edge - left_edge) / 2.0
        road_center = left_edge + road_half
        offset_norm = (self.car.x - road_center) / road_half
        offset_norm = max(-1.0, min(1.0, offset_norm))

        state = list(rays) + [speed_norm, offset_norm]
        return np.array(state, dtype=np.float32)

    def _compute_reward(self, crashed):
        """
        Reward shaping:
        + Small reward each frame for surviving (encourages staying alive)
        + Speed bonus (encourages movement)
        + Centering bonus (encourages lane keeping)
        − Large penalty for crash (discourages collisions)
        − Boundary penalty (discourages hugging walls)
        − Slow penalty (discourages stopping)
        """
        done = False

        if crashed:
            return REWARD_CRASH, True

        reward = REWARD_ALIVE

        # Speed bonus
        reward += REWARD_SPEED_BONUS * self.car.speed

        # Centering bonus: smaller offset = higher reward
        left_edge, right_edge = self.road.get_boundaries()
        road_center = (left_edge + right_edge) / 2.0
        offset      = abs(self.car.x - road_center)
        road_half   = (right_edge - left_edge) / 2.0
        centered    = max(0.0, 1.0 - offset / road_half)
        reward     += REWARD_CENTERED * centered

        # Boundary penalty
        margin = 30
        if (self.car.x < left_edge  + margin or
                self.car.x > right_edge - margin):
            reward += REWARD_BOUNDARY

        # Slow penalty
        if self.car.speed < 0.5:
            reward += REWARD_SLOW

        return reward, done

    def _render(self, reward):
        self.screen.fill((0, 0, 0))
        self.road.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        self.sensors.draw(self.screen)
        self.car.draw(self.screen)

        info = self.font.render(
            f"ε={_agent_epsilon:.3f}  step={self.step_count}  "
            f"reward={reward:.2f}  speed={self.car.speed:.1f}",
            True, (180, 220, 140)
        )
        self.screen.blit(info, (10, 10))
        pygame.display.flip()
        self.clock.tick(sim_c.FPS)


# Module-level reference so renderer can show current epsilon
_agent_epsilon = 1.0