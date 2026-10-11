"""Scheduler: auto-templates -> agent fan-out with hit-rate monitor -> human residue.
Rule (sm64ds-decomp pattern): hit-rate <25% -> raise effort or route to humans."""
from __future__ import annotations
HIT_RATE_FLOOR = 0.25

def route(attempts: int, hits: int) -> str:
    rate = hits / max(1, attempts)
    if rate < HIT_RATE_FLOOR:
        return "human-residue"
    if rate < 0.6:
        return "agent-fanout-high-effort"
    return "agent-fanout"
