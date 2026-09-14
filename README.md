# Intent-Based Swarm Simulator

A **safe, non-weaponized multi-agent swarm simulation** for research, algorithm development, fault injection, testing, and visualization.

> This repository intentionally simulates **survey/coverage** behavior only. It does not implement targeting, weapon control, attack planning, or real-drone flight control.

## Features

- Structured intent validation
- Greedy distance-aware task allocation
- Decentralized neighbor velocity consensus
- Soft collision/separation behavior
- Noisy stochastic movement
- Simulated packet loss
- Simulated agent failures
- Automatic task reassignment
- Dynamic replanning
- Coverage, distance, speed, communication, and failure metrics
- Monte Carlo experiments
- Matplotlib visualization
- Automated tests with `pytest`
- GitHub Actions CI

## Repository structure

```text
intent-based-swarm-simulator/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── swarm_sim/
│       ├── __init__.py
│       ├── allocation.py
│       ├── config.py
│       ├── intent.py
│       ├── metrics.py
│       ├── models.py
│       ├── simulation.py
│       ├── swarm.py
│       └── visualization.py
├── tests/
│   ├── test_allocation.py
│   ├── test_intent.py
│   └── test_simulation.py
├── outputs/
│   └── .gitkeep
├── .gitignore
├── LICENSE
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Run locally

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/intent-based-swarm-simulator.git
cd intent-based-swarm-simulator
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 4. Run tests

```bash
pytest -q
```

### 5. Run the simulator

```bash
python main.py
```

Custom run:

```bash
python main.py --agents 12 --tasks 25 --steps 500 --seed 7
```

Monte Carlo:

```bash
python main.py --runs 20 --agents 12 --tasks 25 --steps 500 --seed 7
```

Generated plots and JSON summaries are written to `outputs/`.

## GitHub Actions

Every push and pull request runs:

1. Dependency installation
2. Automated tests
3. A short smoke simulation
4. Artifact upload of simulation output

GitHub Actions is therefore used for **automated execution/testing**, while GitHub itself remains the source repository.

## Research extensions

Good next extensions for a thesis/research version include:

- Hungarian assignment
- Auction/Contract-Net allocation
- PSO/ACO/GA comparison
- Multi-objective optimization
- Graph-based communication models
- Kalman/EKF/UKF state estimation
- Sensor-fusion confidence models
- MARL/CTDE experiments
- GNN-based coordination
- Domain randomization
- Hardware-in-the-loop using non-flight-control test environments
- Statistical confidence intervals
- Ablation studies
- Scenario configuration files
- Experiment tracking

These can be evaluated entirely in simulation.

## Scope and safety

The simulator is deliberately limited to non-weaponized survey/coverage tasks. It is suitable for studying multi-agent coordination, resilience, optimization, communication loss, uncertainty, and fault tolerance without providing operational military control functionality.
