from tools.asmcfg import (
    branch_target,
    build_blocks,
    is_branch,
    is_cond_branch,
    parse_ghidra_asm,
    resolve_branch_target,
)


def test_branch_target_resolves_direct_far_call():
    assert branch_target("CALLF 0XFFFF:BD66") == 0x10BD56


def test_branch_target_does_not_resolve_indirect_call():
    assert branch_target("CALLF [0X7838]") is None
    assert branch_target("CALLF [BX + 0X14]") is None
    assert branch_target("CALL BX") is None


def test_near_target_wraps_in_the_source_code_segment():
    instruction = "CALL 0X2000:FF06"

    assert resolve_branch_target(instruction, 0x1EC2) == 0x1FF06


def test_far_and_indirect_targets_are_not_reinterpreted_as_near():
    assert resolve_branch_target("CALLF 0X2000:FF06", 0x1EC2) == 0x2FF06
    assert resolve_branch_target("JMPF 0X2000:FF06", 0x1EC2) == 0x2FF06
    assert resolve_branch_target("CALL [BX]", 0x1EC2) is None


def test_e6_match_cfg_uses_wrapped_near_target():
    from tools.e6_match import cfg_from_ghidra_asm

    cfg = cfg_from_ghidra_asm(
        "1ec2:14cd  CALL 0X2000:FF06\n"
        "1ec2:14d0  MOV AX,0X1\n"
        "1ec2:12e6  RETF 0XC\n"
    )

    assert cfg["edges"] == 2


def test_cfg_uses_wrapped_near_target_to_create_branch_edge():
    parsed = parse_ghidra_asm(
        "1ec2:14cd  CALL 0X2000:FF06\n"
        "1ec2:12e6  RETF 0XC\n"
    )

    cfg = build_blocks(parsed["addrs"], parsed["insts"], parsed["segments"])

    assert cfg["nblocks"] == 2
    assert cfg["succ"][0] == {1}


def test_conditional_loop_mnemonics_are_recognized_without_prefix_matches():
    for mnemonic in ("LOOP", "LOOPE", "LOOPZ", "LOOPNE", "LOOPNZ"):
        instruction = f"{mnemonic} 0X1000:0100"
        assert is_branch(instruction)
        assert is_cond_branch(instruction)

    assert not is_branch("LOOPC 0X1000:0100")
    assert not is_cond_branch("LOOPC 0X1000:0100")
