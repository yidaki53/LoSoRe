#!/usr/bin/env python3
"""Generate the lightweight codebase navigation graph."""

from __future__ import annotations

import argparse
import ast
import json
import pathlib

SKIP_DIRS = {".git", ".venv", "__pycache__", "vendor", "extracted", "node_modules"}
SKIP_FILES = {"core.1", "core.2", "core.3", "core.4", "core.5"}
TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".yaml", ".yml", ".cfg", ".sh"}
FOCUS = [
    "recovery Matrix",
    "oracle verification",
    "RL action selection",
    "Pascal drafting",
    "model training and LoRA merge",
    "Liero evidence and provenance",
]


def _rel(path: pathlib.Path, root: pathlib.Path) -> str:
    return path.relative_to(root).as_posix()


def _module_name(path: str) -> str:
    if not path.endswith(".py"):
        return ""
    return path[:-3].replace("/", ".").replace(".__init__", "")


def _python_edges(path: pathlib.Path, rel: str) -> tuple[list[str], list[dict]]:
    entities: list[str] = []
    relationships: list[dict] = []
    try:
        tree = ast.parse(path.read_text(errors="replace"))
    except Exception:
        return entities, relationships
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = f"{rel}::{node.name}"
            entities.append(name)
            relationships.append({"source": rel, "target": name, "relation": "defines"})
        elif isinstance(node, ast.ClassDef):
            name = f"{rel}::{node.name}"
            entities.append(name)
            relationships.append({"source": rel, "target": name, "relation": "defines"})
        elif isinstance(node, ast.Import):
            for alias in node.names:
                relationships.append({
                    "source": rel, "target": alias.name,
                    "relation": "imports",
                })
        elif isinstance(node, ast.ImportFrom) and node.module:
            relationships.append({
                "source": rel, "target": node.module,
                "relation": "imports",
            })
    return entities, relationships


def build(root: pathlib.Path) -> dict:
    root = root.resolve()
    files: list[pathlib.Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = _rel(path, root)
        if rel.startswith(("graphify-out/", ".pytest_cache/")):
            continue
        files.append(path)
        if len(files) >= 600:
            break

    entities = []
    relationships = []
    modules: set[str] = set()
    for path in files:
        rel = _rel(path, root)
        entities.append({"name": rel, "type": "file", "source": "codebase-scan"})
        module = _module_name(rel)
        if module:
            modules.add(module)
        if path.suffix == ".py":
            names, edges = _python_edges(path, rel)
            for name in names:
                entities.append({"name": name, "type": "symbol", "source": "ast"})
            relationships.extend(edges)
        parent = pathlib.PurePosixPath(rel).parent.as_posix()
        if parent and parent != ".":
            relationships.append({"source": parent, "target": rel, "relation": "contains"})

    module_set = {name for name in modules}
    for rel in (item["name"] for item in entities if item["type"] == "file"):
        for module in module_set:
            if module and module != _module_name(rel) and module.split(".")[0] in rel:
                relationships.append({"source": rel, "target": module, "relation": "related-module"})

    seen = set()
    unique_relationships = []
    for edge in relationships:
        key = (edge["source"], edge["target"], edge["relation"])
        if key not in seen:
            seen.add(key)
            unique_relationships.append(edge)

    return {
        "summary": (
            "Repository navigation graph generated from file structure and Python AST. "
            "The authoritative clustered graph remains graphify-out/graph.json."
        ),
        "entities": entities,
        "relationships": unique_relationships[:4000],
        "focus_areas": FOCUS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="graphify/codebase.json")
    args = parser.parse_args()
    graph = build(pathlib.Path(args.root))
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n")
    print(f"wrote {output}: {len(graph['entities'])} entities, "
          f"{len(graph['relationships'])} relationships")


if __name__ == "__main__":
    main()
