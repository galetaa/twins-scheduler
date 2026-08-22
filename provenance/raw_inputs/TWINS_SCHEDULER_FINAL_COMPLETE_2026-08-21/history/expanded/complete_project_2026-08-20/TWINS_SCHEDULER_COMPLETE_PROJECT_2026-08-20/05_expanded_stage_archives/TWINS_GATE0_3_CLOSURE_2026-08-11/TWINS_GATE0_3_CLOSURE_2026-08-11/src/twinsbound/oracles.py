from __future__ import annotations

from twinsbound.model import Observation


def is_agreement_violation(observation: Observation) -> bool:
    return observation.unsafe()


def incompatibility_width(observation: Observation) -> int:
    return observation.width()


def static_k_min(observation: Observation) -> int:
    """Exact for the pilot because one deterministic branch serves one value history."""
    return observation.width()


def dynamic_active_k_min(observation: Observation) -> int:
    """Exact under reusable snapshot slot and unbounded asynchronous delay."""
    return 0 if observation.width() == 0 else 1
