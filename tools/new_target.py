"""Scaffold targets/<slug>/ compilable subfolder (splat-style, INCLUDE_ASM residue).
Kinds: game, app, firmware, driver, tool.

Same-language policy: the scaffold does NOT presume a language. `config/target.yaml`
starts with `language: TODO`; `make provenance TARGET=<slug>` detects the original's
language into `config/toolchain.yaml`, and `make draft` emits that language. The
build Makefile below is the Turbo Pascal 7 / Free Pascal -Mtp proxy default (the
pilot toolchain); adjust per detected toolchain. Never port to another language.
"""
from __future__ import annotations
import argparse, pathlib
SKEL = ["src", "include", "asm", "config", "tools", "docs"]
# Pascal is the pilot default; provenance/draft override per detected language.
PASMAIN = ('{{ {slug} [{kind}] — residue stub; unmatched fns live in asm/ (INCLUDE_ASM).\n'
           '  Language is set by `make provenance` -> config/toolchain.yaml. }}\n'
           '{{$MODE TP}}\nprogram {prog};\nbegin\nend.\n')
MAKE = ('# {slug} — same-language rebuild (default: Turbo Pascal 7 / Free Pascal -Mtp).\n'
        '# Toolchain image: compilers/Dockerfile.dos-tp7. Adjust per detected language.\n'
        'SLUG := {slug}\nIMAGE ?= rev:dos-tp7\nBUILD := build\n\n'
        '.PHONY: all build image clean\nall: build\n\n'
        'image:\n\tdocker build -f ../../compilers/Dockerfile.dos-tp7 -t $(IMAGE) ../../compilers/\n\n'
        '# NB: paths contain spaces, so the bind-mount source must be quoted.\n'
        'build: image\n\tmkdir -p $(BUILD)\n'
        '\tdocker run --rm -v "$(CURDIR):/src" -w /src $(IMAGE) fpc -Mtp -Fi/src/src -FE/src/build -FU/src/build /src/src/$(SLUG).pas\n\n'
        'clean:\n\trm -rf $(BUILD)/*.o $(BUILD)/*.ppu $(BUILD)/$(SLUG)\n')
GIT = "# per-target: never commit BYOD\n"


def new_target(slug: str, kind: str = "game") -> None:
    root = pathlib.Path(f"targets/{slug}")
    for d in SKEL:
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "build").mkdir(exist_ok=True)
    prog = "".join(c for c in slug if c.isalnum() or c == "_") or "game"
    (root / "src" / f"{slug}.pas").write_text(PASMAIN.format(slug=slug, kind=kind, prog=prog))
    (root / "Makefile").write_text(MAKE.format(slug=slug))
    (root / "config/build.sha1").write_text("# <sha1> <relpath> — oracle gate (empty = NOT verified)\n")
    (root / "config/target.yaml").write_text(
        f"slug: {slug}\nkind: {kind}\nlanguage: TODO\ncompiler: TODO\noracle: none\n")
    (root / "docs/PROVENANCE.md").write_text(
        f"# {slug} provenance\n- kind: {kind}\n"
        f"- Run `make provenance TARGET={slug}` to detect the original's toolchain\n"
        f"  (writes config/toolchain.yaml: compiler, confidence, language).\n"
        f"- BYOD version/hash: TODO\n- Oracle per fn: TODO\n")
    (root / ".gitignore").write_text(GIT)
    print(f"scaffolded {root} [{kind}] (language: TODO — run provenance to detect)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--kind", default="game",
                    choices=["game", "app", "firmware", "driver", "tool"])
    a = ap.parse_args()
    new_target(a.slug, a.kind)
