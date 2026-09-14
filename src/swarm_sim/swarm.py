import numpy as np

def limit_norm(v, max_norm):
    n = np.linalg.norm(v)
    if n <= max_norm or n == 0:
        return v
    return v * (max_norm / n)

def compute_action(agent, agents, tasks, cfg, rng):
    if not agent.alive or agent.assigned_task is None:
        return np.zeros(2)

    task = next((t for t in tasks if t.id == agent.assigned_task), None)
    if task is None or task.completed:
        return np.zeros(2)

    to_task = task.position - agent.position
    dist = np.linalg.norm(to_task)
    desired = np.zeros(2) if dist == 0 else to_task / dist * cfg.max_speed

    neighbors = [
        other for other in agents
        if other.alive and other.id != agent.id
        and np.linalg.norm(other.position - agent.position) < cfg.neighbor_radius
    ]
    if neighbors:
        mean_velocity = np.mean([n.velocity for n in neighbors], axis=0)
        desired += cfg.consensus_gain * (mean_velocity - agent.velocity)

    # Soft separation constraint.
    for other in neighbors:
        delta = agent.position - other.position
        d = np.linalg.norm(delta)
        if 0 < d < cfg.separation_radius:
            desired += (delta / d) * (cfg.separation_radius - d)

    desired = limit_norm(desired, cfg.max_speed)
    desired += rng.normal(0, 0.02, size=2)

    acceleration = (desired - agent.velocity)
    return limit_norm(acceleration, cfg.max_accel)
