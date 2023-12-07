import numpy as np

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

# Arrays to store kinetic energy and temperature over time
kinetic_energy = np.zeros(num_steps)
temperature = np.zeros(num_steps)

for step in range(num_steps):
    positions, velocities = verlet_integration(positions, velocities, dt)
    
    # Calculate kinetic energy and temperature
    kinetic_energy[step] = 0.5 * mass * np.sum(velocities**2)
    temperature[step] = 2 * kinetic_energy[step] / (3 * num_particles)  # Equipartition theorem

# Print average kinetic energy and temperature
average_kinetic_energy = np.mean(kinetic_energy)
average_temperature = np.mean(temperature)

print(f"Average Kinetic Energy: {average_kinetic_energy}")
print(f"Average Temperature: {average_temperature}")
