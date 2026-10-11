"""Scaffold targets/<slug>/ compilable subfolder (splat-style, INCLUDE_ASM residue).
Kinds: game, app, firmware, driver, tool. Keeps --game compat alias.
tools/new_game.py is a deprecated shim (will be removed)."""
from __future__ import annotations
import argparse, pathlib
SKEL = ["src", "include", "asm", "config", "tools", "docs"]
CMAIN = '/* {slug} [{kind}]: residue stub — unmatched fns live in asm/, linked via INCLUDE_ASM. */\nint main(void){{return 0;}}\n'
MAKE = 'CC?=cc\nall:\n\t$(CC) -Iinclude -o build/{slug} src/main.c\n'
GIT = "# per-target: never commit BYOD\n"
def new_target(slug: str, kind: str = "game") -> None:
    root = pathlib.Path(f"targets/{slug}")
    for d in SKEL:
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "build").mkdir(exist_ok=True)
    (root / "src/main.c").write_text(CMAIN.format(slug=slug, kind=kind))
    (root / "Makefile").write_text(MAKE.format(slug=slug))
    (root / "config/build.sha1").write_text("# <sha1> <relpath> — oracle gate\n")
    (root / "config/target.yaml").write_text(f"slug: {slug}\nkind: {kind}\ncompiler: TODO\noracle: none\n")
    (root / "docs/PROVENANCE.md").write_text(
        f"# {slug} provenance\n- kind: {kind}\n- BYOD version/hash: TODO\n- Compiler ID: TODO\n- Oracle per fn: TODO\n")
    (root / ".gitignore").write_text(GIT)
    print(f"scaffolded {root} [{kind}]")
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--game", default=None, help="deprecated alias for --slug")
    ap.add_argument("--kind", default="game",
                    choices=["game", "app", "firmware", "driver", "tool"])
    a = ap.parse_args()
    new_target(a.game or a.slug, a.kind)
