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

import draft  # noqa: E402

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


def test_assembly_prompt_summarizes_branch_targets_before_translation():
    evidence = draft._assembly_evidence(
        "0000:0000  CMP AX,0x10\n"
        "0000:0002  JZ 0x0000:0x0010\n"
        "0000:0004  CALLF 0x1000:0x0100\n"
        "0000:0008  JMP 0x0000:0x0020\n"
    )

    assert "1 conditional, 1 unconditional branches, 1 calls" in evidence
    assert "direct branch targets: 0x0000:0x0010, 0x0000:0x0020" in evidence
    assert "Reconstruct basic blocks" in evidence


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


def _verified_pascal_pair(target, fn, asm, source, convention="__cdecl16near"):
    return {
        "fn": fn,
        "target": target,
        "compiler": "turbo-pascal-7",
        "platform": "dos",
        "language": "pascal",
        "oracle": "byte-exact",
        "verification_status": "verified",
        "calling_convention": convention,
        "asm": asm,
        "decomp_c": f"void {fn}(void) {{}}",
        "pascal": source,
    }


def test_verified_pascal_memory_rejects_unverified_and_placeholder_pairs():
    data = knowledge._empty()
    pair = _verified_pascal_pair(
        "old-game", "FUN_1", "0000:0000  RET",
        "procedure FUN_1;\nbegin\nend;",
    )
    pair["verification_status"] = "draft"
    try:
        knowledge.promote_verified_pascal_example(data, "turbo-pascal-7", pair)
    except ValueError as exc:
        assert "function-level oracle verification" in str(exc)
    else:
        raise AssertionError("unverified Pascal pair was accepted")

    pair["verification_status"] = "verified"
    pair["pascal"] = "procedure FUN_1;\nbegin\n  { TODO: translate }\nend;"
    try:
        knowledge.promote_verified_pascal_example(data, "turbo-pascal-7", pair)
    except ValueError as exc:
        assert "placeholder" in str(exc)
    else:
        raise AssertionError("placeholder Pascal pair was accepted")


def test_verified_pascal_retrieval_uses_assembly_anchors_and_excludes_target(tmp_path):
    data = knowledge._empty()
    store = tmp_path / "knowledge.json"
    candidates = [
        _verified_pascal_pair(
            "old-similar", "FUN_A",
            "0000:0000  PUSH BP\n0000:0001  MOV BP,SP\n"
            "0000:0003  ADD AX,0x10\n0000:0006  RET",
            "procedure FUN_A;\nbegin\n  Inc(A);\nend;",
        ),
        _verified_pascal_pair(
            "old-unrelated", "FUN_B",
            "0000:0000  XOR AX,AX\n0000:0002  INT 0x21\n0000:0004  RET",
            "procedure FUN_B;\nbegin\n  A := 0;\nend;",
        ),
        _verified_pascal_pair(
            "new-game", "FUN_C",
            "0000:0000  PUSH BP\n0000:0001  MOV BP,SP\n"
            "0000:0003  ADD AX,0x10\n0000:0006  RET",
            "procedure FUN_C;\nbegin\n  Inc(A);\nend;",
        ),
    ]
    for candidate in candidates:
        knowledge.promote_verified_pascal_example(
            data, "turbo-pascal-7", candidate, store=store
        )

    found = knowledge.verified_pascal_examples_for(
        data, "turbo-pascal-7", "dos",
        "0000:0000  PUSH BP\n0000:0001  MOV BP,SP\n"
        "0000:0003  ADD AX,0x10\n0000:0006  RET",
        exclude_target="new-game", calling_convention="__cdecl16near",
    )
    assert [example["target"] for example in found] == ["old-similar", "old-unrelated"]
    assert all(example["target"] != "new-game" for example in found)


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


def test_draft_retries_one_existing_routine_with_assembly_only_context(
    tmp_path, monkeypatch
):
    _make_target(tmp_path, "tgt-retry", nfns=2)
    target = tmp_path / "targets" / "tgt-retry"
    (target / "decomp" / "FUN_0.c").unlink()
    (target / "src").mkdir()
    (target / "src" / "tgt-retry.pas").write_text(
        "program tgtretry;\nuses LieroRuntime, LieroDat;\nbegin end.\n"
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(draft, "fewshot_context", lambda *args, **kwargs: "")
    assert draft.draft("tgt-retry") == 0

    candidate = target / "src" / "FUN_0.inc"
    sibling = target / "src" / "FUN_1.inc"
    old_candidate = candidate.read_text()
    old_sibling = sibling.read_text()
    prompts = []

    def fake_run_llm(
        prompt,
        model,
        endpoint,
        adapter=None,
        temperature=0.0,
        max_tokens=768,
    ):
        prompts.append(prompt)
        assert temperature == 0.0
        assert max_tokens == 768
        return "procedure FUN_0;\nbegin\nend;"

    monkeypatch.setattr(draft, "run_llm", fake_run_llm)
    assert draft.draft(
        "tgt-retry",
        fn="FUN_0",
        use_llm=True,
        retry_existing=True,
        repair_note="FUN_0.inc(4,3) Error: identifier not found",
        run_compile_gate=False,
    ) == 0

    assert len(prompts) == 1
    assert "identifier not found" in prompts[0]
    assert old_candidate in prompts[0]
    assert "ASSEMBLY:" in prompts[0]
    assert "REFERENCE C (Ghidra" in prompts[0]
    assert "uses LieroRuntime, LieroDat;" in (
        target / "src" / "tgt-retry.pas"
    ).read_text()
    assert "TODO: translate from asm" not in candidate.read_text()
    assert sibling.read_text() == old_sibling


def test_draft_diagnostic_capture_does_not_modify_target_sources(
    tmp_path, monkeypatch
):
    _make_target(tmp_path, "tgt-diagnostic", nfns=2)
    target = tmp_path / "targets" / "tgt-diagnostic"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(draft, "fewshot_context", lambda *args, **kwargs: "")
    monkeypatch.setattr(draft.model_training, "active_adapter_for", lambda *_args: None)
    monkeypatch.setattr(
        draft,
        "run_llm",
        lambda *args, **kwargs: (
            "procedure FUN_0;\nbegin\n  AX := 1;\nend;"
        ),
    )
    capture = tmp_path / "captures"

    result = draft.draft(
        "tgt-diagnostic",
        fn="FUN_0",
        use_llm=True,
        run_compile_gate=False,
        capture_dir=capture,
        diagnostic_only=True,
    )

    metadata = json.loads((capture / "FUN_0" / "capture.json").read_text())
    assert result == 0
    assert metadata["sanitizer_accepted"] is False
    assert metadata["rejection_reason"] == "unsupported-assembly-artifact"
    assert (capture / "FUN_0" / "completion.txt").is_file()
    assert not (target / "src").exists()


def test_read_decomp_seed_rejects_bad_instruction_stub(tmp_path):
    root = tmp_path / "target"
    decomp = root / "decomp"
    decomp.mkdir(parents=True)
    (decomp / "FUN_BAD.c").write_text(
        "/* WARNING: Control flow encountered bad instruction data */\n"
        "void FUN_BAD(void) { halt_baddata(); }\n"
    )

    assert draft.read_decomp_seed(root, "FUN_BAD") is None


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
