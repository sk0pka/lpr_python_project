import numpy as np
import matplotlib.pyplot as plt

# Read data from files
def read_data(filename):
    with open(filename, 'r') as f:
        return np.array([float(line.strip()) for line in f])

ymec = read_data('mec.txt')
ypot = read_data('pot.txt')
ykin = read_data('kin.txt')

x = np.linspace(0, len(ymec), num=len(ymec))

# Plotting
plt.xlabel(r'Время работы программы, тиков', fontsize=14)
plt.ylabel(r'Энергия, у.е.', fontsize=14)
plt.title(r'График зависимости разных видов энергии от времени', fontsize=14)
plt.grid(True)

plt.errorbar(x, ymec, fmt='o', color='black', capsize=3, label=r'Полная механическая энергия')
plt.errorbar(x, ykin, fmt='o', color='orange', capsize=3, label=r'Кинетическая энергия частиц')
plt.errorbar(x, ypot, fmt='o', color='blue', capsize=3, label=r'Потенциальная энергия частиц')

plt.legend(loc='best', fontsize=12)
plt.tight_layout()

plt.show()
