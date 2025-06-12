# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 18:57:49 2025

@author: ninaj
"""

import os
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def decision(probability):
    """Do something with given probability"""
    return random.random() < probability

def up(i, j):
    if i == 0:
        return (L-1, j)
    return (i-1, j)

def down(i, j):
    if i == (L-1):
        return (0, j)
    return (i+1, j)

def left(i, j):
    if j == 0:
        return (i, L-1)
    return (i, j-1)

def right(i, j):
    if j == L-1:
        return (i, 0)
    return (i, j+1)

neighbours = [up, down, left, right]

def sum_spins(i, j):
    s = 0
    for neighbour in neighbours:
        s += lattice[neighbour(i, j)]
    return s

# Initialize parameters
time = 500
L = 50
N = L*L

# Initialize lattice with half spins up (1) and half spins down (-1)
lattice = np.array([[1] * L for _ in range(L)])
down = 0
while down != N/2:
    random_lattice_field = random.randrange(0, N)
    a, b = random_lattice_field // L, random_lattice_field % L
    if lattice[a, b] != -1:
        lattice[a, b] = -1
        down += 1

# Create snapshots folder if it doesn't exist
os.makedirs("snapshots", exist_ok=True)

# Define discrete colormap for plotting
cmap = mpl.colors.ListedColormap(['black', 'white'])
bounds = [-1.5, 0, 1.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# Save initial lattice snapshot at step 0
plt.figure(figsize=(6,6))
img = plt.imshow(lattice, cmap=cmap, norm=norm, origin='lower')
cbar = plt.colorbar(img, ticks=[-1, 1])
cbar.ax.set_yticklabels(['-1', '1'])
plt.xlabel('Lattice X')
plt.ylabel('Lattice Y')
plt.title('Lattice snapshot at step 0')
plt.savefig('snapshots/lattice_step_0.png', dpi=300)
plt.close()

# Monte Carlo simulation loop
for step in range(1, time + 1):
    for _ in range(N):
        spin = random.randrange(0, N)
        x, y = spin // L, spin % L

        s_sum = sum_spins(x, y)
        if s_sum > 0:
            lattice[x, y] = 1
        elif s_sum == 0:
            if decision(0.5):
                lattice[x, y] = -1 * lattice[x, y]
        else:
            lattice[x, y] = -1


    plt.figure(figsize=(6,6))
    img = plt.imshow(lattice, cmap=cmap, norm=norm, origin='lower')
    cbar = plt.colorbar(img, ticks=[-1, 1])
    cbar.ax.set_yticklabels(['-1', '1'])
    plt.xlabel('Lattice X')
    plt.ylabel('Lattice Y')
    plt.title(f'Lattice snapshot at step {step}')
    plt.savefig(f'snapshots/lattice_step_{step}.png', dpi=300)
    plt.close()
