"""Progress report: per-function treemap stub -> reports/progress.json."""
import json, pathlib
def main() -> None:
    root = pathlib.Path("targets") if pathlib.Path("targets").exists() else pathlib.Path("games")
    slugs = sorted(p.name for p in root.glob("*") if p.is_dir()) if root.exists() else []
    kinds = {}
    for s in slugs:
        y = root / s / "config" / "target.yaml"
        kinds[s] = "game"
        if y.exists():
            for line in y.read_text().splitlines():
                if line.startswith("kind:"):
                    kinds[s] = line.split(":", 1)[1].strip()
    out = {"targets": {g: {"kind": kinds[g], "matched": 0, "total": 0, "oracle": "none"} for g in slugs}}
    pathlib.Path("reports").mkdir(exist_ok=True)
    pathlib.Path("reports/progress.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
if __name__ == "__main__":
    main()

