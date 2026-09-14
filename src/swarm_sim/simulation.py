from dataclasses import dataclass
import numpy as np

from .allocation import allocate_tasks
from .config import Config
from .models import Agent, Task
from .swarm import compute_action

@dataclass
class StepRecord:
    step: int
    coverage: float
    alive_agents: int
    failures: int
    communication_events: int
    avg_speed: float

class Simulator:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.seed)
        self.agents = [
            Agent(
                id=i,
                position=self.rng.uniform(0, cfg.world_size, 2),
                velocity=np.zeros(2),
                max_speed=cfg.max_speed,
            )
            for i in range(cfg.n_agents)
        ]
        self.tasks = [
            Task(
                id=i,
                position=self.rng.uniform(0, cfg.world_size, 2),
            )
            for i in range(cfg.n_tasks)
        ]
        self.trajectories = {a.id: [a.position.copy()] for a in self.agents}
        self.records = []
        self.failures = 0
        self.communication_events = 0

    def coverage(self):
        return sum(t.completed for t in self.tasks) / max(1, len(self.tasks))

    def communicate(self, step):
        alive = [a for a in self.agents if a.alive]
        events = 0
        for a in alive:
            for b in alive:
                if a.id == b.id:
                    continue
                if np.linalg.norm(a.position - b.position) <= self.cfg.neighbor_radius:
                    if self.rng.random() >= self.cfg.packet_loss_probability:
                        a.last_contact[b.id] = step
                        events += 1
        self.communication_events += events
        return events

    def inject_failures(self):
        for agent in self.agents:
            if agent.alive and self.rng.random() < self.cfg.failure_probability_per_step:
                agent.alive = False
                self.failures += 1
                if agent.assigned_task is not None:
                    task = next((t for t in self.tasks if t.id == agent.assigned_task), None)
                    if task is not None and not task.completed:
                        task.assigned_to = None
                agent.assigned_task = None

    def update_tasks(self):
        for agent in self.agents:
            if not agent.alive or agent.assigned_task is None:
                continue
            task = next((t for t in self.tasks if t.id == agent.assigned_task), None)
            if task and not task.completed:
                if np.linalg.norm(agent.position - task.position) <= self.cfg.task_radius:
                    task.completed = True
                    task.assigned_to = None
                    agent.assigned_task = None
                    agent.completed_tasks += 1

    def safe_boundary(self, agent):
        agent.position = np.clip(agent.position, 0, self.cfg.world_size)

    def run(self, required_coverage=0.90):
        for step in range(self.cfg.steps):
            if step % self.cfg.replan_interval == 0:
                allocate_tasks(self.agents, self.tasks)

            events = self.communicate(step)
            self.inject_failures()

            for agent in self.agents:
                if not agent.alive:
                    continue
                action = compute_action(agent, self.agents, self.tasks, self.cfg, self.rng)
                agent.velocity += action * self.cfg.dt
                agent.velocity = np.clip(
                    agent.velocity, -agent.max_speed, agent.max_speed
                )
                agent.position += agent.velocity * self.cfg.dt
                self.safe_boundary(agent)
                self.trajectories[agent.id].append(agent.position.copy())

            self.update_tasks()

            alive = [a for a in self.agents if a.alive]
            avg_speed = float(np.mean([np.linalg.norm(a.velocity) for a in alive])) if alive else 0.0
            self.records.append(
                StepRecord(
                    step=step,
                    coverage=self.coverage(),
                    alive_agents=len(alive),
                    failures=self.failures,
                    communication_events=events,
                    avg_speed=avg_speed,
                )
            )

            if self.coverage() >= required_coverage:
                break

        return self.records
