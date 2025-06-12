# Potts coarsening on rewired lattices

This project investigates the long-time phase ordering kinetics of the 3-state Potts model on rewired two-dimensional square lattices following a zero-temperature quench. The Potts model describes a system of $N$ spins, each able to occupy one of $q$ states, which evolve through interactions with neighboring spins.

## Overview

To introduce disorder into the interaction network, the regular lattice is rewired with probability $p$ using the Watts-Strogatz algorithm, where $p$ varies between 0 and 0.95. As the outcome of such dynamics significantly varies from case to case, all results are averaged over an ensemble of 1000 realizations.

Key findings include:

- In the small-world regime ($p \in [0, 0.2]$), the phase ordering process slows compared to the regular lattice ($p=0$), and the system often fails to reach the ground state.
- For higher rewiring probabilities ($p > 0.2$), the system more frequently attains the ground state, reflecting the influence of increased randomness in the topology.
- Some domain boundaries feature "blinker" spins that can flip indefinitely without energy cost, continuously changing their orientation.

## Project Background

This work was completed as a high school research project in 2020 at the **Petnica Science Center** during the **Seminar on Physics**. The research paper based on this project was presented at the XIX **Petnica "Step into Science" Conference**, held online from December 7 to 12, 2020. The full research paper can be found in the `docs` directory of this repository.

## Repository Contents

- Simulation code implementing the 3-state Potts model on rewired lattices
- Scripts for generating rewired lattices using the Watts-Strogatz algorithm
- Analysis tools for averaging and visualizing phase ordering dynamics
- Documentation and sample results from 1000-run ensembles

## Getting Started

Instructions for running simulations and reproducing results will be provided in the `docs` folder.

---

For questions or contributions, please open an issue or contact the author.
