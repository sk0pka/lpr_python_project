import numpy as np

<<<<<<< HEAD
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
=======
dt = float(0.001) # тик
Leng = int(4) # длина коробки
half = Leng/2 # половина длины коробки

class Particle:
    """Particle class"""
     def init(self, c=np.zeros(3), v=np.zeros(3), a=np.zeros(3), lc=np.zeros(3), way=np.zeros(3)):
        self.c = c  # coordinate
        self.v = v  # velocity
        self.a = a  # acceleration
        self.lc = lc  # last coordinate
        self.way = way  # the movement of a particle from the beginning of time
        
        # Correct the initial position based on the boundary conditions
        self.to_border()
        
    def to_border(c):
        # returns the particle to the borders of the box
        for i in np.arange(3):
            while ((c[i] >= Leng)or(c[i] < 0)):
                c[i] %= Leng
             
    def vec_to_virtual_copy(partc, part1c):
        # returns a vector directed to a virtual copy of particle "part1"
        vect_r = part1c - partc
        for i in np.arange(3):
            if (vect_r[i] > half):
                vect_r[i] -= Leng
            if (vect_r[i] < -half):
                vect_r[i] += Leng
        return vect_r
       
    def first_move(self):
        # moves the particle for the first time 
        self.lc = np.zeros(3) + self.c
        delta_r = dt*(self.v) + 0.5*(self.a)*dt**2
        self.way += delta_r
        self.c += delta_r
        Particle.to_border(self.c)
        self.v += dt*(self.a)
    
    def move(self):
        # moves the particle using the Verlet scheme
        delta_r = Particle.vec_to_virtual_copy(self.lc, self.c) + self.a*dt**2
        self.lc = np.zeros(3) + self.c
        self.way += delta_r
        self.c += delta_r
        Particle.to_border(self.c)
        self.v += self.a*dt
>>>>>>> 379679bd109159e0af1cf0e1b677b7e4acd801d1
