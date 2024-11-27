import math
import matplotlib.pyplot as plt
from pendulum_glrk4 import Pendulum  # Replace with the actual Pendulum class import

def simulate_pendulum(initial_angle, initial_velocity, steps=2000, step_skip=10):
    pendulum = Pendulum(origin=(0, 0), length=1, mass=1, angle=initial_angle, velocity=initial_velocity)
    angles, angular_velocities = [], []

    for step in range(steps):
        if step % step_skip == 0:  # Resample data points
            angles.append(pendulum.angle)
            angular_velocities.append(pendulum.velocity)
        pendulum.update()

    return angles, angular_velocities

high_velocity_levels = [
    (math.pi, 5), 
    (math.pi / 2, 10),
    (0, 15),
    (-math.pi / 2, 20),
    (-math.pi, 25),
]

phase_data = []
for angle, velocity in high_velocity_levels:
    angles, angular_velocities = simulate_pendulum(angle, velocity, steps=2000, step_skip=10)
    phase_data.append((angles, angular_velocities))

plt.figure(figsize=(12, 8))
for i, (angles, angular_velocities) in enumerate(phase_data):
    plt.plot(angles, angular_velocities, label=f'Level {i + 1}: $\\theta={angle:.2f}$, $\\omega_0={velocity:.2f}$')

plt.xlabel("Angle \(\\theta \) [radians]", fontsize=14)
plt.ylabel("Angular Velocity \(\\omega \) [radians/s]", fontsize=14)
plt.title("Phase Portrait of the Pendulum (High Energy Levels)", fontsize=16)
plt.legend(title="Energy Levels", fontsize=12)
plt.grid(True)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
