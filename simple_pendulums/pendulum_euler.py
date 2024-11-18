import pygame
import math
import time
import matplotlib.pyplot as plt

pygame.init()
width, height = 800, 800
G = 9.81
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
delta_t = 0.01

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("bespendulum ever crEated")
font = pygame.font.Font(None, 36)

class Pendulum:
    def __init__(self, origin, mass, length, damping=1.0) -> None:
        self.origin = origin
        self.mass = mass
        self.length = length
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.dragging = False
        self.ball_color = black
        self.mouse_pos_history = []  # mouse pos
        self.max_history_length = 4
        self.throwing_enabled = False  # toggle T to throw
    
    def update(self):
        # TRUE STANDARD EULER
        if not self.dragging:
            self.angle += self.velocity * delta_t # use old velocity to update angle
            self.velocity += self.acceleration * delta_t #use old acceleration to update velocity
            self.acceleration = -(G / self.length) * math.sin(self.angle) #update acceleration
            
    
    def get_pos(self):
        x = self.origin[0] + (self.length * math.sin(self.angle))
        y = self.origin[1] + (self.length * math.cos(self.angle))
        return (x, y)
    
    def kinetic_energy(self):
        linear_velocity = self.length * self.velocity
        return 0.5 * self.mass * (linear_velocity ** 2)

    def potential_energy(self):
        _, y = self.get_pos()
        height = self.origin[1] - y + self.length
        return self.mass * G * height

    def total_energy(self):
        return self.kinetic_energy() + self.potential_energy()
    
    def draw(self, screen):
        pos = self.get_pos()
        pygame.draw.line(screen, black, self.origin, pos, 2)
        pygame.draw.circle(screen, self.ball_color, (int(pos[0]), int(pos[1])), int(self.mass))
    
    def mouse_drag(self, mouse_pos):
        if self.dragging:
            dx = mouse_pos[0] - self.origin[0]
            dy = mouse_pos[1] - self.origin[1]
            self.angle = math.atan2(dx, dy)
            current_time = time.time()
            self.mouse_pos_history.append((mouse_pos, current_time))
            if len(self.mouse_pos_history) > self.max_history_length:
                self.mouse_pos_history.pop(0)

    def release(self):
        if self.throwing_enabled and len(self.mouse_pos_history) > 1:
            total_dx = total_dy = total_dt = 0
            for i in range(len(self.mouse_pos_history) - 1):
                (x1, y1), t1 = self.mouse_pos_history[i]
                (x2, y2), t2 = self.mouse_pos_history[i + 1]
                total_dx += (x2 - x1)
                total_dy += (y2 - y1)
                total_dt += (t2 - t1)

            sens = 70
            if total_dt > 0:
                avg_velocity_x = (total_dx / total_dt) / sens
                avg_velocity_y = (total_dy / total_dt) / sens
                self.velocity = (avg_velocity_x * math.cos(self.angle) + avg_velocity_y * math.sin(self.angle)) / self.length

        self.mouse_pos_history.clear()
        self.dragging = False
        self.ball_color = black
    
def draw_text(screen, text, position, font, color=black):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

pendulum = Pendulum(origin=(width // 2, 100), length=300, mass=15)
pendulum.angle= math.pi/4
running = True
clock = pygame.time.Clock()
time_step = 0

# Data lists for plotting after the simulation
time_steps, kinetic_energies, potential_energies, total_energies = [], [], [], []

while running:
    screen.fill(white)
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        bob_x, bob_y = pendulum.get_pos()
        curr_x = mouse_pos[0] - bob_x
        curr_y = mouse_pos[1] - bob_y
        if (curr_x) ** 2 + (curr_y) ** 2 <= pendulum.mass ** 2:
            pendulum.ball_color = red
        elif not pendulum.dragging:
            pendulum.ball_color = black
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pendulum = Pendulum(origin=(width // 2, 100), length=300, mass=15)
            elif event.key == pygame.K_t:
                pendulum.throwing_enabled = not pendulum.throwing_enabled
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (curr_x) ** 2 + (curr_y) ** 2 <= pendulum.mass ** 2:
                pendulum.dragging = True
                pendulum.ball_color = red
        elif event.type == pygame.MOUSEBUTTONUP:
            pendulum.release()
        elif event.type == pygame.MOUSEMOTION:
            if pendulum.dragging:
                pendulum.mouse_drag(pygame.mouse.get_pos())

    pendulum.update()
    pendulum.draw(screen)
    
    kinetic_energy = pendulum.kinetic_energy()
    potential_energy = pendulum.potential_energy()
    total_energy = pendulum.total_energy()
    
    kinetic_energies.append(kinetic_energy)
    potential_energies.append(potential_energy)
    total_energies.append(total_energy)
    time_steps.append(time_step)

    instructions = "Space: Reset | T: Enable/Disable Throwing"
    status = f"Throwing: {'Enabled' if pendulum.throwing_enabled else 'Disabled'}"
    energy_text = f"Total Energy: {total_energy:.2f} | KE: {kinetic_energy:.2f} | PE: {potential_energy:.2f}"

    draw_text(screen, instructions, (10, height - 120), font)
    draw_text(screen, status, (10, height - 90), font)
    draw_text(screen, energy_text, (10, height - 60), font)

    time_step += 1
    if time_step == 10000: # delete later
        running = False

    pygame.display.flip()

pygame.quit()

# plot energy after
plt.figure(figsize=(10, 6))
plt.plot(time_steps, total_energies, 'r-', label="Total Energy")
#plt.plot(time_steps, kinetic_energies, 'g-', label="Kinetic Energy")
#plt.plot(time_steps, potential_energies, 'b-', label="Potential Energy")
plt.xlabel("Time Step")
plt.ylabel("Energy")
plt.title("Euler's Method: Pendulum Energy Over Time")
delta_t_text = f"Time step (\u0394t): {delta_t:.2f}s"
plt.text(1.05, 0.05, delta_t_text, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='bottom', horizontalalignment='left',
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="Legend")
plt.tight_layout(rect=[0, 0, 0.98, 1])
plt.show()
