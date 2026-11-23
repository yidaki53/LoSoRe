# LoSoRe agent instructions

Read `agents.md`, the folder-local `AGENTS.md` guides and the current
`docs/RECOVERY_TODO.md` before recovery work. `RECOVERY_STATUS.md` and
`recovery_results.json` are authoritative status; do not claim DAT parity as
source recovery. CI gates are `make lint`, `make typecheck`, pytest and the
false-status assertion in `.github/workflows/ci.yml`.
Use the configured ai-memory MCP server for cross-agent continuity, explicitly
passing workspace `robin` and project `losore` on project-scoped calls.
At session start, query current work and read pending handoffs; claim one only
when taking responsibility. After bounded milestones and before ending, save
concise decisions, changed paths, reproduction commands, measured results and
remaining blockers, then create a handoff when work remains.
Memory is historical context, not binary-backed evidence: verify current files
and sealed archives. Never store BYOD bytes, traces, candidate bodies, holdout
cases, credentials or unrelated conversation history. Follow all evidence,
same-language, no-promotion and experiment-budget rules in `agents.md`.
