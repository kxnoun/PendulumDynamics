import pygame
import math
import random
from double_pendulum_glrk4 import DoublePendulum

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Double Pendulums with Slightly Different Initial Conditions")
font = pygame.font.Font(None, 36)

black = (0, 0, 0)
G = 9.81
delta_t = 0.05

origin = (width // 2, height // 4)

num_pendulums = 100
initial_theta1 = math.pi / 2  # Starting at 90 degrees
initial_theta2 = math.pi / 2
theta_increment = 1e-5  # thousandth of a radian

pendulums = []
for i in range(num_pendulums):
    theta1 = initial_theta1 + i * theta_increment
    theta2 = initial_theta2 + i * theta_increment

    # Generate non-black, non-white colors
    r = random.randint(50, 255)
    g = random.randint(50, 255)
    b = random.randint(50, 255)
    color = (r, g, b)

    pendulum = DoublePendulum(
        origin=origin,
        l1=200,
        l2=200,
        m1=5,
        m2=5,
        theta1=theta1,
        theta2=theta2,
        ball_color=color,
        line_color=color,  # Use the same color for both balls and lines
        delta_t=delta_t
    )
    pendulums.append(pendulum)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(black)  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for pendulum in pendulums:
        pendulum.update()
        pendulum.draw(screen)

    pygame.display.flip()
    clock.tick(240)  # Limit to 240 FPS

pygame.quit()
