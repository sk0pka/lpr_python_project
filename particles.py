import numpy as np

# Constants
TIME_STEP = 0.001
BOX_LENGTH = 4
BOX_HALF = BOX_LENGTH / 2

class Particle:
    """Particle representation"""

    def __init__(self, position=np.zeros(3), velocity=np.zeros(3), acceleration=np.zeros(3)):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.last_position = np.zeros(3) + self.position
        self.displacement = np.zeros(3)
        self.boundary_check(self.position)

    def boundary_check(self, position):
        """Ensure the particle stays within the box boundaries."""
        for i in range(3):
            while position[i] >= BOX_LENGTH or position[i] < 0:
                position[i] %= BOX_LENGTH

    def vector_to_virtual(self, other_position):
        """Return vector pointing to a virtual copy of another particle."""
        relative_vector = other_position - self.position
        for i in range(3):
            if relative_vector[i] > BOX_HALF:
                relative_vector[i] -= BOX_LENGTH
            if relative_vector[i] < -BOX_HALF:
                relative_vector[i] += BOX_LENGTH
        return relative_vector

    def initial_displacement(self):
        """Compute the initial movement of the particle."""
        displacement = TIME_STEP * self.velocity + 0.5 * self.acceleration * TIME_STEP ** 2
        self.displacement += displacement
        self.position += displacement
        self.boundary_check(self.position)
        self.velocity += TIME_STEP * self.acceleration

    def verlet_move(self):
        """Move the particle using the Verlet integration scheme."""
        displacement = self.vector_to_virtual(self.last_position) + self.acceleration * TIME_STEP ** 2
        self.last_position = np.zeros(3) + self.position
        self.displacement += displacement
        self.position += displacement
        self.boundary_check(self.position)
        self.velocity += self.acceleration * TIME_STEP
