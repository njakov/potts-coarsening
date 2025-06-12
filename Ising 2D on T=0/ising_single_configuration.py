"""
Monte Carlo simulation of a 2D lattice spin system using the Ising model.

This script initializes a lattice of spins, performs Monte Carlo updates,
and tracks energy and magnetization over time. It also visualizes the lattice
and plots the evolution of energy and magnetization.

Author: njakov
Created: Mar 19 18:38:31 2020
"""

#import libraries
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#define functions 
def decision(probability):
    """ Do smth with given probability"""
    return random.random() < probability

def up(i, j):
    """ Return coordinates of up neigbour cell"""
    if i == 0:
        return (L-1, j)
    return (i-1, j)
  
def down(i, j):
    """ Return coordinates of a down neigbour cell"""
    if i == (L-1):
        return(0, j)
    return (i+1, j)

def left(i, j):
    """ Return coordinates of a left neigbour cell"""
    if j == 0:
        return(i, L-1)
    return (i, j-1)

def right(i, j):
    """ Return coordinates of a right neigbour cell"""
    if j == L-1:
        return(i, 0)
    return (i, j+1)

#every lattice cell has 4 neigbours
neighbours = [up, down, left, right]
#------------------------------------------------------------------------------
def sum_spins(i, j):
    """Sum spin values over nearest neighbours"""
    s = 0
    for neighbour in neighbours:
        s += lattice[neighbour(i, j)]
    return s
   
def hi(i, j):
    """Hamiltonian(Energy) for specific spin site i"""
    return -1*lattice[i, j]*sum_spins(i, j)
       
def energy():
    """Energy"""
    E = 0
    for i in range(L):
        for j in range(L):
            E += hi(i, j)
    return E/2

def magn():
    """Magnetization"""
    spins_up = np.count_nonzero(lattice == 1)
    spins_down = N - spins_up
    m = abs(spins_up-spins_down)/N
    return m  
#------------------------------------------------------------------------------

""" 
Intialize lattice

"""
#defining time, lattice dimensions and number of spins
time = 3000
L = 50
N = L*L

#We initialize lattice as 2D array with number 1 at each site
#where number 1 represents one spin oriented up
lattice = np.array([[1] * L for i in range(L)])

#half of a total number of spins are oriented up (1), other half is oriented down (-1)
down = 0
while down != (L*L)/2:
    random_lattice_field = random.randrange(0, L*L)
    a, b = random_lattice_field//L, random_lattice_field%L
    if lattice[a, b] != -1:
        lattice[a, b] = -1
        down += 1
        
#We randomize process of choosing spins to avoid bias"""
#------------------------------------------------------------------------------

#We update values of energy and magnetization before dynamics
#We save them in two arrays by using functions we already defined.
energy_time = [energy()]
magn_time = [magn()]


""" 
Monte Carlo algorithm

"""
#In every timestep of a simulation, every spin tries to flip (change its sign)
for step in range(1, time+1):
    for every_spin in range(N):
        
        #Spins are chosen randomly to avoid bias
        spin = random.randrange(0, L*L)
        x, y = spin//L, spin%L
        
        #Spin will flip (change its sign) if sum_spins(x, y) > 0
        if sum_spins(x, y) > 0:
            #flip
            lattice[x, y] = 1
            
        #If sum_spins(x, y) == 0, flip will happen with possibility 0.5
        elif sum_spins(x, y) == 0:
            if decision(0.5):
                lattice[x, y] = -1*lattice[x, y]
        else: 
            #Flip won't happen
            lattice[x, y] = -1
            
    #Update energy and magn at every 10th step   
    if step%10 == 0:        
        energy_time.append(energy())
        magn_time.append(magn())
        
#Make array that will match with timesteps in which we updated energy and mag     
mc_step = list(range(time+1))[::10]
#Checkout slice notation on the internet for a understanding [:::]    

# Plot Energy vs. time
plt.plot(mc_step, energy_time)
plt.title('The Energy vs. time, L= %i' % L)
plt.ylabel('Energy')
plt.xlabel('MC timestep')
plt.savefig('energy_vs_time.png', dpi=300)  # Save figure as PNG with 300 dpi resolution
plt.show()

# Plot Magnetization vs. time
plt.plot(mc_step, magn_time)
plt.title('Magnetization vs. time, L= %i' % L)
plt.ylabel('Magnetization')
plt.xlabel('MC timestep')
plt.savefig('magnetization_vs_time.png', dpi=300)
plt.show()

# Plot lattice colormap
# Define discrete colormap with two colors
cmap = mpl.colors.ListedColormap(['black', 'white'])

# Boundaries halfway between -1 and 1 to create two bins
bounds = [-1.5, 0, 1.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# Plot lattice with discrete colormap and norm
img = plt.imshow(lattice, cmap=cmap, norm=norm, origin='lower')

# Create colorbar with ticks only at -1 and 1
cbar = plt.colorbar(img, ticks=[-1, 1])
cbar.ax.set_yticklabels(['-1', '1'])  # Set exact tick labels, no intermediate values

plt.xlabel('L')
plt.ylabel('L')
plt.savefig('lattice_colormap.png', dpi=300)
plt.show()