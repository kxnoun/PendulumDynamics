import math
import matplotlib.pyplot as plt
from pendulum_glrk4 import Pendulum

def simulate_pendulum(initial_angle, initial_velocity, steps=1000, step_skip=1, unwrap=False):
    pendulum = Pendulum(origin=(0, 0), length=1, mass=1, angle=initial_angle, velocity=initial_velocity)
    angles, angular_velocities = [], []

    for step in range(steps):
        if step % step_skip == 0:
            angle = pendulum.angle
            if not unwrap:
                angle = (angle + math.pi) % (2 * math.pi) - math.pi
            angles.append(angle)
            angular_velocities.append(pendulum.velocity)
        pendulum.update()

    return angles, angular_velocities

high_velocity_levels = [
    (0, 0), 
    (0.6, 0),
    (1.2, 0),
    (1.8, 0),
    (2.4, 0),
    (math.pi - 0.01, 0),
    (math.pi - 0.01, -5),
    (math.pi - 0.01, -7)
]

phase_data = []
for angle, velocity in high_velocity_levels:
    unwrap = velocity > 4 or velocity < -4  # Unwrap for all high-velocity cases
    angles, angular_velocities = simulate_pendulum(angle, velocity, steps=500, step_skip=1, unwrap=unwrap)
    phase_data.append((angles, angular_velocities))

plt.figure(figsize=(12, 8))
for i, (angles, angular_velocities) in enumerate(phase_data):
    plt.plot(angles, angular_velocities, label=f'Level {i + 1}: $\\theta={high_velocity_levels[i][0]:.2f}$, $\\omega_0={high_velocity_levels[i][1]:.2f}$')

plt.scatter(0, 0, color='blue', s=100, label='Fixed Point $(0, 0)$')

plt.xlabel("Angle \(\\theta \) [radians]", fontsize=14)
plt.ylabel("Angular Velocity \(\\omega \) [radians/s]", fontsize=14)
plt.title("Phase Portrait of the Pendulum (High Energy Levels)", fontsize=16)
plt.legend(title="Energy Levels", fontsize=12)
plt.grid(True)

plt.xlim(-math.pi, math.pi)  # Set x-axis limits
plt.xticks(
    [-math.pi, -math.pi / 2, 0, math.pi / 2, math.pi], 
    [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"], 
    fontsize=12
)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
