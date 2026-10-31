import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "engine"))

import model_training

import knowledge


def _pair(target, fn, asm=None, pascal=None, **overrides):
    pair = {
        "example_id": f"{target}:{fn}",
        "fn": fn,
        "target": target,
        "compiler": "turbo-pascal-7",
        "platform": "dos",
        "language": "pascal",
        "oracle": "byte-exact",
        "verification_status": "verified",
        "asm": asm or "0000:0000  RET",
        "pascal": pascal or f"procedure {fn};\nbegin\n  Inc(A);\nend;",
        "calling_convention": "__cdecl16near",
    }
    return {**pair, **overrides}


def _configure_target(root, target="sample"):
    config = root / "targets" / target / "config"
    config.mkdir(parents=True)
    (config / "toolchain.yaml").write_text(
        "compiler: turbo-pascal-7\nplatform: dos\nlanguage: pascal\n"
        "compiler_confidence: high\n"
    )


def test_eligible_training_pairs_require_verified_pascal_and_deduplicate():
    data = knowledge._empty()
    data["verified_pascal_examples"]["turbo-pascal-7"] = [
        _pair("game-a", "FUN_A"),
        _pair("game-b", "FUN_B", asm="0000:0001  MOV AX,BX"),
        _pair("game-c", "FUN_C", verification_status="draft"),
        _pair("game-d", "FUN_D", pascal="procedure FUN_D;\nbegin\n  { TODO }\nend;"),
        _pair("game-e", "FUN_E", language="c"),
    ]

    eligible = model_training.eligible_examples(data, "turbo-pascal-7")
    assert [example["target"] for example in eligible] == ["game-a", "game-b"]


def test_legacy_assembly_examples_are_separate_and_labeled(tmp_path):
    for target in ("game-a", "game-b"):
        config = tmp_path / target / "config"
        asm_dir = tmp_path / target / "asm"
        decomp_dir = tmp_path / target / "decomp"
        config.mkdir(parents=True)
        asm_dir.mkdir()
        decomp_dir.mkdir()
        (config / "toolchain.yaml").write_text(
            "compiler: turbo-pascal-7\nplatform: dos\nlanguage: pascal\n"
        )
        (asm_dir / "FUN_0010.s").write_text(
            f"0000:{'0010' if target == 'game-a' else '0020'}  MOV AX, 1\n"
            "0000:0013  RET\n"
        )
        (decomp_dir / "FUN_0010.c").write_text(
            "void FUN_0010(void)\n{\n  int value = 1;\n"
            "  value += 2;\n  return;\n}\n"
        )
        (asm_dir / "FUN_0020.s").write_text(
            "0000:0020  MOV BX, 2\n0000:0023  RET\n"
        )
        (decomp_dir / "FUN_0020.c").write_text(
            "void FUN_0020(void)\n{\n  int value = 2;\n"
            "  value += 3;\n  return;\n}\n"
        )

    data = knowledge._empty()
    data["examples"]["turbo-pascal-7"] = [
        {
            "target": "game-a",
            "fn": "FUN_0010",
            "asm_head": "0000:0010  MOV AX, 1\n0000:0013  RET\n",
            "c": (
                "void FUN_0010(void)\n{\n  int value = 1;\n"
                "  value += 2;\n  return;\n}\n"
            ),
        },
        {
            "target": "invalid",
            "fn": "LIERO.DAT",
            "asm_head": "format data",
            "c": "/* format-only record */",
        }
    ]

    examples = model_training.legacy_assembly_examples(
        data, "turbo-pascal-7", targets_root=tmp_path, max_per_target=1
    )

    assert {example["target"] for example in examples} == {"game-a", "game-b"}
    assert all(example["task"] == "assembly_to_c" for example in examples)
    assert all(example["trust_status"] == "legacy-unverified" for example in examples)
    assert next(item for item in examples if item["target"] == "game-a")[
        "source_type"
    ] == "legacy-knowledge+ghidra-decompiler"
    assert next(item for item in examples if item["target"] == "game-a")["fn"] == (
        "FUN_0010"
    )
    assert "Raw assembly" in model_training.format_training_prompt(examples[0])
    assert "Ghidra-style C pseudocode" in model_training.format_training_prompt(
        examples[0]
    )
    record = model_training.training_record(examples[0])
    assert record["oracle"] is None
    assert record["completion"].startswith("void FUN_0010")


def test_training_corpus_combines_verified_pascal_and_legacy_c(tmp_path):
    examples = model_training.training_examples(
        {
            "verified_pascal_examples": {
                "turbo-pascal-7": [_pair("game-a", "FUN_PASCAL")]
            },
            "examples": {},
        },
        "turbo-pascal-7",
        targets_root=tmp_path,
    )

    assert len(examples) == 1
    assert examples[0]["task"] == "assembly_to_pascal"
    assert examples[0]["trust_status"] == "oracle-verified"


def test_target_split_keeps_projects_disjoint():
    examples = [_pair("game-a", "FUN_A"), _pair("game-a", "FUN_B"),
                _pair("game-b", "FUN_C")]

    training, validation, held_out = model_training.split_by_target(examples)

    assert held_out == "game-b"
    assert {item["target"] for item in training} == {"game-a"}
    assert {item["target"] for item in validation} == {"game-b"}
    with pytest.raises(ValueError, match="at least 2 targets"):
        model_training.split_by_target(examples[:2])


def test_export_writes_only_eligible_records(tmp_path):
    data = knowledge._empty()
    data["verified_pascal_examples"]["turbo-pascal-7"] = [
        _pair("game-a", "FUN_A"),
        _pair("game-b", "FUN_B", verification_status="draft"),
    ]
    output = tmp_path / "out" / "pairs.jsonl"

    count = model_training.export_dataset(
        data, "turbo-pascal-7", output, targets_root=tmp_path / "no-targets"
    )

    records = [json.loads(line) for line in output.read_text().splitlines()]
    assert count == len(records) == 1
    assert records[0]["target"] == "game-a"
    assert records[0]["oracle"] == "byte-exact"
    assert "Raw assembly" in records[0]["prompt"]
    assert records[0]["completion"].startswith("procedure FUN_A")


def test_auto_training_respects_new_pair_threshold(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    _configure_target(tmp_path)
    data = knowledge._empty()
    data["verified_pascal_examples"]["turbo-pascal-7"] = [
        _pair(
            "game-a" if index < 32 else "game-b",
            f"FUN_{index}",
            asm=f"0000:{index:04x} RET",
        )
        for index in range(63)
    ]
    store = tmp_path / "knowledge.json"
    knowledge.save(data, store)
    model_path = tmp_path / "base-model"
    model_path.mkdir()
    called = False

    def unexpected_training(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("training should not start below the threshold")

    monkeypatch.setattr(model_training, "train_adapter", unexpected_training)
    result = model_training.train_for_target(
        "sample", str(model_path), 64, automatic=True,
        store_path=store, state_path=tmp_path / "state.json",
        output_root=tmp_path / "adapters",
    )

    assert result == 0
    assert not called
    assert "63/64 new unique training pairs" in capsys.readouterr().out


def test_auto_training_waits_for_second_project(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    _configure_target(tmp_path)
    data = knowledge._empty()
    data["verified_pascal_examples"]["turbo-pascal-7"] = [
        _pair("sample", f"FUN_{index}", asm=f"0000:{index:04x} RET")
        for index in range(64)
    ]
    store = tmp_path / "knowledge.json"
    knowledge.save(data, store)
    model_path = tmp_path / "base-model"
    model_path.mkdir()
    monkeypatch.setattr(
        model_training, "train_adapter",
        lambda *args, **kwargs: pytest.fail("training requires two targets"),
    )

    result = model_training.train_for_target(
        "sample", str(model_path), 64, automatic=True,
        store_path=store, state_path=tmp_path / "state.json",
        output_root=tmp_path / "adapters",
    )

    assert result == 0
    assert "at least 2 projects" in capsys.readouterr().out


def test_training_requires_two_projects_before_importing_ml_stack(tmp_path):
    base_model = tmp_path / "base"
    base_model.mkdir()
    with pytest.raises(ValueError, match="at least 2 targets"):
        model_training.train_adapter(
            [_pair("only-project", "FUN_A")], base_model,
            "turbo-pascal-7", output_root=tmp_path / "adapters",
        )


def test_active_adapter_requires_local_adapter_and_base_model(tmp_path):
    state_path = tmp_path / "state.json"
    model_path = tmp_path / "base"
    adapter_path = tmp_path / "adapter"
    model_path.mkdir()
    adapter_path.mkdir()
    state_path.write_text(json.dumps({
        "toolchains": {
            "turbo-pascal-7": {
                "base_model_path": str(model_path),
                "adapter_path": str(adapter_path),
                "trained_tasks": ["assembly_to_pascal"],
            }
        }
    }))

    assert model_training.active_adapter_for(
        "turbo-pascal-7", state_path
    ) == {
        "base_model_path": str(model_path),
        "adapter_path": str(adapter_path),
    }
    assert model_training.active_adapter_for("other", state_path) is None


def test_legacy_only_adapter_is_not_activated_for_pascal(tmp_path):
    state_path = tmp_path / "state.json"
    model_path = tmp_path / "base"
    adapter_path = tmp_path / "adapter"
    model_path.mkdir()
    adapter_path.mkdir()
    state_path.write_text(json.dumps({
        "toolchains": {
            "turbo-pascal-7": {
                "base_model_path": str(model_path),
                "adapter_path": str(adapter_path),
                "trained_tasks": ["assembly_to_c"],
            }
        }
    }))

    assert model_training.active_adapter_for(
        "turbo-pascal-7", state_path
    ) is None
    assert model_training.active_adapter_for(
        "turbo-pascal-7", state_path, task="assembly_to_c"
    ) == {
        "base_model_path": str(model_path),
        "adapter_path": str(adapter_path),
    }
