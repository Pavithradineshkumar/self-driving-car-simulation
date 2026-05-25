import pygame
import math
from constants import *


class SensorArray:
    """
    Casts NUM_RAYS straight lines from the car's center.
    Each ray travels up to RAY_LENGTH pixels and stops
    at the first obstacle or road boundary it hits.

    Ray angles are spread evenly across RAY_SPREAD degrees,
    centered on the car's current heading (angle).

    Output: self.readings — list of floats in [0.0, 1.0]
        1.0 = nothing detected (ray reaches full length)
        0.0 = obstacle touching the car
    """

    def __init__(self):
        self.readings    = [1.0] * NUM_RAYS   # Normalized distances
        self.ray_ends    = []                  # Pixel endpoints (for drawing)
        self.ray_origins = []                  # Pixel start points (for drawing)

    def update(self, car_x, car_y, car_angle, obstacles, road):
        """
        Recompute all rays. Called every frame.

        car_x, car_y  : car center in pixels
        car_angle     : car heading in degrees (0 = up)
        obstacles     : list of Obstacle objects
        road          : Road object (provides boundary X coords)
        """
        left_edge, right_edge = road.get_boundaries()

        self.readings    = []
        self.ray_ends    = []
        self.ray_origins = []

        # Angular step between adjacent rays
        if NUM_RAYS > 1:
            step = RAY_SPREAD / (NUM_RAYS - 1)
        else:
            step = 0

        # Starting angle: leftmost ray
        start_angle = car_angle - RAY_SPREAD / 2

        for i in range(NUM_RAYS):
            ray_angle_deg = start_angle + i * step
            ray_angle_rad = math.radians(ray_angle_deg)

            # Unit direction vector for this ray
            dx = math.sin(ray_angle_rad)
            dy = -math.cos(ray_angle_rad)   # Y is flipped in pygame

            # Walk along the ray, step by step
            hit_distance = RAY_LENGTH       # Assume no hit initially
            end_x = car_x + dx * RAY_LENGTH
            end_y = car_y + dy * RAY_LENGTH

            # Step size: 4px is a good balance between accuracy and speed
            for dist in range(0, RAY_LENGTH, 4):
                check_x = car_x + dx * dist
                check_y = car_y + dy * dist

                # ── Check 1: Road boundary ───────────────────────
                if check_x < left_edge or check_x > right_edge:
                    hit_distance = dist
                    end_x, end_y = check_x, check_y
                    break

                # ── Check 2: Each obstacle ───────────────────────
                hit_obstacle = False
                for obs in obstacles:
                    if obs.contains_point(check_x, check_y):
                        hit_distance = dist
                        end_x, end_y = check_x, check_y
                        hit_obstacle = True
                        break
                if hit_obstacle:
                    break

            # Normalize: 1.0 = full length, 0.0 = right at car
            normalized = hit_distance / RAY_LENGTH

            self.readings.append(normalized)
            self.ray_ends.append((end_x, end_y))
            self.ray_origins.append((car_x, car_y))

    def draw(self, surface):
        """Visualise all rays. Green = clear, red = hit detected."""
        if not SHOW_SENSORS:
            return

        for i in range(NUM_RAYS):
            # Color based on normalized reading
            t = self.readings[i]       # 1.0 = clear, 0.0 = close hit
            if t > 0.9:
                color = RAY_COLOR      # Green: nothing close
            elif t > 0.5:
                # Interpolate green → yellow
                g = int(200 * t)
                color = (255 - g, 200, 0)
            else:
                color = RAY_HIT_COLOR  # Red: obstacle very close

            pygame.draw.line(surface, color,
                             self.ray_origins[i],
                             self.ray_ends[i], 1)

            # Small circle at the ray's hit point
            pygame.draw.circle(surface, color,
                                (int(self.ray_ends[i][0]),
                                 int(self.ray_ends[i][1])), 3)