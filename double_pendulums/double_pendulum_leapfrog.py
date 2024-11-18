import pygame
import math
import matplotlib.pyplot as plt
pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("bes double pendulum ever creat3d")
font = pygame.font.Font(None, 36)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
G = 9.81
FPS = 60
delta_t = 0.01
# smaller delta t is more accurate, but slow
# bigger delta t is less accurate but our sim runs faster

class DoublePendulum:
    def __init__(self, origin, l1, l2, m1, m2, theta1, theta2):
        self.origin = origin
        self.l1 = l1 # length1 from main bob to first bob
        self.l2 = l2 # length 2 from first bob to second bob
        self.m1 = m1 # mass 1
        self.m2 = m2 # mass 2
        self.theta1 = theta1
        self.theta2 = theta2
        self.vel1 = 0
        self.vel2 = 0
        self.acc1 = 0
        self.acc2 = 0
        self.drag1 = False # if were dragging the first bob
        self.drag2 = False # if were dragging the second bob

    def get_pos(self):
        #where pendulum hangs + length (our y) + sin/cos of our angle (our x)
        x1 = self.origin[0] + self.l1 * math.sin(self.theta1)
        y1 = self.origin[1] + self.l1 * math.cos(self.theta1)
        x2 = x1 + self.l2 * math.sin(self.theta2)
        y2 = y1 + self.l2 * math.cos(self.theta2)
        return (x1,y1), (x2,y2)

    def update(self):
        # if we not dragging da ball
        if not self.drag1 and not self.drag2:
            # all our physics go BOOM
            self.vel1 += 0.5 * delta_t * self.acc1
            self.vel2 += 0.5 * delta_t * self.acc2

            self.theta1 += delta_t * self.vel1
            self.theta2 += delta_t * self.vel2

            m1 = self.m1
            m2 = self.m2
            l1 = self.l1
            l2 = self.l2
            
            def compute_accelerations(theta1, theta2, vel1, vel2):
                delta_theta = theta1 - theta2
                den1 = l1 * (2 * m1 + m2 - m2 * math.cos(2 * delta_theta))
                den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * delta_theta))

                num1 = -G * (2 * m1 + m2) * math.sin(theta1)
                num2 = -m2 * G * math.sin(theta1 - 2 * theta2)
                num3 = -2 * math.sin(delta_theta) * m2
                num4 = vel2 ** 2 * l2 + vel1 ** 2 * l1 * math.cos(delta_theta)
                acc1 = (num1 + num2 + num3 * num4) / den1

                num1 = 2 * math.sin(delta_theta)
                num2 = vel1 ** 2 * l1 * (m1 + m2)
                num3 = G * (m1 + m2) * math.cos(theta1)
                num4 = vel2 ** 2 * l2 * m2 * math.cos(delta_theta)
                acc2 = num1 * (num2 + num3 + num4) / den2

                return acc1, acc2

            self.acc1, self.acc2 = compute_accelerations(self.theta1, self.theta2, self.vel1, self.vel2)
            self.vel1 += 0.5 * delta_t * self.acc1
            self.vel2 += 0.5 * delta_t * self.acc2
    

    def kinetic(self):
        v1x = self.l1 * self.vel1 * math.cos(self.theta1)
        v1y = self.l1 * self.vel1 * math.sin(self.theta1)
        v2x = v1x + self.l2 * self.vel2 * math.cos(self.theta2)
        v2y = v1y + self.l2 * self.vel2 * math.sin(self.theta2)

        return 0.5 * self.m1 * (v1x**2 + v1y**2) + 0.5 * self.m2 * (v2x**2 + v2y**2)

    def potential(self):
        """
        Calculate potential energy relative to the origin with offset to
        ensure the eq position is zero.
        """
        (x1, y1), (x2, y2) = self.get_pos()

        # calc height relative to the origin
        potential_energy = self.m1 * G * (self.origin[1] - y1) + self.m2 * G * (self.origin[1] - y2)

        # subtract potential energy at equilibrium pos (when da bob is down)
        y1_rest = self.origin[1] + self.l1
        y2_rest = y1_rest + self.l2
        potential_energy_offset = self.m1 * G * (self.origin[1] - y1_rest) + self.m2 * G * (self.origin[1] - y2_rest)

        return potential_energy - potential_energy_offset

    def total_energy(self):
        """Calculate total energy of the system."""
        return self.kinetic() + self.potential()

    def draw(self, screen):
        (x1, y1), (x2, y2) = self.get_pos()
        pygame.draw.line(screen, black, self.origin, (x1, y1), 2)
        pygame.draw.circle(screen, red if self.drag1 else black, (int(x1), int(y1)), self.m1)
        pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)
        pygame.draw.circle(screen, red if self.drag2 else black, (int(x2), int(y2)), self.m2)

    def handle_mouse_drag(self, mouse_pos):
        """Adjust the angles of the pendulum based on the mouse position."""
        if self.drag1:
            dx = mouse_pos[0] - self.origin[0]
            dy = mouse_pos[1] - self.origin[1]
            self.theta1 = math.atan2(dx, dy)
        elif self.drag2:
            (x1, y1), _ = self.get_pos()
            dx = mouse_pos[0] - x1
            dy = mouse_pos[1] - y1
            self.theta2 = math.atan2(dx, dy)

    def release(self):
        """Handle the release of the pendulum bobs."""
        self.drag1 = False
        self.drag2 = False

def draw_text(screen, text, position, font, color=black):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


origin = (width // 2, height // 4)
double_pendulum = DoublePendulum(origin, l1=200, l2=200, m1=15, m2=15, theta1=0, theta2=0)


kinetic_energies = []
potential_energies = []
total_energies = []
time_steps = []

time_step = 0
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                double_pendulum = DoublePendulum(origin, l1=200, l2=200, m1=15, m2=15, theta1=0, theta2=0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            (x1, y1), (x2, y2) = double_pendulum.get_pos()
            if (mouse_pos[0] - x1) ** 2 + (mouse_pos[1] - y1) ** 2 <= double_pendulum.m1 ** 2:
                double_pendulum.drag1 = True
            elif (mouse_pos[0] - x2) ** 2 + (mouse_pos[1] - y2) ** 2 <= double_pendulum.m2 ** 2:
                double_pendulum.drag2 = True
        elif event.type == pygame.MOUSEBUTTONUP:
            double_pendulum.release()
        elif event.type == pygame.MOUSEMOTION:
            double_pendulum.handle_mouse_drag(pygame.mouse.get_pos())

    double_pendulum.update()
    double_pendulum.draw(screen)

    # Calculate energies
    kinetic_energy = double_pendulum.kinetic()
    potential_energy = double_pendulum.potential()
    total_energy = kinetic_energy + potential_energy

    # Append energies to lists
    kinetic_energies.append(kinetic_energy)
    potential_energies.append(potential_energy)
    total_energies.append(total_energy)
    time_steps.append(time_step)

    instructions = "Space: Reset, dont reccomend lol"
    energy_text = f"Total Energy: {total_energy:.2f} | KE: {kinetic_energy:.2f} | PE: {potential_energy:.2f}"

    draw_text(screen, instructions, (10, height - 90), font)
    draw_text(screen, energy_text, (10, height - 60), font)

    time_step += 1

    pygame.display.flip()

pygame.quit()

plt.figure(figsize=(10, 6))
plt.plot(time_steps, total_energies, label="Total Energy", color='red')
plt.plot(time_steps, kinetic_energies, label="Kinetic Energy", color='green')
plt.plot(time_steps, potential_energies, label="Potential Energy", color='blue')
plt.title("Energy Over Time")
plt.xlabel("Time Step")
plt.ylabel("Energy")
plt.legend(loc="upper right")
plt.grid()
plt.show()