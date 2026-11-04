import hashlib
import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from engine import draft
from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.routine_contract import load_contract
from tools.liero_file_probe import assemble_probe, run_dosbox
from tools.liero_startup_clear_contract import startup_cpu_contract

ROOT = pathlib.Path(__file__).resolve().parents[1]
HELPER = bytes.fromhex("0507008bd0d1dad1ead1ead1ea250800c3")
ALLOCATOR = bytes.fromhex(
    "0bc07477a33c7be87f01bff6638cd98ec18bcf8cc326c43d8cc63b36f063"
    "745f263b550677eb7206263b450477e306575351268b0d268b5d0274335351"
    "268b4d04268b5d062bc81bda83e10f03c703d604f083d200240f8bf88ec2"
    "268f05268f450226894d0426895d068bcf8cc35f0726890d26895d02585af8"
    "c333c099c303c703d604f083d200240f3b16f463720877253b06f263771f06"
    "578bf98ec3a3ee638916f0632689052689550233c050ff1efe63585af8c3ff"
    "363c7bff1efe633c0172b774b6a13c7be93cff"
)
HEAP_STARTUP = bytes.fromhex(
    "8bc4051300b104d3e88cd203c2a3de63a3e0630306d863a3e263a3ec63"
    "a3f063a3f8638e060c6426a10200a3f463c706fe63d6008c0e0064"
)


@pytest.mark.parametrize("load_segment", [0x1000, 0x1200, 0x1800])
def test_original_heap_initialization_is_conditional_not_capacity_proof(
    tmp_path, load_segment
):
    """Oracle: original bytes, actual relocations and loader minimum; no startup execution."""
    target = ROOT / "targets/liero"
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    binary, header, _, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    startup = startup_cpu_contract(binary, load_segment=load_segment)
    start = startup["startup"]["file_offset"]
    assert binary[start + 3 : start + 5] == b"\x8e\xda"
    assert "24dd:0003  MOV DS,DX" in (target / "asm/FUN_24dd_0000.s").read_text()
    relocations = _mz_relocation_locations(binary, header)
    assert binary[start + 0x11 : start + 0x49] == HEAP_STARTUP
    assert not any(start + 0x10 <= r < start + 0x49 for r in relocations)
    assert binary[start + 0xE : start + 0x11] == b"\xe8\xa0\x00"
    assert 0x11 + 0xA0 == 0xB1
    callback = binary[start + 0xD6 : start + 0xDB]
    assert callback == b"\x33\xc0\xca\x02\x00"
    assert not any(start + 0xD5 <= r < start + 0xDB for r in relocations)
    relative_ds = int.from_bytes(binary[start + 1 : start + 3], "little")
    assert startup["startup"]["relocated_ds"] == load_segment + relative_ds
    file_ds = header + relative_ds * 16
    initial_zero_cells = (0x63D8, 0x63EE, 0x63F2, 0x63F6)
    for cell in initial_zero_cells:
        assert binary[file_ds + cell : file_ds + cell + 2] == b"\x00\x00"
        assert not any(
            file_ds + cell - 1 <= r < file_ds + cell + 2 for r in relocations
        )
    after_clear_sp = startup["stack"]["after_clear"]
    assert startup["cpu"]["return_sp"] == after_clear_sp
    assert after_clear_sp + 0x13 == 0xFFFF
    heap_segment = startup["mz"]["initial_ss"] + ((after_clear_sp + 0x13) >> 4)
    minimum_end_segment = load_segment + startup["mz"]["minimum_allocation_bytes"] // 16
    assert heap_segment == minimum_end_segment
    assert heap_segment * 16 + 64000 > minimum_end_segment * 16
    begin, end = startup["clear"]["ds_range"]
    assert begin <= 0x7B3C and 0x7B3E <= end
    data_relative = relative_ds * 16
    for cell in (*initial_zero_cells, 0x63F0, 0x63F4, 0x63F8, 0x63FE, 0x6400, 0x7B3C):
        bounds = (data_relative + cell, data_relative + cell + 2)
        cpu_store = startup["cpu"]["store_module_range"]
        assert bounds[1] <= cpu_store[0] or bounds[0] >= cpu_store[1]
        assert bounds[1] <= startup["mz"]["minimum_allocation_bytes"]
        assert bounds[1] <= start - header or bounds[0] >= start - header + 0xDB
        for region in ("entry_code", "startup_prefix", "clear_code", "active_stack"):
            left, right = startup["module_relative_ranges"][region]
            assert bounds[1] <= left or bounds[0] >= right
    contract = load_contract(target, "FUN_24dd_0353")
    facts = contract["startup_heap_evidence"]
    assert facts["startup_tail_bytes_hex"] == HEAP_STARTUP.hex()
    assert facts["file_offset"] == start + 0x11
    assert facts["file_backed_zero_words"] == list(initial_zero_cells)
    assert facts["default_callback"]["bytes_hex"] == callback.hex()
    assert facts["default_callback"]["offset"] == 0xD6
    assert facts["default_callback"]["segment_origin"] == "startup CS"
    assert facts["minimum_guaranteed_spare_heap_bytes"] == 0
    assert facts["clear_covers_saved_request"] is True
    assert facts["cpu_return_projection"]["preserved"] == startup["cpu"]["preserved"]
    assert facts["cpu_return_projection"]["source_recovered"] is False
    for cell in initial_zero_cells:
        assert f"{cell:04x}" in facts["conditional_state"]
    assert "00b1" in facts["limitations"]
    ledger = json.loads((target / "recovery.json").read_text())["functions"]
    assert ledger["FUN_24dd_0353"]["status"] == "unreviewed"
    assert ledger["FUN_24dd_028a"]["status"] == "unreviewed"
    prompt = draft._build_pascal_prompt(
        target,
        "liero",
        "FUN_24dd_0353",
        "",
        "",
        "Ghidra",
        draft._decl_for(target, "FUN_24dd_0353"),
        set(),
    )
    assert "minimum allocation guarantees no spare heap" in prompt
    assert "default00d6 callback" in prompt
    assert "00b1 return/segment projection established" in prompt
    assert "TF=0" in prompt
    assert "unresolved00b1" not in prompt
    observation = facts["instrumented_initial_observation"]
    assert (
        observation["scope"]
        == "one-dosbox-startup-before0049-not-normal-run-or-allocation"
    )
    assert (
        observation["spare_heap_bytes"]
        == (observation["allocation_end_segment"] - observation["heap_start_segment"])
        * 16
    )
    assert observation["allocation_success_established"] is False
    assert observation["pascal_parity"] is False
    assert "447360" in prompt
    assert "not successful allocation" in prompt
    boundary = facts["next_external_boundary"]
    assert boundary["stop_before_startup_offset"] == 0x58
    assert boundary["service_contract_established"] is False
    assert boundary["conditional_vector_save_ds_range"] == [0x7AF0, 0x7B3C]
    assert "firstINT21 at0058" in prompt
    assert "not a service preservation guarantee" in prompt
    service = facts["instrumented_first_service_observation"]
    assert service["protected_ds_range"] == [0x63D8, 0x7B52]
    assert service["protected_memory_bytes_unchanged"] == 0x7B52 - 0x63D8
    assert service["trace_bytes"] == 12094
    assert service["service_contract_established"] is False
    assert service["pascal_parity"] is False
    assert "returnsF000:1060" in prompt
    assert "remaining18 queries" in prompt
    assert "not universal service ABI" in prompt
    bridge = facts["instrumented_first_vector_bridge"]
    assert bridge["first_store_ds_range"] == [0x7AF0, 0x7AF4]
    assert bridge["stored_offset_segment"] == [0x1060, 0xF000]
    assert bridge["memory_bytes_checked"] == 6010
    assert bridge["other_protected_bytes_unchanged"] == 6006
    assert bridge["next_input_before_mov_ah35"] == {
        "AX": 0x3502,
        "CX": 18,
        "SI": 0x23B,
        "DI": 0x7AF4,
        "DF": 0,
    }
    assert bridge["second_service_executed"] is False
    assert bridge["service_contract_established"] is False
    assert "NOT allocator outputs" in prompt
    assert "other6006 unchanged" in prompt
    assert "Stops before second query" in prompt
    second = facts["instrumented_second_service_observation"]
    assert second["trace_bytes"] == 12102
    assert second["returned_vector2_segment_offset"] == [0x70, 8]
    assert second["protected_ds_range"] == [0x63D8, 0x7B52]
    assert second["protected_memory_bytes_unchanged"] == 6010
    assert second["first_saved_slot_offset_segment"] == [0x1060, 0xF000]
    assert second["second_pointer_store_executed"] is False
    assert second["service_contract_established"] is False
    assert second["pascal_parity"] is False
    assert "returns0070:0008 matching pre-call IVT2" in prompt
    assert "remaining17 queries" in prompt
    assert "not universal DOS ABI" in prompt
    second_bridge = facts["instrumented_second_vector_bridge"]
    assert second_bridge["second_store_ds_range"] == [0x7AF4, 0x7AF8]
    assert second_bridge["stored_offset_segment"] == [8, 0x70]
    assert second_bridge["memory_bytes_checked"] == 6010
    assert second_bridge["other_protected_bytes_unchanged"] == 6006
    assert second_bridge["first_saved_slot_intact"] is True
    assert second_bridge["next_input_before_mov_ah35"] == {
        "AX": 0x351B,
        "CX": 17,
        "SI": 0x23C,
        "DI": 0x7AF8,
        "DF": 0,
    }
    assert second_bridge["third_service_executed"] is False
    assert second_bridge["service_contract_established"] is False
    assert "observedAX351b/CX17/SI023c/DI7af8/DF0" in prompt
    assert "Stops before third service" in prompt
    third = contract["startup_third_service_context"]
    assert third["trace_bytes"] == 12110
    assert third["returned_vector1b_segment_offset"] == [0xF000, 0x1060]
    assert third["protected_ds_range"] == [0x63D8, 0x7B52]
    assert third["protected_bytes_unchanged"] == 6010
    assert third["saved_slot_bytes_checked"] == 8
    assert third["third_pointer_store_executed"] is False
    assert third["service_contract_established"] is False
    assert third["pascal_parity"] is False
    assert "returnsF000:1060 matching pre-call IVT1B" in prompt
    assert "remaining16 queries" in prompt
    batch = contract["startup_vector_batch_context"]
    assert batch["queries_checked"] == 19
    assert batch["trace_bytes"] == 12238
    assert batch["saved_pointer_bytes"] == 76
    assert batch["other_protected_bytes_unchanged"] == 5934
    assert batch["stop_before_startup_offset"] == 0x64
    assert batch["allocator_entry_state_established"] is False
    assert batch["service_contract_established"] is False
    assert "not completion of later startup services" in prompt
    paths = (
        target / "config/routine_contracts.json",
        target / "asm/FUN_24dd_0000.s",
        target / "recovery.json",
        ROOT / "tools/liero_startup_clear_contract.py",
        ROOT / "engine/alternate_streams.py",
        pathlib.Path(__file__),
    )
    report = {
        "status": "conditional-startup-heap-provenance-not-allocation",
        "binary_sha256": identity,
        "load_segment": load_segment,
        "heap_start_if_premises_hold": heap_segment,
        "minimum_allocation_end_segment": minimum_end_segment,
        "minimum_guaranteed_spare_heap_bytes": 0,
        "conditional_free_list": {"offset": 0, "segment": heap_segment},
        "conditional_sentinel": {"offset": 0, "segment": heap_segment},
        "conditional_handler": {
            "offset": 0xD6,
            "segment": startup["startup"]["relocated_cs"],
            "bytes_hex": callback.hex(),
            "behavior": "XOR AX,AX; RETF2. AX0,CF0,ZF1; BX/CX/DX/SI/DI/BP and DS/ES/SS/DF unchanged. Pops return IP/CS and one argument word, advancing SP6 under valid disjoint nonwrapping stack.",
        },
        "premises": [
            "Existing successful ordinary MZ loader and startup-clear premises.",
            "Checked original00b1 return/segment projection under real-mode TF=0/no-trap/no-asynchronous-mutation premises; no CPU-family or Pascal parity claim.",
            "Entry ES is PSP; PSP:2 is the DOS allocation end, with valid readable PSP.",
            "No intervening replacement/aliasing stores or external mutations before use.",
        ],
        "blockers": [
            "Actual CPU class and the historical constant2 Pascal body's full behavior remain unverified.",
            "Later startup calls/interrupts and parent5e66 pointer/DS continuity remain unresolved.",
            "Actual PSP allocation end, valid heap capacity and callback lifetime are not observed.",
        ],
        "execution_cases": 0,
        "source_promoted": False,
        "model_requests": 0,
        "evidence_hashes": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths
        },
    }
    (tmp_path / "sources").mkdir()
    for path in paths:
        shutil.copy2(path, tmp_path / "sources" / path.name)
    (tmp_path / "result.json").write_text(json.dumps(report, indent=2) + "\n")


def test_original_allocator_dependency_and_segment_direction(tmp_path):
    """Oracle: original bytes and real relocations, conditional heap facts only."""
    target = ROOT / "targets/liero"
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    offset = header + (0x24DD - base) * 16 + 0x0353
    assert binary[offset : offset + 203] == ALLOCATOR
    assert not any(
        offset - 1 <= r < offset + 203 for r in _mz_relocation_locations(binary, header)
    )
    assert 0x035A + 3 + int.from_bytes(ALLOCATOR[8:10], "little", signed=True) == 0x04DC
    listing = (target / "asm/FUN_24dd_0353.s").read_text()
    for address, raw, text in (
        (0x0362, b"\x8e\xc1", "MOV ES,CX"),
        (0x03AC, b"\x8e\xc2", "MOV ES,DX"),
        (0x03EF, b"\x8e\xc3", "MOV ES,BX"),
    ):
        assert ALLOCATOR[address - 0x353 : address - 0x353 + 2] == raw
        assert f"24dd:{address:04x}  {text}" in listing
    assert ALLOCATOR[4:7] == b"\xa3\x3c\x7b"
    assert ALLOCATOR[10:24] == bytes.fromhex("bff6638cd98ec18bcf8cc326c43d")
    assert 0x0357 + ALLOCATOR[3] == 0x03CE
    assert ALLOCATOR[0x03CE - 0x353 : 0x03D2 - 0x353] == b"\x33\xc0\x99\xc3"
    for address in (0x0402, 0x040E):
        assert ALLOCATOR[address - 0x353 : address - 0x353 + 4] == b"\xff\x1e\xfe\x63"
    contract = load_contract(target, "FUN_24dd_0353")
    assert contract["reviewed_bytes_hex"] == ALLOCATOR.hex()
    assert contract["file_offset"] == offset
    assert contract["binary_sha256"] == identity
    assert contract["callee_contracts"] == ["FUN_24dd_04dc"]
    assert (
        contract["scope"]
        == "blocked-heap-and-handler-premises-not-allocation-acceptance"
    )
    wrapper_offset = header + (0x24DD - base) * 16 + 0x028A
    wrapper = binary[wrapper_offset : wrapper_offset + 21]
    wrapper_contract = load_contract(target, "FUN_24dd_028a")
    assert wrapper_contract["reviewed_bytes_hex"] == wrapper.hex()
    assert wrapper_contract["file_offset"] == wrapper_offset
    assert wrapper_contract["callee_contracts"] == ["FUN_24dd_0353"]
    assert wrapper[9:15] == b"\x5d\x72\x03\xca\x02\x00"
    assert 0x029F + int.from_bytes(wrapper[19:21], "little", signed=True) == 0x010F
    prompt = draft._build_pascal_prompt(
        target,
        "liero",
        "FUN_24dd_0353",
        listing,
        "",
        "Ghidra",
        draft._decl_for(target, "FUN_24dd_0353"),
        set(),
    )
    assert "FUN_24dd_04dc [original-size-rounding-projection]" in prompt
    assert "ES=entryDS" in prompt
    assert "64000" in prompt and "4000" in prompt
    assert "DS63f6" in prompt and "DS63fe" in prompt
    assert "not a proven allocation" in prompt
    ledger_path = target / "recovery.json"
    ledger = json.loads(ledger_path.read_text())["functions"]
    assert ledger["FUN_24dd_04dc"]["status"] == "source_recovered"
    assert ledger["FUN_24dd_0353"]["status"] == "unreviewed"
    paths = (
        target / "config/routine_contracts.json",
        target / "asm/FUN_24dd_0353.s",
        target / "asm/FUN_24dd_04dc.s",
        target / "asm/FUN_24dd_028a.s",
        ROOT / "engine/routine_contract.py",
        ROOT / "engine/draft.py",
        ledger_path,
        pathlib.Path(__file__),
    )
    report = {
        "status": "blocked-on-heap-state-and-handler-contract",
        "binary_sha256": identity,
        "contract": contract,
        "execution_cases": 0,
        "model_requests": 0,
        "source_promoted": False,
        "evidence_hashes": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths
        },
    }
    (tmp_path / "sources").mkdir()
    for path in paths:
        shutil.copy2(path, tmp_path / "sources" / path.name)
    (tmp_path / "result.json").write_text(json.dumps(report, indent=2) + "\n")


def test_actual_size_helper_all_unsigned_inputs(tmp_path):
    """Oracle: original17 bytes versus actual accepted source, scoped AX/DX/CF/ZF/DF."""
    target = ROOT / "targets/liero"
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    offset = header + (0x24DD - base) * 16 + 0x04DC
    assert binary[offset : offset + 17] == HELPER
    helper_contract = load_contract(target, "FUN_24dd_04dc")
    assert helper_contract["reviewed_bytes_hex"] == HELPER.hex()
    assert helper_contract["file_offset"] == offset
    assert not any(
        offset - 1 <= r < offset + 17 for r in _mz_relocation_locations(binary, header)
    )
    paths = (
        target / "src/FUN_24dd_04dc.inc",
        target / "src/LieroRuntime.pas",
        target / "asm/FUN_24dd_04dc.s",
        target / "config/routine_contracts.json",
        ROOT / "tools/liero_file_probe.py",
        ROOT / "engine/alternate_streams.py",
        pathlib.Path(__file__),
    )
    hashes = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }
    (tmp_path / "sources").mkdir()
    for path in paths:
        shutil.copy2(path, tmp_path / "sources" / path.name)
    freeze = {
        "binary_sha256": identity,
        "original_bytes_hex": HELPER.hex(),
        "file_offset": offset,
        "source_hashes": hashes,
        "cases": "All65536 unsigned AX inputs; input CF=1, DF alternates by bit0.",
        "compiler": "FPC-Mtp, existing unchecked16-bit arithmetic contract; no-Cr claim.",
        "budget": "one original execution and one actual-source compilation/execution;30s subprocess limits; no model/holdout",
        "premises": "Valid writable disjoint COM stack/code/output; no aliasing or asynchronous mutations.",
        "limitations": "Register projection only, not allocator, heap provenance, full ABI or normal-program reachability.",
    }
    (tmp_path / "freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    (tmp_path / "original.bin").write_bytes(HELPER)
    assembly = tmp_path / "harness.S"
    assembly.write_text(f"""
.code16
.global _start
_start:
    push %cs
    pop %ds
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, handle
next_case:
    mov $0x1234, %bp
    mov %sp, before_sp
    cld
    testw $1, counter
    jz invoke
    std
invoke:
    mov counter, %ax
    stc
    call original
    pushf
    pop %bx
    mov used, %di
    mov %ax, buffer(%di)
    mov %dx, buffer+2(%di)
    mov %bx, buffer+4(%di)
    mov %bp, buffer+6(%di)
    mov before_sp, %ax
    mov %ax, buffer+8(%di)
    mov %sp, buffer+10(%di)
    mov %ds, buffer+12(%di)
    mov %ss, buffer+14(%di)
    add $16, %di
    mov %di, used
    cmp $4096, %di
    jne advance
    cld
    mov handle, %bx
    mov $buffer, %dx
    mov $4096, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $4096, %ax
    jne failed
    movw $0, used
advance:
    incw counter
    jnz next_case
    mov handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    cld
    mov $0x4c01, %ax
    int $0x21
original:
.incbin "{tmp_path / "original.bin"}"
filename: .asciz "TRACE.BIN"
handle: .word 0
counter: .word 0
used: .word 0
before_sp: .word 0
buffer: .space 4096
""")
    (tmp_path / "PROBE.COM").write_bytes(assemble_probe(assembly, tmp_path))
    run_dosbox(tmp_path)
    (tmp_path / "actual_size.pas").write_text("""
program ActualSize;
uses LieroRuntime;
{$I FUN_24dd_04dc.inc}
var bits: LongInt; resultValue: Longint; outputFile: file;
    recordWords: array[0..4] of Word; written: LongInt;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  for bits := 0 to 65535 do
  begin
    RegisterAX := Word(bits);
    RegisterCarryFlag := True;
    RegisterZeroFlag := False;
    RegisterDirectionFlag := (bits and 1) <> 0;
    resultValue := FUN_24dd_04dc;
    recordWords[0] := RegisterAX; recordWords[1] := RegisterDX;
    recordWords[2] := Word(RegisterCarryFlag) +
      Word(RegisterZeroFlag) * $40 + Word(RegisterDirectionFlag) * $400;
    recordWords[3] := Word(resultValue);
    recordWords[4] := Word(resultValue shr 16);
    BlockWrite(outputFile, recordWords, 10, written);
    if written <> 10 then Halt(2);
  end;
  Close(outputFile);
end.
""")
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Fusources", "-Fisources", "-FU.", "actual_size.pas"],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(tmp_path / "actual_size")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "runtime.log").write_bytes(executed.stdout + executed.stderr)
    assert executed.returncode == 0, executed.stdout + executed.stderr
    original = (tmp_path / "TRACE.BIN").read_bytes()
    actual = (tmp_path / "PASCAL.BIN").read_bytes()
    assert len(original) == 65536 * 16 and len(actual) == 65536 * 10
    segment = struct.unpack_from("<H", original, 12)[0]
    for bits in range(65536):
        ax, dx, flags, bp, before, after, ds, ss = struct.unpack_from(
            "<8H", original, bits * 16
        )
        rounded = ((bits + 7) // 8) * 8
        assert dx * 16 + ax == rounded
        assert ax == rounded % 16 and dx == rounded // 16
        expected_flags = int(ax == 0) * 0x40 + (bits & 1) * 0x400
        assert flags & 0x441 == expected_flags
        assert bp == 0x1234 and before == after == 0xFFFE
        assert ds == ss == segment
        assert struct.unpack_from("<5H", actual, bits * 10) == (
            ax,
            dx,
            expected_flags,
            ax,
            dx,
        )
    assert struct.unpack_from("<2H", original, 64000 * 16) == (0, 4000)
    for relative, expected in hashes.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    result = {
        "status": "exhaustive-size-projection-pass",
        "cases": 65536,
        "source_hashes": hashes,
        "request64000": {"offset": 0, "paragraphs": 4000, "rounded_bytes": 64000},
        "limitations": freeze["limitations"],
        "original_only": "BP/SP/DS/SS; not host ABI equivalence.",
        "source_promoted": False,
        "artifact_hashes": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in tmp_path.iterdir()
            if p.is_file()
        },
    }
    (tmp_path / "result.json").write_text(json.dumps(result, indent=2) + "\n")
