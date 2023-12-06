import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
epsilon = 1.0
sigma = 1.0
mass = 1.0
dt = 0.01  # Time step
num_steps = 1000

# Function to calculate LJ potential and force
def lj_potential(r):
    return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)

def lj_force(r):
    return 24 * epsilon / r * (2 * (sigma / r)**12 - (sigma / r)**6)

# Function to perform Verlet integration
def verlet_integration(positions, velocities, dt):
    num_particles = len(positions)
    forces = np.zeros_like(positions)

    # Calculate forces
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            r = np.linalg.norm(positions[i] - positions[j])
            force_ij = lj_force(r)
            direction_ij = (positions[j] - positions[i]) / r
            forces[i] += force_ij * direction_ij
            forces[j] -= force_ij * direction_ij

    # Update positions and velocities
    positions += velocities * dt + 0.5 * forces / mass * dt**2
    new_forces = np.zeros_like(positions)
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            r = np.linalg.norm(positions[i] - positions[j])
            force_ij = lj_force(r)
            direction_ij = (positions[j] - positions[i]) / r
            new_forces[i] += force_ij * direction_ij
            new_forces[j] -= force_ij * direction_ij
    velocities += 0.5 * (forces + new_forces) / mass * dt

    return positions, velocities

# Simulation
num_particles = 10
positions = np.random.rand(num_particles, 3)
velocities = np.random.rand(num_particles, 3)

for step in range(num_steps):
    positions, velocities = verlet_integration(positions, velocities, dt)

# Visualization (3D plot)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
