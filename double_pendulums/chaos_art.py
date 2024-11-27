import pygame
import math
from collections import deque
from double_pendulum_glrk4 import DoublePendulum

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Glowing Double Pendulum Trails")

black = (0, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

origin = (width // 2, height // 4)
delta_t = 0.03
pendulum = DoublePendulum(
    origin=origin,
    l1=200,
    l2=200,
    m1=5,
    m2=5,
    theta1=math.pi / 2,
    theta2=math.pi / 4,
    ball_color=white,
    line_color=white,
    delta_t=delta_t
)

fading_trail_max_length = 1200
first_bob_fading_trail = deque(maxlen=fading_trail_max_length)
second_bob_fading_trail = deque(maxlen=fading_trail_max_length)

first_bob_full_trail = []
second_bob_full_trail = []

trail_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Add alpha channel

clock = pygame.time.Clock()
running = True
simulation_ended = False

while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation_ended = True
            running = False

    pendulum.update()

    first_bob_pos, second_bob_pos = pendulum.get_pos()

    first_bob_fading_trail.append(first_bob_pos)
    second_bob_fading_trail.append(second_bob_pos)

    first_bob_full_trail.append(first_bob_pos)
    second_bob_full_trail.append(second_bob_pos)

    trail_surface.fill((0, 0, 0, 15))  # The last value (15) controls fade speed (lower = slower)

    for i in range(len(first_bob_fading_trail) - 1):
        alpha = int(255 * (i / len(first_bob_fading_trail)))  # Fade effect
        color = (0, 0, 255, alpha)  # Blue with variable alpha
        pygame.draw.line(trail_surface, color, first_bob_fading_trail[i], first_bob_fading_trail[i + 1], 2)

    for i in range(len(second_bob_fading_trail) - 1):
        alpha = int(255 * (i / len(second_bob_fading_trail)))  # Fade effect
        color = (255, 255, 255, alpha)  # White with variable alpha
        pygame.draw.line(trail_surface, color, second_bob_fading_trail[i], second_bob_fading_trail[i + 1], 2)

    pygame.draw.circle(screen, blue, (int(first_bob_pos[0]), int(first_bob_pos[1])), 8)  # First bob (blue)
    pygame.draw.circle(screen, white, (int(second_bob_pos[0]), int(second_bob_pos[1])), 8)  # Second bob (red)

    screen.blit(trail_surface, (0, 0))

    pygame.display.flip()
    clock.tick(240)

if simulation_ended:
    static_surface = pygame.Surface((width, height))
    static_surface.fill(black)

    for i in range(len(first_bob_full_trail) - 1):
        pygame.draw.line(static_surface, blue, first_bob_full_trail[i], first_bob_full_trail[i + 1], 2)

    for i in range(len(second_bob_full_trail) - 1):
        pygame.draw.line(static_surface, white, second_bob_full_trail[i], second_bob_full_trail[i + 1], 2)

    pygame.image.save(static_surface, "double_pendulum_full_trail.png")
    print("Full trail image saved as 'double_pendulum_full_trail.png'")

pygame.quit()
