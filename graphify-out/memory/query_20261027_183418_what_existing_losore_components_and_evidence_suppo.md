---
type: "query"
date: "2026-10-27T18:34:18.030362+00:00"
question: "What existing LoSoRe components and evidence support the next source-recovery stages for Liero, and what are current gaps?"
contributor: "graphify"
source_nodes: ["liero", "LieroRuntime", "Verification Flow"]
---

# Q: What existing LoSoRe components and evidence support the next source-recovery stages for Liero, and what are current gaps?

## Answer

The Oct 27 graph snapshot connects Liero's Pascal entry unit to LieroDat and LieroRuntime and links those units with focused DAT/runtime tests and the general verification flow. It also distinguishes format preservation from semantic knowledge for opaque DAT bytes. The graph snapshot predates the new recovery ledger, so it does not evidence the current 295-routine ledger or executable-wide census; use the live recovery artifacts and audit as authoritative. This supports a staged plan: whole-binary census, function evidence graph, then family-based Pascal recovery with separate compile and behavior checks.

## Source Nodes

- liero
- LieroRuntime
- Verification Flow