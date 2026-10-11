"""Scaffold targets/<slug>/ — MOVED to tools/new_target.py. Deprecated shim."""
import argparse, sys
sys.path.insert(0, "tools")
from new_target import new_target
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    print("DEPRECATED: use tools/new_target.py --slug X --kind game")
    new_target(a.slug, "game")
from __future__ import annotations
import argparse, pathlib
SKEL = ["src", "include", "asm", "config", "tools", "docs"]
CMAIN = '/* {slug}: residue stub — unmatched fns live in asm/, linked via INCLUDE_ASM. */\nint main(void){return 0;}\n'
MAKE = 'CC?=cc\nall:\n\t$(CC) -Iinclude -o build/{slug} src/main.c\n'
GIT = "# per-game: never commit BYOD\n"
def new_game(slug: str) -> None:
    root = pathlib.Path(f"games/{slug}")
    for d in SKEL:
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "build").mkdir(exist_ok=True)
    (root / "src/main.c").write_text(CMAIN.format(slug=slug))
    (root / "Makefile").write_text(MAKE.format(slug=slug))
    (root / "config/build.sha1").write_text("# <sha1> <relpath> — oracle gate\n")
    (root / "docs/PROVENANCE.md").write_text(f"# {slug} provenance\n- BYOD version/hash: TODO\n- Compiler ID: TODO\n- Oracle per fn: TODO\n")
    (root / ".gitignore").write_text(GIT)
    print(f"scaffolded {root}")
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    new_game(a.slug)
