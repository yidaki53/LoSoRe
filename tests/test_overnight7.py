from tools.overnight7 import _disassemble, _file_backed_targets


def test_file_backed_targets_maps_exact_offset_and_keeps_caller_evidence(
    tmp_path,
):
    asm_dir = tmp_path / "asm"
    asm_dir.mkdir()
    (asm_dir / "FUN_CALLER.s").write_text(
        "1000:0000  JZ 0X1000:398B\n"
        "1000:0002  RET\n"
    )
    audit = {
        "target": "liero",
        "routines": [
            {
                "name": "FUN_CALLER",
                "unresolved_control_transfers": [
                    {
                        "address": "0x10000",
                        "instruction": "JZ 0X1000:398B",
                        "target": "0x1398b",
                    },
                    {
                        "address": "0x10002",
                        "instruction": "JMPF 0X0000:0000",
                        "target": "0x00000",
                    },
                ],
            }
        ],
    }
    census = {
        "summary": {"analysis_load_segment": "1000"},
        "binary": {
            "header_bytes": 0x1770,
            "actual_file_bytes": 0x6770,
            "load_image_bytes": 0x5000,
            "sha256": "binary-hash",
        },
    }

    candidates, image_start, image_end, binary_sha256 = _file_backed_targets(
        tmp_path, audit, census
    )

    assert image_start == 0x10000
    assert image_end == 0x15000
    assert binary_sha256 == "binary-hash"
    assert len(candidates) == 1
    assert candidates[0]["address"] == "0x1398b"
    assert candidates[0]["file_offset"] == "0x050fb"
    assert candidates[0]["callers"][0]["caller"] == "FUN_CALLER"
    assert len(candidates[0]["callers"][0]["context"]) == 2


def test_disassemble_keeps_all_instruction_lines(monkeypatch, tmp_path):
    class Completed:
        returncode = 0
        stderr = ""
        stdout = "\n".join(
            f" {address:05x}:\t90\t nop" for address in range(0x10000, 0x1007D)
        )

    monkeypatch.setattr(
        "tools.overnight7.subprocess.run",
        lambda *args, **kwargs: Completed(),
    )

    disassembly = _disassemble(
        tmp_path / "LIERO.EXE",
        {"address": "0x10000"},
        file_vma=0x10000,
        file_size=0x200,
        max_bytes=0x180,
    )

    assert len(disassembly.splitlines()) == 125
