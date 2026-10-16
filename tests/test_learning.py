"""Tests for the learning component: knowledge store + learn stage.

The central claim is that the factory IMPROVES target-over-target: after
learning one target, a second target with the same toolchain inherits its
recipe (calling conventions, idioms) and verified few-shot examples. These
tests pin that contract against isolated temp stores, decoupled from the
committed knowledge/knowledge.json so CI is deterministic.
"""
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "engine"))

import knowledge  # noqa: E402


def _run(script, *args, cwd=None):
    return subprocess.run([sys.executable, str(REPO / script), *args],
                          capture_output=True, text=True, cwd=str(cwd or REPO))


def _make_target(root: pathlib.Path, slug: str, compiler="turbo-pascal-7",
                 platform="dos", nfns=3, language="pascal", confidence="high"):
    t = root / "targets" / slug
    (t / "config").mkdir(parents=True)
    (t / "asm").mkdir(parents=True)
    (t / "decomp").mkdir(parents=True)
    (t / "config" / "target.yaml").write_text(
        f"slug: {slug}\nkind: game\nplatform: {platform}\n"
        f"compiler: {compiler}\nlanguage: {language}\n")
    # provenance writes this evidence-backed file; learn/draft read it as the gate.
    (t / "config" / "toolchain.yaml").write_text(
        f"slug: {slug}\ncompiler: {compiler}\n"
        f"compiler_confidence: {confidence}\nlanguage: {language}\n"
        f"platform: {platform}\ndetected: 2026-01-01\n")
    fns = []
    for i in range(nfns):
        name = f"FUN_{i}"
        (t / "asm" / f"{name}.s").write_text(
            f"; entry\n0000:{i:04x}  PUSH BP\n0000:{i:04x}  MOV BP,SP\n"
            f"0000:{i:04x}  CALLF 0x2000:1234\n")
        (t / "decomp" / f"{name}.c").write_text(f"int {name}(void){{return {i};}}\n")
        fns.append({"name": name, "entry": f"0000:{i:04x}", "size": 10,
                    "num_instructions": 3, "calling_convention": "__cdecl16near",
                    "decompiled": True})
    (t / "functions.json").write_text(json.dumps(
        {"program": f"{slug}.exe", "compiler": compiler, "language": language,
         "image_base": "0000:0000", "num_functions": nfns, "functions": fns}))


def test_knowledge_store_roundtrip(tmp_path):
    store = tmp_path / "knowledge.json"
    data = knowledge._empty()
    knowledge.save(data, store)
    loaded = knowledge.load(store)
    assert loaded["version"] == knowledge.SCHEMA_VERSION
    assert loaded["compilers"] == {}


def test_compiler_key_falls_back_to_platform():
    assert knowledge.compiler_key("Turbo Pascal 7", "DOS") == "turbo pascal 7"
    assert "@" in knowledge.compiler_key("unknown", "dos")


def test_learn_creates_toolchain_recipe(tmp_path):
    _make_target(tmp_path, "tgt-a")
    r = _run("engine/learn.py", "--target", "tgt-a",
             "--store", str(tmp_path / "knowledge.json"), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    data = knowledge.load(tmp_path / "knowledge.json")
    recipe = data["compilers"]["turbo-pascal-7"]
    assert "tgt-a" in recipe["targets"]
    assert recipe["calling_conventions"].get("__cdecl16near") == 3
    assert recipe["image_bases"] == ["0000:0000"]
    # idioms learned: CALLF (far calls) must show up for a TP7 DOS target
    assert "CALLF" in recipe["top_mnemonics"]
    # few-shot examples captured
    assert len(data["examples"]["turbo-pascal-7"]) >= 1


def test_learning_transfers_to_second_target(tmp_path):
    store = tmp_path / "knowledge.json"
    _make_target(tmp_path, "tgt-a")
    _run("engine/learn.py", "--target", "tgt-a", "--store", str(store), cwd=tmp_path)
    # a DIFFERENT target, same toolchain
    _make_target(tmp_path, "tgt-b", nfns=4)
    r = _run("engine/learn.py", "--target", "tgt-b", "--store", str(store), cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    data = knowledge.load(store)
    recipe = data["compilers"]["turbo-pascal-7"]
    # both targets share ONE recipe; knowledge accumulated, not reset
    assert set(recipe["targets"]) == {"tgt-a", "tgt-b"}
    assert recipe["functions_seen"] == 7
    assert knowledge.prior_targets_with(data, "turbo-pascal-7", "dos") == \
        ["tgt-a", "tgt-b"]
    # few-shot examples available for a new same-toolchain draft
    assert len(knowledge.examples_for(data, "turbo-pascal-7", "dos")) >= 1


def test_learn_skips_without_functions_json(tmp_path):
    r = _run("engine/learn.py", "--target", "absent-target",
             "--store", str(tmp_path / "knowledge.json"), cwd=tmp_path)
    assert r.returncode == 0 and "SKIP" in r.stdout


def test_record_verified_closes_loop(tmp_path):
    store = tmp_path / "knowledge.json"
    knowledge.save(knowledge._empty(), store)
    data = knowledge.load(store)
    knowledge.record_verified(data, "tgt-a", ["LIERO.EXE", "LEVEDIT.EXE"],
                              "byte-exact", store=store)
    data2 = knowledge.load(store)
    assert data2["targets"]["tgt-a"]["num_verified"] == 2
    assert "byte-exact" in data2["targets"]["tgt-a"]["verified"]


def test_draft_emits_same_language_pascal(tmp_path, monkeypatch):
    # seed a store with a prior target so few-shot context is non-empty
    store = tmp_path / "knowledge.json"
    _make_target(tmp_path, "tgt-a")
    _run("engine/learn.py", "--target", "tgt-a", "--store", str(store), cwd=tmp_path)
    _make_target(tmp_path, "tgt-b", nfns=2)
    monkeypatch.chdir(tmp_path)
    sys.path.insert(0, str(REPO / "engine"))
    import importlib
    import draft
    importlib.reload(draft)
    monkeypatch.setattr(draft.knowledge, "STORE", store)
    rc = draft.draft("tgt-b")
    assert rc == 0
    # same-language policy: a pascal target emits Pascal (.inc + program), NOT C
    incs = [p for p in (tmp_path / "targets" / "tgt-b" / "src").glob("*.inc")
            if p.stem != "_forward"]  # exclude the generated forward-decl header
    assert incs, "draft should emit Pascal .inc files"
    assert not list((tmp_path / "targets" / "tgt-b" / "src").glob("*.c")), \
        "no C files should be emitted for a pascal target"
    assert (tmp_path / "targets" / "tgt-b" / "src" / "tgt-b.pas").exists()
    body = incs[0].read_text()
    assert "procedure" in body or "function" in body  # Pascal routine skeleton
    assert "// --- reference: Ghidra decompiler C" in body  # C kept as //-comment ref


def test_draft_gated_on_low_confidence(tmp_path, monkeypatch):
    # unknown/low-confidence toolchain must NOT be drafted (wrong-language guard)
    _make_target(tmp_path, "tgt-low", confidence="low", language="unknown")
    monkeypatch.chdir(tmp_path)
    sys.path.insert(0, str(REPO / "engine"))
    import importlib
    import draft
    importlib.reload(draft)
    rc = draft.draft("tgt-low")
    assert rc == 0  # disc-gated SKIP, not a crash
    assert not list((tmp_path / "targets" / "tgt-low" / "src").glob("*.inc"))

