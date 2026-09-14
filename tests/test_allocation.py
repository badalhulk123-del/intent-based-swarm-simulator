import numpy as np
from src.swarm_sim.allocation import allocate_tasks
from src.swarm_sim.models import Agent, Task

def test_unique_assignments():
    agents = [
        Agent(0, np.array([0.0, 0.0]), np.zeros(2), 2.0),
        Agent(1, np.array([10.0, 0.0]), np.zeros(2), 2.0),
    ]
    tasks = [
        Task(0, np.array([1.0, 0.0])),
        Task(1, np.array([9.0, 0.0])),
    ]
    allocate_tasks(agents, tasks)
    assigned = [a.assigned_task for a in agents]
    assert len(set(assigned)) == 2
