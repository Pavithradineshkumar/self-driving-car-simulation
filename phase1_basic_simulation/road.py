import pygame
from constants import *

class Road:
    """
    Draws a 3-lane road that scrolls vertically to simulate movement.
    The road itself is stationary on screen; the scrolling offset
    comes from the car's speed, creating the illusion of forward motion.
    """

    def __init__(self):
        self.scroll_offset = 0      # How many pixels the road has scrolled
        self.speed         = 0      # Set externally by the car each frame

    def update(self, car_speed):
        """
        Advance the scroll offset by the car's current speed.
        We use modulo so the pattern repeats seamlessly.
        """
        self.speed = car_speed
        # DASH_LENGTH + DASH_GAP = one full dash cycle
        cycle = DASH_LENGTH + DASH_GAP
        self.scroll_offset = (self.scroll_offset + car_speed) % cycle

    def draw(self, surface):
        # ── 1. Road shoulder (dark strips left and right of road) ──
        pygame.draw.rect(surface, DARK_GRAY,
                         (0, 0, ROAD_LEFT, SCREEN_HEIGHT))
        pygame.draw.rect(surface, DARK_GRAY,
                         (ROAD_RIGHT, 0, SCREEN_WIDTH - ROAD_RIGHT, SCREEN_HEIGHT))

        # ── 2. Road surface ──────────────────────────────────────
        pygame.draw.rect(surface, GRAY,
                         (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # ── 3. Road edge lines (solid white) ─────────────────────
        pygame.draw.line(surface, WHITE_LINE,
                         (ROAD_LEFT,  0), (ROAD_LEFT,  SCREEN_HEIGHT), 3)
        pygame.draw.line(surface, WHITE_LINE,
                         (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 3)

        # ── 4. Lane dividers (dashed yellow) ─────────────────────
        # There are NUM_LANES - 1 = 2 inner dividers
        for lane_index in range(1, NUM_LANES):
            x = ROAD_LEFT + lane_index * LANE_WIDTH

            # Start above screen so dashes flow in smoothly
            y = -DASH_LENGTH + self.scroll_offset

            while y < SCREEN_HEIGHT:
                # Draw one dash segment
                dash_end = min(y + DASH_LENGTH, SCREEN_HEIGHT)
                if dash_end > 0:   # Only draw if visible
                    pygame.draw.line(surface, YELLOW,
                                     (x, max(y, 0)),
                                     (x, dash_end), 2)
                # Advance to next dash position
                y += DASH_LENGTH + DASH_GAP

    def get_lane_centers(self):
        """Return the X pixel center of each lane — used by AI in later phases."""
        centers = []
        for i in range(NUM_LANES):
            cx = ROAD_LEFT + i * LANE_WIDTH + LANE_WIDTH // 2
            centers.append(cx)
        return centers

    def get_boundaries(self):
        """Return (left_edge, right_edge) X coords of the drivable road."""
        return ROAD_LEFT, ROAD_RIGHT