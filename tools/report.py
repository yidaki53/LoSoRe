"""Progress report: per-target function counts + learning (knowledge store) stats.

Reads targets/<slug>/functions.json (ingest) and knowledge/knowledge.json
(learn/verify) to report real, oracle-aware progress — not just stubs.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "engine"))
import knowledge  # noqa: E402


def _fn_count(root: pathlib.Path, slug: str) -> int:
    fj = root / slug / "functions.json"
    if fj.exists():
        try:
            return json.loads(fj.read_text()).get("num_functions", 0)
        except Exception:
            return 0
    return 0


def _drafted(root: pathlib.Path, slug: str) -> int:
    src = root / slug / "src"
    return len(list(src.glob("*.c"))) if src.exists() else 0


def main() -> None:
    root = pathlib.Path("targets") if pathlib.Path("targets").exists() else pathlib.Path("games")
    slugs = sorted(p.name for p in root.glob("*") if p.is_dir()) if root.exists() else []

    kinds, total, drafted = {}, 0, 0
    for s in slugs:
        y = root / s / "config" / "target.yaml"
        kinds[s] = "game"
        if y.exists():
            for line in y.read_text().splitlines():
                if line.startswith("kind:"):
                    kinds[s] = line.split(":", 1)[1].strip()
        total += _fn_count(root, s)
        drafted += _drafted(root, s)

    kd = knowledge.load()
    targets_out = {}
    for g in slugs:
        kt = kd.get("targets", {}).get(g, {})
        targets_out[g] = {
            "kind": kinds[g],
            "functions": _fn_count(root, g),
            "drafted": _drafted(root, g),
            "toolchain": kt.get("toolchain"),
            "verified": kt.get("num_verified", 0),
            "oracle": kinds[g] and kt.get("verified", {}) and "yes" or "none",
        }

    out = {
        "targets": targets_out,
        "totals": {
            "functions_ingested": total,
            "drafted": drafted,
            "targets_seen": knowledge.stats(kd)["targets_seen"],
            "toolchains_seen": knowledge.stats(kd)["toolchains_seen"],
            "examples_total": knowledge.stats(kd)["examples_total"],
        },
    }
    pathlib.Path("reports").mkdir(exist_ok=True)
    pathlib.Path("reports/progress.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()


