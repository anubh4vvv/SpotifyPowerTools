from dataclasses import dataclass


@dataclass
class RuleResult:
    score: float
    reason: str
    weight: float