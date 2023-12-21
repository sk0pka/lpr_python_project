import numpy as np

DT = 0.001  # Time step
LENG = 4    # Box length
HALF = LENG / 2  # Half the box length


class Particle:
    """Particle class representing a particle in the simulation."""
    
    def __init__(self, c=np.zeros(3), v=np.zeros(3), a=np.zeros(3), lc=np.zeros(3), way=np.zeros(3)):
        """Initialize the particle with given attributes."""
        self.c = c  # Coordinate
        self.v = v  # Velocity
        self.a = a  # Acceleration
        self.lc = lc  # Last coordinate
        self.way = way  # Displacement from the start
    
    @staticmethod
    def to_border(c):
        """Place the particle within the boundaries of the simulation box."""
        for i in range(3):
            while not 0 <= c[i] < LENG:
                c[i] %= LENG
    
    @staticmethod
    def vec_to_virtual_copy(partc, part1c):
        """Compute the vector pointing to a virtual copy of another particle."""
        vect_r = part1c - partc
        for i in range(3):
            if vect_r[i] > HALF:
                vect_r[i] -= LENG
            if vect_r[i] < -HALF:
                vect_r[i] += LENG
        return vect_r
    
    def first_move(self):
        """Move the particle for the first time using the Verlet scheme."""
        self.lc[:] = self.c  # Update last coordinate
        delta_r = DT * self.v + 0.5 * self.a * DT ** 2
        self.way += delta_r
        self.c += delta_r
        self.to_border(self.c)
        self.v += DT * self.a
    
    def move(self):
        """Move the particle using the Verlet scheme."""
        delta_r = self.vec_to_virtual_copy(self.lc, self.c) + self.a * DT ** 2
        self.lc[:] = self.c  # Update last coordinate
        self.way += delta_r
        self.c += delta_r
        self.to_border(self.c)
        self.v += self.a * DT
