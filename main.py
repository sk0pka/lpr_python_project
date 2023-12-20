import numpy as np
from particles import Particle
import math
import time


# Constants
NUM_PARTICLES = 64
MAX_VELOCITY = 20.0
TIME_STEP = 0.001
BOX_LENGTH = 4

# Output file handlers
kinetic_energy_file = open('kinetic_energy.txt', 'w')
potential_energy_file = open('potential_energy.txt', 'w')
mechanical_energy_file = open('mechanical_energy.txt', 'w')
maxwell_velocity_file = open('maxwell_velocity.txt', 'w')
average_displacement_file = open('average_displacement.txt', 'w')

def initialize_particles(particles):
    """Generate initial cubic crystal lattice configuration."""
    edge_length = int(np.cbrt(NUM_PARTICLES))
    dl = BOX_LENGTH / edge_length
    dl_half = dl / 2
    n = 0
    for i in range(edge_length):
        for j in range(edge_length):
            for k in range(edge_length):
                c = dl_half + np.array([i, j, k]) * dl
                v = np.random.uniform(-MAX_VELOCITY, MAX_VELOCITY, (3))
                if n == NUM_PARTICLES - 1:
                    v = np.zeros(3)
                particles.append(Particle(c, v))
                n += 1

def reset_all_accelerations(particles):
    """Reset all particle accelerations to zero."""
    for particle in particles:
        particle.reset_acceleration()

def compute_force_between_particles(particle1, particle2):
    """Compute interaction forces between two particles."""
    r = Particle.relative_position(particle1, particle2)
    force = 24 * (2 * np.power(np.linalg.norm(r), -14) - np.power(np.linalg.norm(r), -8)) * r
    particle1.add_acceleration(-force)
    particle2.add_acceleration(force)

def compute_all_accelerations(particles):
    """Compute accelerations for all particles based on interaction forces."""
    reset_all_accelerations(particles)
    for i in range(NUM_PARTICLES - 1):
        for j in range(i + 1, NUM_PARTICLES):
            compute_force_between_particles(particles[i], particles[j])

def compute_and_record_potential_energy(particles):
    """Compute and record the potential energy of the system."""
    total_potential = 0.0
    for i in range(NUM_PARTICLES - 1):
        for j in range(i + 1, NUM_PARTICLES):
            total_potential += Particle.compute_potential_energy(particles[i], particles[j])
    potential_energy_file.write(f"{total_potential}\n")
    return total_potential

def compute_and_record_kinetic_energy(particles):
    """Compute and record the kinetic energy of the system."""
    total_kinetic = sum([particle.kinetic_energy() for particle in particles])
    kinetic_energy_file.write(f"{total_kinetic}\n")
    return total_kinetic

def display_coordinates(particles):
    coord.write(str(len(particles)) + '\n')
    coord.write('Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0" Properties=S:1:pos:R:3' + '\n')
    for particle in particles:
        coord.write(' '.join(map(str, particle.c)) + '\n')

def timego(particles, tick):
    print(0, '%')
    initial_displacement(particles)
    average_way(particles)
    for i in range(1, tick):
        move(particles)
        average_way(particles)
        if i % (tick//20) == 0:
            print(i*100/tick, '%')
    maxwellx(particles)
    print(100, '%')

def main():
    t = 50000  # ticks
    start = time.time()
    particles = []
    initialize_particles(particles)
    timego(particles, t)
    end = time.time() - start
    print(end)

if __name__ == "__main__":
    main()

# Close the files with data
kinetic_energy_file.close()
potential_energy_file.close()
mechanical_energy_file.close()
maxwell_velocity_file.close()
average_displacement_file.close()