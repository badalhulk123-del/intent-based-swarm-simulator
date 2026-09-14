from dataclasses import dataclass

@dataclass
class Config:
    world_size: float = 100.0
    n_agents: int = 10
    n_tasks: int = 18
    steps: int = 600
    dt: float = 0.25
    max_speed: float = 2.5
    max_accel: float = 1.0
    separation_radius: float = 4.0
    task_radius: float = 3.0
    neighbor_radius: float = 25.0
    consensus_gain: float = 0.15
    sensor_noise_std: float = 0.6
    packet_loss_probability: float = 0.08
    communication_timeout: int = 12
    failure_probability_per_step: float = 0.0015
    replan_interval: int = 10
    seed: int = 7
