from dataclasses import dataclass, field
from typing import Dict, Optional
import numpy as np

@dataclass
class Task:
    id: int
    position: np.ndarray
    completed: bool = False
    assigned_to: Optional[int] = None

@dataclass
class Agent:
    id: int
    position: np.ndarray
    velocity: np.ndarray
    max_speed: float
    alive: bool = True
    assigned_task: Optional[int] = None
    last_contact: Dict[int, int] = field(default_factory=dict)
    completed_tasks: int = 0

@dataclass
class Observation:
    agent_id: int
    task_id: int
    estimated_position: np.ndarray
    confidence: float
