import math
import numpy as np
import time
from particles import Particle

# Global constants
N = 8
VMAX = 20.0
DT = 0.001
LENG = 4
HALF = LENG / 2

# Open output files
kint = open('kin.txt', 'w')
pott = open('pot.txt', 'w')
mect = open('mec.txt', 'w')
maxwt = open('maxw.txt', 'w')
wayt = open('way.txt', 'w')


def cell_gen(particles):
    """Generate particles in a 3D grid."""
    n = 0
    particle_is_even = True
    edge = math.ceil(np.cbrt(N))
    dl = LENG / edge
    dl_half = dl / 2
    for i in range(edge):
        for j in range(edge):
            for k in range(edge):
                c = dl_half + np.array([i, j, k]) * dl
                v = np.random.uniform(-VMAX, VMAX, 3)
                particles.append(Particle(c, v) if particle_is_even else Particle(c, -v))
                n += 1
                if n == N:
                    return


def null_axel(particles):
    """Nullify all accelerations."""
    for particle in particles:
        particle.a = np.zeros(3)


def axel(part, part1):
    """Calculate forces of interaction between particles."""
    vect_r = Particle.vec_to_virtual_copy(part.c, part1.c)
    abs_r = np.linalg.norm(vect_r)
    ac = 24 * (2 * abs_r ** -14 - abs_r ** -8) * vect_r
    part.a -= ac
    part1.a += ac


def calc_axel(particles):
    """Calculate accelerations for all particles."""
    null_axel(particles)
    for i in range(N - 1):
        for j in range(i + 1, N):
            axel(particles[i], particles[j])


def first_move(particles):
    """Move all particles for the first time."""
    calc_axel(particles)
    for particle in particles:
        particle.first_move()


def move(particles):
    """Move all particles."""
    calc_axel(particles)
    for particle in particles:
        particle.move()


def potentwo(part, part1):
    """Calculate potential energy between two particles."""
    vect_r = Particle.vec_to_virtual_copy(part.c, part1.c)
    abs_r = np.linalg.norm(vect_r)
    return 4 * (abs_r ** -12 - abs_r ** -6)


def impulse(particles):
    """Calculate total momentum of the system."""
    total_momentum = np.sum([particle.v for particle in particles], axis=0)
    # impt.write(np.array2string(total_momentum) + '\n') # Uncomment if needed


def poten_eng(particles):
    """Calculate potential energy of the system."""
    pot = sum(potentwo(particles[i], particles[j]) for i in range(N - 1) for j in range(i + 1, N))
    pott.write(f"{pot}\n")
    return pot


def kinetic_eng(particles):
    """Calculate total kinetic energy of the system."""
    kin = sum(np.linalg.norm(particle.v) ** 2 / 2 for particle in particles)
    kint.write(f"{kin}\n")
    return kin


def energy(particles):
    """Calculate total mechanical energy of the system."""
    pot = poten_eng(particles)
    kin = kinetic_eng(particles)
    total_energy = pot + kin
    mect.write(f"{total_energy}\n")


def maxwellx(particles):
    """Write maxwell distribution in x-direction."""
    velocities = sorted([particle.v[0] for particle in particles])
    for velocity in velocities:
        maxwt.write(f"{velocity}\n")


def average_way(particles):
    """Calculate average squared displacement."""
    total_disp = sum(np.linalg.norm(particle.way) ** 2 for particle in particles)
    avg_disp = total_disp / N
    wayt.write(f"{avg_disp}\n")


def display_coordinates(particles):
    """Write particle coordinates to a file."""
    coord.write(f"{N}\n")
    coord.write('Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0" Properties=S:1:pos:R:3\n')
    for particle in particles:
        coord.write(" ".join(map(str, particle.c)) + "\n")


def timego(particles, tick):
    """Start the simulation."""
    print("0%")
    first_move(particles)
    energy(particles)
    average_way(particles)
    for i in range(1, tick):
        move(particles)
        energy(particles)
        average_way(particles)
        if i % (tick // 20) == 0:
            print(f"{i * 100 / tick}%")
    maxwellx(particles)
    print("100%")


def main():
    t = 50000
    start = time.time()
    particles = []
    cell_gen(particles)
    timego(particles, t)
    end = time.time() - start
    print(end)


if __name__ == "__main__":
    main()

# Close files
kint.close()
mect.close()
pott.close()
maxwt.close()
wayt.close()
