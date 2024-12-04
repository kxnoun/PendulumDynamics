import math
import matplotlib.pyplot as plt
from double_pendulum_glrk4 import DoublePendulum  # Replace with the correct import

def simulate_double_pendulum(initial_conditions, steps=2000, step_skip=10):
    """
    Simulates a double pendulum for given initial conditions.

    Args:
        initial_conditions (tuple): Tuple containing (theta1, omega1, theta2, omega2).
        steps (int): Number of time steps to simulate.
        step_skip (int): Number of steps to skip for plotting.

    Returns:
        lists: Angles and angular velocities for both pendulums.
    """
    theta1, omega1, theta2, omega2 = initial_conditions
    pendulum = DoublePendulum(origin=(0,0), l1=200,l2=200,m1=15,m2=15,theta1=theta1, vel1=omega1, theta2=theta2, vel2=omega2)
    angles1, velocities1, angles2, velocities2 = [], [], [], []

    for step in range(steps):
        if step % step_skip == 0:  # Resample data points
            angles1.append(pendulum.theta1)
            velocities1.append(pendulum.vel1)
            angles2.append(pendulum.theta2)
            velocities2.append(pendulum.vel2)
        pendulum.update()

    return angles1, velocities1, angles2, velocities2

initial_conditions = [
    (math.pi / 4, 0, math.pi / 4, 0), # Opposing velocities
    (math.pi / 6, 0, math.pi / 2, 0),  # Mixed initial conditions
    (3 * math.pi / 2, 0, math.pi / 6, 0) # High-energy motion
]

phase_data = []
for conditions in initial_conditions:
    angles1, velocities1, angles2, velocities2 = simulate_double_pendulum(conditions)
    phase_data.append((angles1, velocities1, angles2, velocities2))

plt.figure(figsize=(12, 8))

for i, (angles1, velocities1, _, _) in enumerate(phase_data):
    plt.plot(angles1, velocities1, label=f'Pendulum 1 - Level {i + 1}')

plt.xlabel("Angle \( \\theta_1 \) [radians]", fontsize=14)
plt.ylabel("Angular Velocity \( \\omega_1 \) [radians/s]", fontsize=14)
plt.title("Phase Portrait of Double Pendulum (First Arm)", fontsize=16)
plt.legend(title="Energy Levels", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
for i, (_, _, angles2, velocities2) in enumerate(phase_data):
    plt.plot(angles2, velocities2, label=f'Pendulum 2 - Level {i + 1}')

plt.xlabel("Angle \( \\theta_2 \) [radians]", fontsize=14)
plt.ylabel("Angular Velocity \( \\omega_2 \) [radians/s]", fontsize=14)
plt.title("Phase Portrait of Double Pendulum (Second Arm)", fontsize=16)
plt.legend(title="Energy Levels", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
