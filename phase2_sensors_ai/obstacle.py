import pygame
import random
from constants import *


class Obstacle:
    """
    A static or moving car/object on the road.

    Uses AABB (Axis-Aligned Bounding Box) collision:
    Two rectangles collide if they overlap on BOTH axes simultaneously.
    No rotation — simple and fast. Phase 4 upgrades this with YOLO detection.

    Spawns at the top of the screen and moves downward (toward player).
    """

    def __init__(self, lane_centers):
        """
        lane_centers: list of X coords for each lane's center
                      (from Road.get_lane_centers())
        """
        # Pick a random lane to spawn in
        lane_x = random.choice(lane_centers)

        self.x      = float(lane_x)
        self.y      = float(-OBSTACLE_HEIGHT)  # Start just above screen
        self.width  = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.speed  = OBSTACLE_SPEED + random.uniform(-1.0, 1.0)  # Vary speed
        self.active = True    # False = remove from list

    def update(self):
        """Move the obstacle down the screen."""
        self.y += self.speed

        # Deactivate once it scrolls off the bottom
        if self.y > SCREEN_HEIGHT + self.height:
            self.active = False

    def draw(self, surface):
        # Draw as a rounded rect (same proportions as player car)
        rect = pygame.Rect(
            self.x - self.width  // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, OBSTACLE_COLOR, rect, border_radius=6)

        # Taillights (two red dots at the bottom of the obstacle)
        pygame.draw.circle(surface, (255, 0, 0),
                           (int(self.x - self.width  // 4),
                            int(self.y + self.height // 2 - 8)), 4)
        pygame.draw.circle(surface, (255, 0, 0),
                           (int(self.x + self.width  // 4),
                            int(self.y + self.height // 2 - 8)), 4)

    def get_rect(self):
        """Return a pygame.Rect for AABB collision checks."""
        return pygame.Rect(
            self.x - self.width  // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    def contains_point(self, px, py):
        """
        Check if point (px, py) is inside this obstacle's bounding box.
        Used by the sensor ray-caster.
        """
        half_w = self.width  // 2
        half_h = self.height // 2
        return (self.x - half_w <= px <= self.x + half_w and
                self.y - half_h <= py <= self.y + half_h)