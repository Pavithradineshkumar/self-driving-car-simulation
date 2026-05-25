import pygame
import sys
import random
from constants import *
from car        import Car
from road       import Road
from sensors    import SensorArray
from obstacle   import Obstacle
from ai_driver  import AIDriver
from utils      import draw_hud, draw_controls_hint

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    font   = pygame.font.SysFont("monospace", 14)
    timer  = pygame.time.Clock()

    road      = Road()
    car       = Car(CAR_START_X, CAR_START_Y)
    sensors   = SensorArray()
    ai        = AIDriver()
    obstacles = []
    spawn_timer = 0
    mode = "MANUAL"    # Start in manual; press TAB to toggle

    running = True
    while running:

        # ── Events ───────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_TAB:
                    # Toggle between manual and AI driving
                    mode = "AI" if mode == "MANUAL" else "MANUAL"
                    car.is_crashed = False   # Reset crash on mode switch
                if event.key == pygame.K_r:
                    # Reset car position and obstacles
                    car = Car(CAR_START_X, CAR_START_Y)
                    obstacles.clear()

        # ── Spawn obstacles ──────────────────────────────────────
        spawn_timer += 1
        if spawn_timer >= SPAWN_INTERVAL and len(obstacles) < MAX_OBSTACLES:
            spawn_timer = 0
            lane_centers = road.get_lane_centers()
            obstacles.append(Obstacle(lane_centers))

        # ── Update obstacles ─────────────────────────────────────
        for obs in obstacles:
            obs.update()
        # Remove obstacles that scrolled off screen
        obstacles = [o for o in obstacles if o.active]

        # ── Sensor update ────────────────────────────────────────
        sensors.update(car.x, car.y, car.angle, obstacles, road)

        # ── Car control ──────────────────────────────────────────
        if mode == "MANUAL":
            keys = pygame.key.get_pressed()
            car.handle_input(keys)
        else:
            steer, accel, brake = ai.decide(sensors.readings)
            car.apply_ai(steer, accel, brake)

        # ── AABB collision: car vs each obstacle ─────────────────
        car_rect = pygame.Rect(
            car.x - car.width  // 2,
            car.y - car.height // 2,
            car.width,
            car.height
        )
        for obs in obstacles:
            if car_rect.colliderect(obs.get_rect()):
                car.is_crashed = True
                car.speed = 0
                break
        else:
            car.is_crashed = False

        car.update(road)
        road.update(car.speed)

        # ── Draw ─────────────────────────────────────────────────
        screen.fill(BLACK)
        road.draw(screen)

        for obs in obstacles:
            obs.draw(screen)

        # Draw sensors before car so car renders on top
        sensors.draw(screen)
        car.draw(screen)

        # HUD
        telemetry = car.get_telemetry()
        telemetry["mode"] = mode
        draw_hud(screen, telemetry, font)
        draw_controls_hint(screen, font)

        # Mode indicator (top center)
        mode_color = (50, 220, 120) if mode == "AI" else (220, 180, 50)
        mode_surf  = font.render(f"[ {mode} MODE — TAB to switch ]", True, mode_color)
        screen.blit(mode_surf, (SCREEN_WIDTH // 2 - mode_surf.get_width() // 2, 14))

        pygame.display.flip()
        timer.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()