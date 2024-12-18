import pygame
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("bes double pendulum ever creat3d")
font = pygame.font.Font(None, 36)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
G = 9.81
delta_t = 0.03

class DoublePendulum:
    def __init__(self, origin, l1, l2, m1, m2, theta1, theta2, ball_color=black, line_color=black, delta_t=delta_t, vel1=0, vel2=0):
        self.origin = origin
        self.l1 = l1 # length1 from main bob to first bob
        self.l2 = l2 # length 2 from first bob to second bob
        self.m1 = m1 # mass 1
        self.m2 = m2 # mass 2
        self.theta1 = theta1
        self.theta2 = theta2
        self.vel1 = vel1
        self.vel2 = vel2
        self.acc1 = 0
        self.acc2 = 0
        self.drag1 = False # if were dragging the first bob
        self.drag2 = False # if were dragging the second bob
        self.ball_color = ball_color
        self.line_color = line_color
        self.delta_t=delta_t

    def get_pos(self):
        #where pendulum hangs + length (our y) + sin/cos of our angle (our x)
        x1 = self.origin[0] + self.l1 * math.sin(self.theta1)
        y1 = self.origin[1] + self.l1 * math.cos(self.theta1)
        x2 = x1 + self.l2 * math.sin(self.theta2)
        y2 = y1 + self.l2 * math.cos(self.theta2)
        return (x1,y1), (x2,y2)

    def update(self):
        if not self.drag1 and not self.drag2:
            h = self.delta_t
            m1 = self.m1
            m2 = self.m2
            l1 = self.l1
            l2 = self.l2

            y_n = np.array([self.theta1, self.theta2, self.vel1, self.vel2])
            # c1 and c2 unusued since diff equations do not depend explicitly on time
            c1 = 0.5 - math.sqrt(3)/6
            c2 = 0.5 + math.sqrt(3)/6
            a11 = 0.25
            a12 = 0.25 - math.sqrt(3)/6
            a21 = 0.25 + math.sqrt(3)/6
            a22 = 0.25
            b1 = 0.5
            b2 = 0.5

            K1_guess = np.zeros(4)
            K2_guess = np.zeros(4)

            def compute_derivatives(y):
                theta1, theta2, omega1, omega2 = y
                acc1, acc2 = compute_accelerations(theta1, theta2, omega1, omega2)
                return np.array([omega1, omega2, acc1, acc2])
            
            def compute_accelerations(theta1, theta2, omega1, omega2):
                delta_theta = theta1 - theta2
                den1 = l1 * (2 * m1 + m2 - m2 * math.cos(2 * delta_theta))
                den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * delta_theta))

                num1 = -G * (2 * m1 + m2) * math.sin(theta1)
                num2 = -m2 * G * math.sin(theta1 - 2 * theta2)
                num3 = -2 * math.sin(delta_theta) * m2
                num4 = omega2 ** 2 * l2 + omega1 ** 2 * l1 * math.cos(delta_theta)
                acc1 = (num1 + num2 + num3 * num4) / den1

                num1 = 2 * math.sin(delta_theta)
                num2 = omega1 ** 2 * l1 * (m1 + m2)
                num3 = G * (m1 + m2) * math.cos(theta1)
                num4 = omega2 ** 2 * l2 * m2 * math.cos(delta_theta)
                acc2 = num1 * (num2 + num3 + num4) / den2

                return acc1, acc2

            def residuals(K):
                K1 = K[:4]
                K2 = K[4:]

                y1 = y_n + h * (a11 * K1 + a12 * K2)
                f1 = compute_derivatives(y1)
                res1 = K1 - f1

                y2 = y_n + h * (a21 * K1 + a22 * K2)
                f2 = compute_derivatives(y2)
                res2 = K2 - f2

                return np.concatenate((res1, res2))

            K_initial = np.concatenate((K1_guess, K2_guess))
            K_solution, _ , ier, msg = fsolve(residuals, K_initial, full_output=True)

            if ier != 1: # if we cant converge, we should always be able to tho
                raise RuntimeError(msg)

            K1 = K_solution[:4]
            K2 = K_solution[4:]

            y_n_plus_1 = y_n + h * (b1 * K1 + b2 * K2)

            self.theta1 = y_n_plus_1[0]
            self.theta2 = y_n_plus_1[1]
            self.vel1 = y_n_plus_1[2]
            self.vel2 = y_n_plus_1[3]

            self.acc1, self.acc2 = compute_accelerations(self.theta1, self.theta2, self.vel1, self.vel2)
            

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
        pygame.draw.line(screen, self.line_color, self.origin, (x1, y1), 2)
        pygame.draw.circle(screen, red if self.drag1 else self.ball_color, (int(x1), int(y1)), self.m1)
        pygame.draw.line(screen, self.line_color, (x1, y1), (x2, y2), 2)
        pygame.draw.circle(screen, red if self.drag2 else self.ball_color, (int(x2), int(y2)), self.m2)

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

if __name__ == '__main__':
    origin = (width // 2, height // 4)
    double_pendulum = DoublePendulum(origin, l1=200, l2=200, m1=15, m2=15, theta1=0, theta2=0)


    kinetic_energies = []
    potential_energies = []
    total_energies = []
    time_steps = []
    theta1_list, theta2_list, omega1_list, omega2_list = [], [], [], []


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

        theta1_list.append(double_pendulum.theta1)
        theta2_list.append(double_pendulum.theta2)
        omega1_list.append(double_pendulum.vel1)
        omega2_list.append(double_pendulum.vel2)

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
    plt.title("GLRK4: Double Pendulum Energy Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Energy")
    plt.legend(loc="upper right")
    delta_t_text = f"Time step (\u0394t): {delta_t:.2f}s"
    plt.text(1.05, 0.05, delta_t_text, transform=plt.gca().transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='left',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="Legend")
    plt.tight_layout(rect=[0, 0, 0.98, 1])
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, total_energies, label="Total Energy", color='red')
    plt.title("GLRK4: Double Pendulum Energy Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Energy")
    plt.legend(loc="upper right")
    delta_t_text = f"Time step (\u0394t): {delta_t:.2f}s"
    plt.text(1.05, 0.05, delta_t_text, transform=plt.gca().transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='left',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="Legend")
    plt.tight_layout(rect=[0, 0, 0.98, 1])
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(theta1_list, omega1_list, 'b-', label=r"$\theta_1$ vs $\omega_1$")
    plt.xlabel("Angle θ1 [radians]")
    plt.ylabel("Angular Velocity ω1 [radians/s]")
    plt.title("Phase Portrait: First Pendulum")
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(theta2_list, omega2_list, 'g-', label=r"$\theta_2$ vs $\omega_2$")
    plt.xlabel("Angle θ2 [radians]")
    plt.ylabel("Angular Velocity ω2 [radians/s]")
    plt.title("Phase Portrait: Second Pendulum")
    plt.legend()
    plt.grid()
    plt.show()