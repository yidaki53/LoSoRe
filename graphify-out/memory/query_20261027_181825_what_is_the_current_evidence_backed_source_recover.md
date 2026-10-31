---
type: "query"
date: "2026-10-27T18:18:25.056927+00:00"
question: "What is the current evidence-backed source recovery baseline for Liero?"
contributor: "graphify"
source_nodes: ["Liero source reconstruction status", "_drafted()", "draft()"]
---

# Q: What is the current evidence-backed source recovery baseline for Liero?

## Answer

The new target recovery ledger audits 295 routine entries; this count matches both functions.json's declared/listed count and the assembly file stems, but it does not yet prove whole-executable code/data coverage. It parses 33,601 assembly instructions across 293 routines with decoded instructions, sees usable decompiler output for 289, and finds 20 non-placeholder Pascal bodies. No routine has yet been formally evidence-mapped or source-recovery-attested, so the ledger reports 0% source recovery and 0% evidence accounted. This is an attestation baseline, not a claim that prior assembly-derived routines contain no valid work. The next steps are a binary-wide code/data census and semantic candidate acceptance gates; compile success remains separate from source recovery.

## Source Nodes

- Liero source reconstruction status
- _drafted()
- draft()