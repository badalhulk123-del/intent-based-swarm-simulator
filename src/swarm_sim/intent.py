from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class SurveyIntent:
    objective: str = "SURVEY"
    priority: int = 3
    max_duration_steps: int = 600
    required_coverage: float = 0.90
    min_separation: float = 4.0
    allow_replanning: bool = True
    constraints: Dict[str, Any] = field(default_factory=dict)

def validate_intent(intent: SurveyIntent) -> None:
    if intent.objective != "SURVEY":
        raise ValueError("Only SURVEY intent is supported by this safe simulator.")
    if not 1 <= intent.priority <= 5:
        raise ValueError("priority must be between 1 and 5")
    if not 0.0 <= intent.required_coverage <= 1.0:
        raise ValueError("required_coverage must be between 0 and 1")
    if intent.min_separation <= 0:
        raise ValueError("min_separation must be positive")
    if intent.max_duration_steps <= 0:
        raise ValueError("max_duration_steps must be positive")
