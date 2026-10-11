# agents.md — orchestration (adapted from openrecet AGENT-WORKFLOW.md)
Tiers: R3 orchestrator (decides targets, thresholds, proof) / R2 implementer (bounded) / R1 worker (grep/run/fixtures).
Rules: no recursive delegation; never touch vendor/ or extracted/; disc-gated inputs degrade to skip; INCLUDE_ASM residue always builds; every fn labeled with oracle type.
Scope: any lost-source program (games, apps, firmware). Target kinds: game, app, firmware, driver, tool.
Fan-out: independent fns in parallel; stop if hit-rate <25% -> raise effort or route to humans (sm64ds-decomp pattern).
