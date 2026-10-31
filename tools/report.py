"""Progress report: per-target function counts + learning (knowledge store) stats.

Reads targets/<slug>/functions.json (ingest) and knowledge/knowledge.json
(learn/verify) to report real, oracle-aware progress — not just stubs.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "engine"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import knowledge


def _fn_count(root: pathlib.Path, slug: str) -> int:
    fj = root / slug / "functions.json"
    if fj.exists():
        try:
            data = json.loads(fj.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read function inventory {fj}: {exc}") from exc
        return data.get("num_functions", 0)
    return 0


def _function_names(root: pathlib.Path, slug: str) -> set[str]:
    asm = root / slug / "asm"
    return {path.stem for path in asm.glob("*.s")} if asm.exists() else set()


def _generated(root: pathlib.Path, slug: str) -> int:
    src = root / slug / "src"
    if not src.exists():
        return 0
    function_names = _function_names(root, slug)
    drafted_names = {
        path.stem
        for pattern in ("*.c", "*.inc")
        for path in src.glob(pattern)
    }
    return len(function_names & drafted_names)


def _has_pascal_implementation(path: pathlib.Path) -> bool:
    source = path.read_text(errors="replace")
    if "TODO: translate from asm" in source:
        return False
    source = re.sub(
        r"\{.*?\}|\(\*.*?\*\)|//[^\n]*", "", source, flags=re.DOTALL
    )
    if not re.search(r"(?im)^\s*(procedure|function)\s+[A-Za-z_]\w*", source):
        return False
    begins = list(re.finditer(r"\bbegin\b", source, re.IGNORECASE))
    endings = list(re.finditer(r"\bend\s*;", source, re.IGNORECASE))
    if not begins or not endings or endings[-1].start() <= begins[0].end():
        return False
    return bool(source[begins[0].end():endings[-1].start()].strip(" \t\r\n;"))


def _drafted(root: pathlib.Path, slug: str) -> int:
    src = root / slug / "src"
    if not src.exists():
        return 0
    function_names = _function_names(root, slug)
    return sum(
        _has_pascal_implementation(src / f"{name}.inc")
        for name in function_names
        if (src / f"{name}.inc").is_file()
    )


def _verified(root: pathlib.Path, slug: str, target_data: dict) -> int:
    function_names = _function_names(root, slug)
    verified_paths = {
        pathlib.Path(path).stem
        for paths in target_data.get("verified", {}).values()
        for path in paths
    }
    return len(function_names & verified_paths)


def _recovery_summary(root: pathlib.Path, slug: str) -> dict:
    target_root = root / slug
    if not (target_root / "recovery.json").is_file():
        return {
            "recovery_ledger": "missing",
            "source_recovered": None,
            "evidence_accounted_percent": None,
            "stale_source_recoveries": None,
        }

    from engine.recovery import audit_target

    summary = audit_target(target_root)["summary"]
    return {
        "recovery_ledger": "present",
        "source_recovered": summary["source_recovered"],
        "evidence_accounted_percent": summary["evidence_accounted_percent"],
        "stale_source_recoveries": summary["stale_source_recoveries"],
        "scoped_differential_routines_passed": summary["scoped_differential_routines_passed"],
        "scoped_differential_reports_invalid": summary["scoped_differential_reports_invalid"],
    }


def main() -> None:
    root = pathlib.Path("targets") if pathlib.Path("targets").exists() else pathlib.Path("games")
    slugs = sorted(p.name for p in root.glob("*") if p.is_dir()) if root.exists() else []

    kinds, total = {}, 0
    for s in slugs:
        y = root / s / "config" / "target.yaml"
        kinds[s] = "game"
        if y.exists():
            for line in y.read_text().splitlines():
                if line.startswith("kind:"):
                    kinds[s] = line.split(":", 1)[1].strip()
        total += _fn_count(root, s)

    kd = knowledge.load()
    targets_out = {}
    for g in slugs:
        kt = kd.get("targets", {}).get(g, {})
        verified = _verified(root, g, kt)
        targets_out[g] = {
            "kind": kinds[g],
            "functions": _fn_count(root, g),
            "generated": _generated(root, g),
            "drafted": _drafted(root, g),
            **_recovery_summary(root, g),
            "toolchain": kt.get("toolchain"),
            "verified": verified,
            "oracle": "yes" if verified else "none",
        }

    out = {
        "targets": targets_out,
        "totals": {
            "functions_ingested": total,
            "generated": sum(t["generated"] for t in targets_out.values()),
            "drafted": sum(t["drafted"] for t in targets_out.values()),
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
