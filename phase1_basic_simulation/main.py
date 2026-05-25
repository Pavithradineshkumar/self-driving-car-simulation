import pygame
import sys
from constants import *
from car  import Car
from road import Road
from utils import draw_hud, draw_controls_hint

def main():
    # ── Pygame initialization ─────────────────────────────────────
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock  = pygame.font.SysFont("monospace", 14)   # HUD font
    font   = pygame.font.SysFont("monospace", 14)
    timer  = pygame.time.Clock()

    # ── Create game objects ────────────────────────────────────────
    road = Road()
    car  = Car(CAR_START_X, CAR_START_Y)

    # ── Main game loop ─────────────────────────────────────────────
    running = True
    while running:

        # 1. Event handling (window close, keyboard quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 2. Read continuous key state (held-down keys)
        keys = pygame.key.get_pressed()

        # 3. Update car physics from input
        car.handle_input(keys)

        # 4. Update car position + boundary checks
        car.update(road)

        # 5. Scroll road at car's speed (creates illusion of movement)
        road.update(car.speed)

        # 6. Draw everything
        screen.fill(BLACK)           # Clear screen first
        road.draw(screen)            # Road layer
        car.draw(screen)             # Car on top of road

        # HUD overlay
        telemetry = car.get_telemetry()
        draw_hud(screen, telemetry, font)
        draw_controls_hint(screen, font)

        # 7. Flip buffer to display (double buffering prevents flicker)
        pygame.display.flip()

        # 8. Cap at FPS to keep speed consistent across machines
        timer.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()