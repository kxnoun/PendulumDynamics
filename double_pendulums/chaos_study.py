import pygame
import math
import matplotlib.pyplot as plt
from double_pendulum_glrk4 import DoublePendulum  # Import your DoublePendulum class

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chaos Transition Study: Double Pendulum")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

origin = (width // 2, height // 4)
delta_t = 0.03

theta1_initial = math.pi / 2
theta2_initial = math.pi / 2
theta_increment = 1e-5  # Small difference for chaos study

pendulum1 = DoublePendulum(
    origin, l1=200, l2=200, m1=10, m2=10, theta1=theta1_initial, theta2=theta2_initial,
    ball_color=red, line_color=red, delta_t=delta_t
)
pendulum2 = DoublePendulum(
    origin, l1=200, l2=200, m1=10, m2=10, theta1=theta1_initial + theta_increment, theta2=theta2_initial + theta_increment,
    ball_color=blue, line_color=blue, delta_t=delta_t
)

divergence_data = []
time_data = []
time_elapsed = 0

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pendulum1.update()
    pendulum2.update()

    pendulum1.draw(screen)
    pendulum2.draw(screen)

    (x1_1, y1_1), (x2_1, y2_1) = pendulum1.get_pos()
    (x1_2, y1_2), (x2_2, y2_2) = pendulum2.get_pos()
    divergence = math.sqrt((x2_1 - x2_2) ** 2 + (y2_1 - y2_2) ** 2)

    time_elapsed += delta_t
    divergence_data.append(divergence)
    time_data.append(time_elapsed)

    pygame.display.flip()
    clock.tick(500)

pygame.quit()

plt.figure(figsize=(10, 6))
plt.plot(time_data, divergence_data, color="orange", label="Divergence")
plt.title("Chaos Transition Study: Divergence Over Time")
plt.xlabel("Simulation Time (s)")
plt.ylabel("Divergence (Euclidean Distance)")
plt.legend()
plt.grid()
plt.show()
