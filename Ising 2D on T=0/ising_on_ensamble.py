from timeit import default_timer as timer
import random
import numpy as np

start = timer()

L = 50
N = L * L
time_steps = 3000
num_configs = 10

def decision(probability):
    """Return True with the given probability."""
    return random.random() < probability

def up(i):
    return (i - L) % N

def down(i):
    return (i + L) % N

def left(i):
    return i - 1 if i % L != 0 else i + L - 1

def right(i):
    return i + 1 if i % L != L - 1 else i - (L - 1)

# Precompute neighbors for all sites to speed up sum_spins
neighbors = [[left(i), right(i), up(i), down(i)] for i in range(N)]

def sum_spins(i, lattice):
    """Sum spins of the nearest neighbors of site i."""
    return sum(lattice[neighbor] for neighbor in neighbors[i])

def local_field(i, lattice):
    """Calculate local energy contribution of spin at site i."""
    return -lattice[i] * sum_spins(i, lattice)

def total_energy(lattice):
    """Calculate total energy of the lattice."""
    return sum(local_field(i, lattice) for i in range(N)) / 2

def magnetization(lattice):
    """Calculate magnetization of the lattice."""
    return np.sum(lattice) / N

# Tracking variables
no_ground_states = 0
magn_all = []
energy_all = []
magn_active = []
energy_active = []

with open(f'{num_configs}_configurations_lattices.txt', 'w') as graph_file:
    for config_idx in range(num_configs):
        # Initialize lattice with half spins up (+1) and half spins down (-1)
        lattice = np.ones(N, dtype=int)
        minus_spins = 0
        while minus_spins < N // 2:
            idx = random.randrange(N)
            if lattice[idx] != -1:
                lattice[idx] = -1
                minus_spins += 1

        for step in range(1, time_steps + 1):
            for _ in range(N):
                spin = random.randrange(N)
                ss = sum_spins(spin, lattice)
                if ss > 0:
                    lattice[spin] = 1
                elif ss == 0:
                    if decision(0.5):
                        lattice[spin] = -lattice[spin]
                else:
                    lattice[spin] = -1

            # Check for ground state after step 500 and every 50 steps
            if step >= 500 and step % 50 == 0:
                if np.count_nonzero(lattice == 1) in [0, N]:
                    no_ground_states += 1
                    break

        # Record magnetization and energy for all configurations
        magn_all.append(abs(magnetization(lattice)))
        energy_all.append(total_energy(lattice))

        # Record magnetization and energy for active (non-ground) configurations
        if step == time_steps:
            magn_active.append(magnetization(lattice))
            energy_active.append(total_energy(lattice))

        # Write lattice configuration to file
        graph_file.write(f'Configuration number: {config_idx}\n|')
        for i, spin in enumerate(lattice):
            if i > 0 and i % L == 0:
                graph_file.write('|\n|')
            graph_file.write('X' if spin == 1 else ' ')
        graph_file.write('|\n' + '_' * 79 + '\n')

        print(f'Completed configuration {config_idx + 1}/{num_configs}')

end = timer()
run_time = end - start

# Compute statistics
no_active_states = num_configs - no_ground_states
mean_magn_all = np.mean(magn_all)
mean_energy_all = np.mean(energy_all)
mean_magn_active = np.mean(magn_active) if magn_active else 0
mean_energy_active = np.mean(energy_active) if energy_active else 0

with open(f'{num_configs}_config_ensemble_data.txt', 'w') as ensemble_file:
    ensemble_file.write(
        f"""Lattice dimensions: {L}
Number of configurations: {num_configs}

Total MC steps per configuration: {time_steps}

Number of active states: {no_active_states}
Fraction of active states: {no_active_states / num_configs:.4f}

Number of ground states: {no_ground_states}
Fraction of ground states: {no_ground_states / num_configs:.4f}

Magnetization (all configs): {magn_all}
Mean magnetization (all configs): {mean_magn_all:.4f}

Energy (all configs): {energy_all}
Mean energy (all configs): {mean_energy_all:.4f}

Magnetization (active configs): {magn_active}
Mean magnetization (active configs): {mean_magn_active:.4f}

Energy (active configs): {energy_active}
Mean energy (active configs): {mean_energy_active:.4f}

Execution time: {run_time:.2f} seconds
"""
    )

print('Simulation complete.')