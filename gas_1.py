import numpy as np
import pandas as pd

# Constants
epsilon = 1.0
sigma = 1.0
mass = 1.0
dt = 0.01  # Time step
num_steps = 1000
box_size = 10.0  # Size of the simulation box

# Function to calculate LJ potential and force
def lj_force(r):
    return 24 * epsilon / r * (2 * (sigma / r)**12 - (sigma / r)**6)

# Function to apply periodic boundary conditions
def apply_periodic_boundary_conditions(positions, box_size):
    return np.mod(positions, box_size)

# Function to perform Verlet integration with periodic boundary conditions
def verlet_integration_periodic(positions, velocities, dt, box_size):
    num_particles = len(positions)
    forces = np.zeros_like(positions)

    # Apply periodic boundary conditions
    positions = apply_periodic_boundary_conditions(positions, box_size)

    # Calculate forces
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            r = positions[j] - positions[i]
            r = r - np.round(r / box_size) * box_size  # Account for PBC
            distance = np.linalg.norm(r)
            force_ij = lj_force(distance)
            direction_ij = r / distance
            forces[i] += force_ij * direction_ij
            forces[j] -= force_ij * direction_ij

    # Update positions and velocities
    positions += velocities * dt + 0.5 * forces / mass * dt**2
    new_forces = np.zeros_like(positions)
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            r = positions[j] - positions[i]
            r = r - np.round(r / box_size) * box_size  # Account for PBC
            distance = np.linalg.norm(r)
            force_ij = lj_force(distance)
            direction_ij = r / distance
            new_forces[i] += force_ij * direction_ij
            new_forces[j] -= force_ij * direction_ij
    velocities += 0.5 * (forces + new_forces) / mass * dt

    # Apply periodic boundary conditions again
    positions = apply_periodic_boundary_conditions(positions, box_size)

    return positions, velocities

# Simulation
num_particles = 10
positions = np.random.rand(num_particles, 3) * box_size
velocities = np.random.rand(num_particles, 3)

# Arrays to store kinetic energy and temperature over time
kinetic_energy = np.zeros(num_steps)
temperature = np.zeros(num_steps)

for step in range(num_steps):
    positions, velocities = verlet_integration_periodic(positions, velocities, dt, box_size)
    
    # Calculate kinetic energy and temperature
    kinetic_energy[step] = 0.5 * mass * np.sum(velocities**2)
    temperature[step] = 2 * kinetic_energy[step] / (3 * num_particles)  # Equipartition theorem

# Print average kinetic energy and temperature
average_kinetic_energy = np.mean(kinetic_energy)
average_temperature = np.mean(temperature)

# Write data to a csv file
data = {
    'Kinetic Energy': kinetic_energy,
    'Temperature': temperature
}
df = pd.DataFrame(data)
df.to_csv('simulation_data.csv', index=False)

print(f"Average Kinetic Energy: {average_kinetic_energy}")
print(f"Average Temperature: {average_temperature}")