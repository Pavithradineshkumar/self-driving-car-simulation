import pygame
import math
from constants import *

class Car:
    """
    Represents the player/autonomous car.
    Handles physics, input, drawing, and boundary enforcement.
    
    Coordinate system:
      - x, y = center of the car on screen
      - angle = rotation in degrees (0 = pointing up, positive = clockwise)
      - speed = current speed in pixels/frame (positive = forward)
    """

    def __init__(self, x, y):
        self.x      = float(x)     # Center X position
        self.y      = float(y)     # Center Y position
        self.angle  = 0.0          # Degrees; 0 means facing up (north)
        self.speed  = 0.0          # Pixels per frame
        self.width  = CAR_WIDTH
        self.height = CAR_HEIGHT

        # Telemetry (used by HUD and later by dashboard)
        self.odometer    = 0.0     # Total distance traveled (px)
        self.is_crashed  = False

    # ── Input handling ─────────────────────────────────────────────

    def handle_input(self, keys):
        """
        Read keyboard state and apply acceleration / steering.
        Called once per frame from main.py.
        """
        accelerating = False
        braking      = False

        # W / Up arrow → accelerate forward
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
            accelerating = True

        # S / Down arrow → brake or reverse
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.speed > 0:
                self.speed = max(self.speed - BRAKE_FORCE, 0)
            else:
                self.speed = max(self.speed - ACCELERATION, -MAX_SPEED / 2)
            braking = True

        # Natural friction when no key pressed
        if not accelerating and not braking:
            if self.speed > 0:
                self.speed = max(self.speed - DECELERATION, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + DECELERATION, 0)

        # A / Left arrow → steer left (only effective when moving)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if abs(self.speed) > 0.5:
                # Steering is proportional to speed for realism
                turn_amount = STEERING_SPEED * (self.speed / MAX_SPEED)
                self.angle -= turn_amount

        # D / Right arrow → steer right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if abs(self.speed) > 0.5:
                turn_amount = STEERING_SPEED * (self.speed / MAX_SPEED)
                self.angle += turn_amount

    # ── Physics update ─────────────────────────────────────────────

    def update(self, road):
        """
        Move the car based on current speed and angle.
        Enforce road boundaries.
        """
        # Convert angle to radians for trig
        rad = math.radians(self.angle)

        # Decompose speed into X and Y components
        # Note: pygame Y axis is inverted (positive Y = down)
        # sin(angle) moves right, -cos(angle) moves up when angle=0
        dx = math.sin(rad) * self.speed
        dy = -math.cos(rad) * self.speed

        self.x += dx
        self.y += dy

        # Track total distance (for analytics)
        self.odometer += abs(self.speed)

        # ── Boundary enforcement ────────────────────────────────
        left_edge, right_edge = road.get_boundaries()
        half_w = self.width / 2

        # Clamp X so car stays on the road
        if self.x - half_w < left_edge:
            self.x = left_edge + half_w
            self.speed *= 0.5      # Friction when hitting wall
        elif self.x + half_w > right_edge:
            self.x = right_edge - half_w
            self.speed *= 0.5

        # Keep car vertically centered (road scrolls, car stays mid-screen)
        self.y = SCREEN_HEIGHT / 2

    # ── Drawing ─────────────────────────────────────────────────────

    def draw(self, surface):
        """
        Draw the car as a rotated rectangle with a windshield stripe.
        Uses pygame's transform.rotate on a temporary surface.
        """
        # Create a small surface for the car at 0° rotation
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Car body
        pygame.draw.rect(car_surface, RED,
                         (0, 0, self.width, self.height), border_radius=6)

        # Windshield (top portion of car body)
        windshield_rect = pygame.Rect(4, 8, self.width - 8, self.height // 4)
        pygame.draw.rect(car_surface, BLUE, windshield_rect, border_radius=3)

        # Headlights (two small white dots at bottom — front of car when angle=0)
        pygame.draw.circle(car_surface, WHITE,
                           (self.width // 4,     self.height - 8), 4)
        pygame.draw.circle(car_surface, WHITE,
                           (3 * self.width // 4, self.height - 8), 4)

        # Rotate the entire car surface by the current angle
        rotated = pygame.transform.rotate(car_surface, -self.angle)

        # Place it so its center aligns with self.x, self.y
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

    # ── Telemetry ───────────────────────────────────────────────────

    def get_telemetry(self):
        """Return a dict of current car state — used by HUD and later dashboard."""
        return {
            "x":         round(self.x, 1),
            "y":         round(self.y, 1),
            "speed":     round(self.speed, 2),
            "angle":     round(self.angle % 360, 1),
            "odometer":  round(self.odometer, 0),
            "crashed":   self.is_crashed,
        }