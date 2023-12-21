import numpy as np
import matplotlib.pyplot as plt

# Read data from file
def read_data(filename):
    with open(filename, 'r') as f:
        return np.array([float(line.strip()) for line in f])

# Read velocities from file
v_x = read_data('maxw.txt')
N = len(v_x)

# Calculate temperature
T = np.sum(v_x ** 2) / N

# Plotting
plt.hist(v_x, bins=N // 3, density=True)
plt.title(r'Распределение проекции скоростей частиц на ось X', fontsize=14)
plt.xlabel(r'Скорость', fontsize=12)
plt.ylabel(r'Плотность', fontsize=12)

plt.show()

print(T)