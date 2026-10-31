---
type: "query"
date: "2026-10-27T18:07:22.289289+00:00"
question: "How should the project define progress toward 100% Liero source recovery?"
contributor: "graphify"
source_nodes: ["Liero source reconstruction status", "_drafted()", "draft()"]
---

# Q: How should the project define progress toward 100% Liero source recovery?

## Answer

The existing graph and reconstruction documentation show that compilation, routine body presence, and dat-parity do not establish recovered source. Define progress from an audited executable census and per-routine evidence: source body accounts for assembly-derived signature/calling convention, control-flow blocks and branches, calls, state/register effects, and data references. Track inventory/evidence coverage, evidence-accounted Pascal bodies, compilation, and binary behavioral checks separately. Preserve the original Turbo Pascal structure and explicitly classify irrecoverable or ambiguous regions. Exact historical source text cannot be guaranteed from a stripped binary; the objective is complete evidence-accounted source reconstruction, not a clone.

## Source Nodes

- Liero source reconstruction status
- _drafted()
- draft()