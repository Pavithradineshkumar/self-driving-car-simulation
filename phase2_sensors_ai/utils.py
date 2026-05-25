import pygame
from constants import *

def draw_hud(surface, telemetry, font):
    """
    Renders a heads-up display in the top-left corner.
    telemetry: dict from Car.get_telemetry()
    font: a pygame.font.Font object (created once in main.py)
    """
    hud_lines = [
        f"Speed  : {telemetry['speed']:5.2f} px/frame",
        f"Angle  : {telemetry['angle']:6.1f}°",
        f"Pos    : ({telemetry['x']:.0f}, {telemetry['y']:.0f})",
        f"Dist   : {telemetry['odometer']:.0f} px",
    ]

    # Semi-transparent background panel
    panel = pygame.Surface((220, 20 + len(hud_lines) * 22), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))   # RGBA — 140 = ~55% opacity
    surface.blit(panel, (10, 10))

    for i, line in enumerate(hud_lines):
        color = GREEN if not telemetry['crashed'] else RED
        text_surf = font.render(line, True, color)
        surface.blit(text_surf, (18, 18 + i * 22))


def draw_controls_hint(surface, font):
    """Small reminder of controls — fades into the corner."""
    hints = ["W/↑ Accelerate", "S/↓ Brake", "A/← Steer left", "D/→ Steer right"]
    for i, hint in enumerate(hints):
        surf = font.render(hint, True, (160, 160, 160))
        surface.blit(surf, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 100 + i * 22))