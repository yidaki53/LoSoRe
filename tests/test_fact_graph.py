import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "engine"))

import fact_graph


def _graph():
    graph = fact_graph.FactGraph()
    graph.add_node(fact_graph.Node("caller-slot", "stack-slot", "game-a"))
    graph.add_node(fact_graph.Node("callee-param", "parameter", "game-a"))
    graph.add_edge(
        fact_graph.Edge(
            "argument-mapping",
            "caller-slot",
            "callee-param",
            "same_value",
            ("asm:caller:0x100",),
        )
    )
    graph.add_fact(
        fact_graph.Fact(
            "slot-width",
            "caller-slot",
            "width_bits",
            16,
            "observed",
            ("asm:caller:0x100",),
            producer="assembly-observation",
        )
    )
    return graph


def test_same_value_propagation_is_traceable_and_not_verified():
    graph = _graph()

    derived = graph.propagate_same_value()

    assert len(derived) == 1
    fact = derived[0]
    assert fact.subject == "callee-param"
    assert fact.predicate == "width_bits"
    assert fact.value == 16
    assert fact.status == "derived"
    assert fact.supports == ("slot-width",)
    assert fact.evidence_refs == ("asm:caller:0x100",)
    assert "oracle-verified" not in {fact.status}


def test_propagation_is_idempotent_and_does_not_overwrite_conflicts():
    graph = _graph()
    graph.add_fact(
        fact_graph.Fact(
            "param-width",
            "callee-param",
            "width_bits",
            32,
            "observed",
            ("asm:callee:0x200",),
            producer="assembly-observation",
        )
    )

    first = graph.propagate_same_value()
    second = graph.propagate_same_value()

    assert len(first) == 2
    assert second == []
    conflict = {
        frozenset(conflict.fact_ids)
        for conflict in graph.conflicts()
    }
    assert conflict == {
        frozenset(
            ("param-width", next(
                fact.id for fact in first if fact.subject == "callee-param"
            ))
        ),
        frozenset(
            ("slot-width", next(
                fact.id for fact in first if fact.subject == "caller-slot"
            ))
        ),
    }


def test_only_explicit_same_value_edges_propagate():
    graph = fact_graph.FactGraph()
    graph.add_node(fact_graph.Node("left", "register", "game-a"))
    graph.add_node(fact_graph.Node("right", "register", "game-a"))
    graph.add_fact(
        fact_graph.Fact(
            "left-value",
            "left",
            "value",
            7,
            "observed",
            ("asm:0x10",),
            producer="assembly-observation",
        )
    )

    assert graph.propagate_same_value() == []
    assert not graph.facts_for("right")


def test_transitive_propagation_records_only_the_supporting_path():
    graph = fact_graph.FactGraph()
    for node in ("first", "middle", "last", "unrelated"):
        graph.add_node(fact_graph.Node(node, "value", "game-a"))
    graph.add_edge(
        fact_graph.Edge("first-middle", "first", "middle", "same_value",
                        ("asm:0x10",))
    )
    graph.add_edge(
        fact_graph.Edge("middle-last", "middle", "last", "same_value",
                        ("asm:0x20",))
    )
    graph.add_fact(
        fact_graph.Fact(
            "first-width",
            "first",
            "width_bits",
            16,
            "observed",
            ("asm:0x01",),
            producer="assembly-observation",
        )
    )

    derived = graph.propagate_same_value()
    last_fact = next(fact for fact in derived if fact.subject == "last")

    assert last_fact.via_edges == ("first-middle", "middle-last")
    assert last_fact.evidence_refs == ("asm:0x01", "asm:0x10", "asm:0x20")
    assert {fact.subject for fact in derived} == {"middle", "last"}


def test_assembly_extraction_keeps_direct_and_unresolved_calls_distinct(tmp_path):
    leaf = tmp_path / "FUN_LEAF.s"
    caller = tmp_path / "FUN_CALLER.s"
    leaf.write_text(
        "; FUN_LEAF entry=0000:0100 size=1\n0000:0100  RET\n"
    )
    caller.write_text(
        "; FUN_CALLER entry=0000:0200 size=3\n"
        "0000:0200  CALLF 0x0000:0100\n"
        "0000:0205  CALLF 0x0000:0300\n"
        "0000:020a  CALL AX\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a",
        {"FUN_LEAF": leaf, "FUN_CALLER": caller},
    )

    relations = {edge.relation for edge in graph.edges.values()}
    assert "direct_call" in relations
    assert "unresolved_direct_target" in relations
    assert "unresolved_indirect_target" in relations
    direct_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate == "direct_target_flat_address"
    ]
    assert {fact.value for fact in direct_facts} == {0x100, 0x300}
    unknown_facts = [
        fact for fact in graph.facts.values() if fact.status == "unknown"
    ]
    assert len(unknown_facts) == 1
    assert unknown_facts[0].evidence_refs == ("asm:FUN_CALLER:0x20a",)


def test_assembly_extraction_resolves_wrapped_near_call_in_caller_segment(
    tmp_path,
):
    callee = tmp_path / "FUN_CALLEE.s"
    caller = tmp_path / "FUN_CALLER.s"
    callee.write_text(
        "; FUN_CALLEE entry=1ec2:12e6 size=1\n"
        "1ec2:12e6  RETF 0XC\n"
    )
    caller.write_text(
        "; FUN_CALLER entry=1ec2:14cd size=1\n"
        "1ec2:14cd  CALL 0X2000:FF06\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a",
        {"FUN_CALLEE": callee, "FUN_CALLER": caller},
    )

    call_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate == "direct_target_flat_address"
    ]
    assert [fact.value for fact in call_facts] == [0x1FF06]
    assert any(edge.relation == "direct_call" for edge in graph.edges.values())


def test_assembly_extraction_records_cfg_branch_and_fallthrough_evidence(tmp_path):
    routine = tmp_path / "FUN_BRANCH.s"
    routine.write_text(
        "; FUN_BRANCH entry=0000:0000 size=6\n"
        "0000:0000  CMP AX,0x0\n"
        "0000:0002  JZ 0x0000:0008\n"
        "0000:0004  INC AX\n"
        "0000:0006  JMP 0x0000:000a\n"
        "0000:0008  DEC AX\n"
        "0000:000a  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_BRANCH": routine}
    )

    blocks = sorted(
        (node for node in graph.nodes.values() if node.kind == "basic-block"),
        key=lambda node: node.attributes["start_address"],
    )
    assert len(blocks) == 4
    transitions = {
        (
            graph.nodes[edge.source].attributes["start_address"],
            graph.nodes[edge.target].attributes["start_address"],
            edge.relation,
        )
        for edge in graph.edges.values()
        if edge.relation in {"cfg_branch", "cfg_fallthrough"}
    }
    assert transitions == {
        (0, 8, "cfg_branch"),
        (0, 4, "cfg_fallthrough"),
        (4, 10, "cfg_branch"),
        (8, 10, "cfg_fallthrough"),
    }
    assert all(
        edge.evidence_refs
        for edge in graph.edges.values()
        if edge.relation in {"cfg_branch", "cfg_fallthrough"}
    )


def test_assembly_extraction_records_frame_operands_without_interpretation(
    tmp_path,
):
    routine = tmp_path / "FUN_FRAME.s"
    routine.write_text(
        "; FUN_FRAME entry=0000:0000 size=4\n"
        "0000:0000  MOV AL,byte ptr [BP + 0x4]\n"
        "0000:0002  MOV word ptr [BP + -0x2],AX\n"
        "0000:0005  XCHG word ptr [BP + 0xfed4],word ptr [BP + 0x6]\n"
        "0000:000a  MOV AX,word ptr [BP + SI]\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_FRAME": routine}
    )

    slots = {
        node.attributes["displacement_bytes"]: node
        for node in graph.nodes.values()
        if node.kind == "stack-slot"
    }
    assert set(slots) == {4, -2, -300, 6}
    accesses = [
        fact
        for fact in graph.facts.values()
        if fact.predicate == "frame_operand_observed"
    ]
    assert len(accesses) == 4
    assert all(fact.status == "observed" for fact in accesses)
    assert all(
        fact.producer == "assembly-frame-operand-extractor"
        for fact in accesses
    )
    assert not any(
        "direction" in fact.value or "parameter" in fact.value
        for fact in accesses
    )
    assert {
        (
            fact.value["address"],
            fact.value["displacement_bytes"],
            fact.evidence_refs[0],
        )
        for fact in accesses
    } == {
        (0, 4, "asm:FUN_FRAME:0x0:operand:1"),
        (2, -2, "asm:FUN_FRAME:0x2:operand:0"),
        (5, -300, "asm:FUN_FRAME:0x5:operand:0"),
        (5, 6, "asm:FUN_FRAME:0x5:operand:1"),
    }
    access_edges = [
        edge
        for edge in graph.edges.values()
        if edge.relation == "accesses_frame_slot"
    ]
    assert len(access_edges) == 4
    assert {edge.target for edge in access_edges} == {
        slot.id for slot in slots.values()
    }
    assert all(edge.source == "routine:game-a:FUN_FRAME" for edge in access_edges)


def test_frame_access_semantics_are_derived_only_for_supported_instructions(
    tmp_path,
):
    routine = tmp_path / "FUN_ACCESS.s"
    routine.write_text(
        "; FUN_ACCESS entry=0000:0000 size=5\n"
        "0000:0000  MOV AX,word ptr [BP + -0x2]\n"
        "0000:0003  MOV word ptr [BP + -0x2],AX\n"
        "0000:0006  ADD word ptr [BP + -0x2],0x1\n"
        "0000:000a  CMP word ptr [BP + -0x2],0x0\n"
        "0000:000e  LEA AX,[BP + -0x2]\n"
        "0000:0011  UNKNOWN word ptr [BP + -0x2]\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_ACCESS": routine}
    )

    access_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate == "frame_operand_access"
    ]
    assert {
        (
            fact.value["address"],
            fact.value["access"],
        )
        for fact in access_facts
    } == {
        (0, "read"),
        (3, "write"),
        (6, "read_write"),
        (10, "read"),
    }
    assert all(fact.status == "derived" for fact in access_facts)
    assert all(len(fact.supports) == len(fact.via_edges) == 1
               for fact in access_facts)
    assert all(fact.supports[0] in graph.facts for fact in access_facts)
    assert all(fact.via_edges[0] in graph.edges for fact in access_facts)
    assert not any(
        conflict.predicate in {
            "frame_operand_observed",
            "frame_operand_access",
        }
        for conflict in graph.conflicts()
    )


def test_direct_register_operand_effects_are_evidence_linked(tmp_path):
    routine = tmp_path / "FUN_REGISTERS.s"
    routine.write_text(
        "; FUN_REGISTERS entry=0000:0000 size=7\n"
        "0000:0000  MOV AX,BX\n"
        "0000:0002  ADD AX,CX\n"
        "0000:0004  CMP DX,AX\n"
        "0000:0006  PUSH SI\n"
        "0000:0007  POP DI\n"
        "0000:0008  LEA BX,[BP + SI]\n"
        "0000:000b  UNKNOWN CX\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REGISTERS": routine}
    )

    access_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate == "register_operand_access"
    ]
    assert {
        (
            fact.value["address"],
            fact.value["register"],
            fact.value["access"],
        )
        for fact in access_facts
    } == {
        (0, "AX", "write"),
        (0, "BX", "read"),
        (2, "AX", "read_write"),
        (2, "CX", "read"),
        (4, "DX", "read"),
        (4, "AX", "read"),
        (6, "SI", "read"),
        (7, "DI", "write"),
        (8, "BX", "write"),
    }
    assert all(fact.status == "derived" for fact in access_facts)
    observations = [
        fact for fact in graph.facts.values()
        if fact.predicate == "register_operand_observed"
    ]
    assert len(observations) == 10
    assert all(
        fact.evidence_refs[0].startswith("asm:FUN_REGISTERS:0x")
        for fact in observations
    )
    assert not any(
        fact.value["address"] == 11
        for fact in access_facts
    )
    assert not any(
        node.kind == "register-operand"
        and node.attributes["address"] == 8
        and node.attributes["register"] == "SI"
        for node in graph.nodes.values()
    )


def test_register_storage_aliases_are_exact_and_do_not_overlap_lanes(tmp_path):
    routine = tmp_path / "FUN_REGISTER_ALIASES.s"
    routine.write_text(
        "; FUN_REGISTER_ALIASES entry=0000:0000 size=3\n"
        "0000:0000  MOV AX,AL\n"
        "0000:0002  MOV AH,BL\n"
        "0000:0004  MOV SP,BP\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REGISTER_ALIASES": routine}
    )

    aliases = {
        frozenset(
            graph.nodes[node_id].attributes["register"]
            for node_id in (edge.source, edge.target)
        )
        for edge in graph.edges.values()
        if edge.relation == "overlaps_register_storage"
    }
    assert aliases == {
        frozenset(("AX", "AL")),
        frozenset(("AX", "AH")),
    }
    register_nodes = {
        node.attributes["register"]: node
        for node in graph.nodes.values()
        if node.kind == "register"
    }
    assert {
        name: (
            node.attributes["storage_family"],
            node.attributes["storage_bit_offset"],
            node.attributes["storage_width_bits"],
        )
        for name, node in register_nodes.items()
    } == {
        "AX": ("AX", 0, 16),
        "AL": ("AX", 0, 8),
        "AH": ("AX", 8, 8),
        "BL": ("BX", 0, 8),
        "SP": ("SP", 0, 16),
        "BP": ("BP", 0, 16),
    }
    assert all(
        edge.evidence_refs[0].startswith("isa:x86-16:")
        for edge in graph.edges.values()
        if edge.relation == "overlaps_register_storage"
    )
    assert graph.propagate_same_value() == []
    assert not any(
        conflict.predicate in {
            "register_operand_observed",
            "register_operand_access",
        }
        for conflict in graph.conflicts()
    )


def test_register_accesses_identify_the_affected_storage_lane(tmp_path):
    routine = tmp_path / "FUN_REGISTER_LANES.s"
    routine.write_text(
        "; FUN_REGISTER_LANES entry=0000:0000 size=2\n"
        "0000:0000  MOV AH,BL\n"
        "0000:0002  MOV AX,AL\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REGISTER_LANES": routine}
    )

    storage_accesses = [
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    ]
    assert {
        (
            fact.value["address"],
            fact.value["register"],
            fact.value["storage_family"],
            fact.value["start_bit"],
            fact.value["end_bit"],
            fact.value["access"],
        )
        for fact in storage_accesses
    } == {
        (0, "AH", "AX", 8, 16, "write"),
        (0, "BL", "BX", 0, 8, "read"),
        (2, "AX", "AX", 0, 16, "write"),
        (2, "AL", "AX", 0, 8, "read"),
    }
    assert all(fact.status == "derived" for fact in storage_accesses)
    assert all(fact.supports for fact in storage_accesses)
    assert all(fact.via_edges for fact in storage_accesses)
    assert graph.propagate_same_value() == []


def test_double_shift_reads_both_sources_and_updates_destination(tmp_path):
    routine = tmp_path / "FUN_DOUBLE_SHIFT.s"
    routine.write_text(
        "; FUN_DOUBLE_SHIFT entry=0000:0000 size=3\n"
        "0000:0000  SHRD AX,DX,CL\n"
        "0000:0003  SHLD word ptr [BP - 0x2],BX,CL\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_DOUBLE_SHIFT": routine}
    )

    register_accesses = {
        (
            fact.value["instruction"],
            fact.value["register"],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    }
    frame_accesses = {
        (
            fact.value["instruction"],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "frame_operand_access"
    }

    assert register_accesses == {
        ("SHRD AX,DX,CL", "AX", "read_write"),
        ("SHRD AX,DX,CL", "DX", "read"),
        ("SHRD AX,DX,CL", "CL", "read"),
        ("SHLD WORD PTR [BP - 0X2],BX,CL", "BX", "read"),
        ("SHLD WORD PTR [BP - 0X2],BX,CL", "CL", "read"),
    }
    assert frame_accesses == {
        ("SHLD WORD PTR [BP - 0X2],BX,CL", "read_write")
    }


def test_indirect_register_call_reads_only_its_explicit_target(tmp_path):
    routine = tmp_path / "FUN_REGISTER_CALL.s"
    routine.write_text(
        "; FUN_REGISTER_CALL entry=0000:0000 size=2\n"
        "0000:0000  CALL AX\n"
        "0000:0002  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REGISTER_CALL": routine}
    )

    accesses = [
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    ]

    assert len(accesses) == 1
    assert accesses[0].value["instruction"] == "CALL AX"
    assert accesses[0].value["register"] == "AX"
    assert accesses[0].value["access"] == "read"
    assert not accesses[0].value.get("implicit", False)


def test_three_operand_imul_reads_source_and_writes_destination(tmp_path):
    routine = tmp_path / "FUN_IMUL_THREE_OPERANDS.s"
    routine.write_text(
        "; FUN_IMUL_THREE_OPERANDS entry=0000:0000 size=3\n"
        "0000:0000  IMUL AX,BX,0x3f\n"
        "0000:0004  IMUL DI,WORD PTR [BP - 0x2],0x9\n"
        "0000:0009  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_IMUL_THREE_OPERANDS": routine}
    )

    register_accesses = {
        (
            fact.value["instruction"],
            fact.value["register"],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    }
    frame_accesses = {
        (
            fact.value["instruction"],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "frame_operand_access"
    }

    assert register_accesses == {
        ("IMUL AX,BX,0X3F", "AX", "write"),
        ("IMUL AX,BX,0X3F", "BX", "read"),
        ("IMUL DI,WORD PTR [BP - 0X2],0X9", "DI", "write"),
    }
    assert frame_accesses == {
        ("IMUL DI,WORD PTR [BP - 0X2],0X9", "read")
    }


def test_single_operand_multiply_and_divide_model_implicit_register_effects(
    tmp_path,
):
    routine = tmp_path / "FUN_IMPLICIT_ARITHMETIC.s"
    routine.write_text(
        "; FUN_IMPLICIT_ARITHMETIC entry=0000:0000 size=4\n"
        "0000:0000  MUL BL\n"
        "0000:0002  IMUL DX\n"
        "0000:0004  DIV CX\n"
        "0000:0006  IDIV CX\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_IMPLICIT_ARITHMETIC": routine}
    )

    accesses_by_instruction = {}
    for fact in graph.facts.values():
        if fact.predicate != "register_storage_access":
            continue
        access = fact.value
        accesses_by_instruction.setdefault(access["instruction"], set()).add(
            (access["register"], access["access"], access.get("implicit", False))
        )

    assert accesses_by_instruction == {
        "MUL BL": {
            ("BL", "read", False),
            ("AL", "read", True),
            ("AX", "write", True),
        },
        "IMUL DX": {
            ("DX", "read", False),
            ("AX", "read_write", True),
            ("DX", "write", True),
        },
        "DIV CX": {
            ("CX", "read", False),
            ("AX", "read_write", True),
            ("DX", "read_write", True),
        },
        "IDIV CX": {
            ("CX", "read", False),
            ("AX", "read_write", True),
            ("DX", "read_write", True),
        },
    }
    liveness = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_liveness"
    )
    live_in = {
        (item["family"], item["start_bit"], item["end_bit"])
        for item in liveness.value["blocks"][0]["live_in"]
    }
    assert live_in == {
        ("AX", 0, 8),
        ("BX", 0, 8),
        ("CX", 0, 16),
        ("DX", 0, 16),
    }
    implicit_facts = [
        fact for fact in graph.facts.values()
        if (
            fact.predicate == "register_storage_access"
            and fact.value.get("implicit")
        )
    ]
    assert all(fact.status == "derived" for fact in implicit_facts)
    assert all(fact.supports and fact.via_edges for fact in implicit_facts)
    assert all(
        any(reference.startswith("isa:x86-16:") for reference in fact.evidence_refs)
        for fact in implicit_facts
    )


def test_sixteen_bit_string_instructions_track_index_data_and_repeat_registers(
    tmp_path,
):
    routine = tmp_path / "FUN_STRING_EFFECTS.s"
    routine.write_text(
        "; FUN_STRING_EFFECTS entry=0000:0000 size=8\n"
        "0000:0000  MOVSB.REP ES:DI,SI\n"
        "0000:0002  LODSB SI\n"
        "0000:0004  STOSW ES:DI\n"
        "0000:0006  CMPSB.REPE ES:DI,SI\n"
        "0000:0008  SCASB.REPNE ES:DI\n"
        "0000:000a  OUTSB DX,SI\n"
        "0000:000c  MOVSD.REP ES:DI,SI\n"
        "0000:000e  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_STRING_EFFECTS": routine}
    )

    accesses_by_instruction = {}
    for fact in graph.facts.values():
        if (
            fact.predicate == "register_storage_access"
            and fact.value.get("implicit")
        ):
            access = fact.value
            accesses_by_instruction.setdefault(access["instruction"], set()).add(
                (access["register"], access["access"])
            )

    assert accesses_by_instruction == {
        "MOVSB.REP ES:DI,SI": {
            ("SI", "read_write"),
            ("DI", "read_write"),
            ("CX", "read_write"),
        },
        "LODSB SI": {("SI", "read_write"), ("AL", "write")},
        "STOSW ES:DI": {("DI", "read_write"), ("AX", "read")},
        "CMPSB.REPE ES:DI,SI": {
            ("SI", "read_write"),
            ("DI", "read_write"),
            ("CX", "read_write"),
        },
        "SCASB.REPNE ES:DI": {
            ("DI", "read_write"),
            ("AL", "read"),
            ("CX", "read_write"),
        },
        "OUTSB DX,SI": {("SI", "read_write"), ("DX", "read")},
        "MOVSD.REP ES:DI,SI": {
            ("SI", "read_write"),
            ("DI", "read_write"),
            ("CX", "read_write"),
        },
    }


def test_far_pointer_loads_read_frame_sources_and_write_destinations(tmp_path):
    routine = tmp_path / "FUN_FAR_POINTER_LOADS.s"
    routine.write_text(
        "; FUN_FAR_POINTER_LOADS entry=0000:0000 size=2\n"
        "0000:0000  LES DI,word ptr [BP + 0x4]\n"
        "0000:0004  LDS SI,word ptr [BP - 0x2]\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_FAR_POINTER_LOADS": routine}
    )

    register_accesses = {
        (
            fact.value["instruction"].split()[0],
            fact.value["register"],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    }
    frame_accesses = {
        (
            fact.value["instruction"].split()[0],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "frame_operand_access"
    }

    assert register_accesses == {
        ("LES", "DI", "write"),
        ("LDS", "SI", "write"),
    }
    assert frame_accesses == {("LES", "read"), ("LDS", "read")}


def test_port_io_models_explicit_register_effects_for_liveness(tmp_path):
    routine = tmp_path / "FUN_PORT_IO.s"
    routine.write_text(
        "; FUN_PORT_IO entry=0000:0000 size=4\n"
        "0000:0000  IN AL,DX\n"
        "0000:0002  AND AL,0x8\n"
        "0000:0004  OUT DX,AL\n"
        "0000:0006  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_PORT_IO": routine}
    )

    access_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    ]
    assert {
        (
            fact.value["instruction"].split()[0],
            fact.value["register"],
            fact.value["access"],
        )
        for fact in access_facts
    } == {
        ("IN", "AL", "write"),
        ("IN", "DX", "read"),
        ("AND", "AL", "read_write"),
        ("OUT", "DX", "read"),
        ("OUT", "AL", "read"),
    }

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_liveness"
    )
    live_in = {
        (item["family"], item["start_bit"], item["end_bit"])
        for item in analysis.value["blocks"][0]["live_in"]
    }
    assert live_in == {("DX", 0, 16)}


def test_frame_slot_use_and_definition_summaries_respect_instruction_order(
    tmp_path,
):
    routine = tmp_path / "FUN_FRAME_FLOW.s"
    routine.write_text(
        "; FUN_FRAME_FLOW entry=0000:0000 size=5\n"
        "0000:0000  MOV AX,word ptr [BP + -0x2]\n"
        "0000:0003  MOV word ptr [BP + -0x4],AX\n"
        "0000:0006  JZ 0x0000:000c\n"
        "0000:0009  MOV word ptr [BP + -0x2],AX\n"
        "0000:000c  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_FRAME_FLOW": routine}
    )

    def displacement_by_block(predicate):
        return {
            graph.nodes[fact.subject].attributes["start_address"]: {
                graph.nodes[slot_id].attributes["displacement_bytes"]
                for slot_id in fact.value["slots"]
            }
            for fact in graph.facts.values()
            if fact.predicate == predicate
        }

    assert displacement_by_block("frame_slots_used") == {0: {-2}}
    assert displacement_by_block("frame_slots_defined") == {
        0: {-4},
        9: {-2},
    }
    summary_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate in {"frame_slots_used", "frame_slots_defined"}
    ]
    assert all(fact.status == "derived" for fact in summary_facts)
    assert all(fact.supports and fact.via_edges for fact in summary_facts)
    assert all(
        all(support in graph.facts for support in fact.supports)
        for fact in summary_facts
    )


def test_frame_slot_liveness_flows_across_cfg_successors(tmp_path):
    routine = tmp_path / "FUN_LIVENESS.s"
    routine.write_text(
        "; FUN_LIVENESS entry=0000:0000 size=6\n"
        "0000:0000  MOV AX,word ptr [BP + -0x2]\n"
        "0000:0003  JZ 0x0000:000c\n"
        "0000:0006  MOV word ptr [BP + -0x2],AX\n"
        "0000:0009  JMP 0x0000:000f\n"
        "0000:000c  MOV AX,word ptr [BP + -0x4]\n"
        "0000:000f  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_LIVENESS": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "frame_slot_liveness"
    )
    blocks = analysis.value["blocks"]

    assert {
        graph.nodes[block["block"]].attributes["start_address"]: (
            {
                graph.nodes[slot].attributes["displacement_bytes"]
                for slot in block["live_in"]
            },
            {
                graph.nodes[slot].attributes["displacement_bytes"]
                for slot in block["live_out"]
            },
        )
        for block in blocks
    } == {
        0: ({-2, -4}, {-4}),
        6: (set(), set()),
        12: ({-4}, set()),
        15: (set(), set()),
    }
    assert analysis.status == "derived"
    assert analysis.supports and analysis.via_edges
    assert all(support in graph.facts for support in analysis.supports)
    assert all(edge in graph.edges for edge in analysis.via_edges)
    graph_path = tmp_path / "frame-liveness.json"
    graph.save(graph_path)
    assert fact_graph.FactGraph.load(graph_path).to_dict() == graph.to_dict()


def test_frame_slot_liveness_converges_through_a_cfg_loop(tmp_path):
    routine = tmp_path / "FUN_LIVENESS_LOOP.s"
    routine.write_text(
        "; FUN_LIVENESS_LOOP entry=0000:0000 size=6\n"
        "0000:0000  JZ 0x0000:0009\n"
        "0000:0003  MOV AX,word ptr [BP + -0x2]\n"
        "0000:0006  JMP 0x0000:0000\n"
        "0000:0009  MOV word ptr [BP + -0x4],AX\n"
        "0000:000c  MOV AX,word ptr [BP + -0x2]\n"
        "0000:000f  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_LIVENESS_LOOP": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "frame_slot_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            {
                graph.nodes[slot].attributes["displacement_bytes"]
                for slot in block["live_in"]
            },
            {
                graph.nodes[slot].attributes["displacement_bytes"]
                for slot in block["live_out"]
            },
        )
        for block in analysis.value["blocks"]
    }

    assert live_sets == {
        0: ({-2}, {-2}),
        3: ({-2}, {-2}),
        9: ({-2}, set()),
    }


def test_register_storage_liveness_respects_byte_lane_definitions(tmp_path):
    routine = tmp_path / "FUN_REGISTER_LIVENESS.s"
    routine.write_text(
        "; FUN_REGISTER_LIVENESS entry=0000:0000 size=6\n"
        "0000:0000  MOV AH,BL\n"
        "0000:0002  JZ 0x0000:000c\n"
        "0000:0004  MOV AX,CX\n"
        "0000:0006  JMP 0x0000:000c\n"
        "0000:000c  MOV DX,AH\n"
        "0000:000e  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REGISTER_LIVENESS": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            {
                (item["family"], item["start_bit"], item["end_bit"])
                for item in block["live_in"]
            },
            {
                (item["family"], item["start_bit"], item["end_bit"])
                for item in block["live_out"]
            },
        )
        for block in analysis.value["blocks"]
    }

    assert live_sets == {
        0: (
            {("BX", 0, 8), ("CX", 0, 16)},
            {("AX", 8, 16), ("CX", 0, 16)},
        ),
        4: ({("CX", 0, 16)}, {("AX", 8, 16)}),
        12: ({("AX", 8, 16)}, set()),
    }
    assert analysis.status == "derived"
    assert analysis.supports and analysis.via_edges
    assert all(support in graph.facts for support in analysis.supports)
    assert all(edge in graph.edges for edge in analysis.via_edges)


def test_register_storage_liveness_converges_through_a_cfg_loop(tmp_path):
    routine = tmp_path / "FUN_REGISTER_LIVENESS_LOOP.s"
    routine.write_text(
        "; FUN_REGISTER_LIVENESS_LOOP entry=0000:0000 size=6\n"
        "0000:0000  JZ 0x0000:0009\n"
        "0000:0003  MOV AX,BX\n"
        "0000:0005  JMP 0x0000:0000\n"
        "0000:0009  MOV DX,AX\n"
        "0000:000b  MOV SI,DX\n"
        "0000:000d  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REGISTER_LIVENESS_LOOP": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            {
                (item["family"], item["start_bit"], item["end_bit"])
                for item in block["live_in"]
            },
            {
                (item["family"], item["start_bit"], item["end_bit"])
                for item in block["live_out"]
            },
        )
        for block in analysis.value["blocks"]
    }

    assert live_sets == {
        0: (
            {("AX", 0, 16), ("BX", 0, 16)},
            {("AX", 0, 16), ("BX", 0, 16)},
        ),
        3: (
            {("BX", 0, 16)},
            {("AX", 0, 16), ("BX", 0, 16)},
        ),
        9: ({("AX", 0, 16)}, set()),
    }


def test_condition_flag_liveness_tracks_branch_reads_and_cmp_definitions(
    tmp_path,
):
    routine = tmp_path / "FUN_FLAG_LIVENESS.s"
    routine.write_text(
        "; FUN_FLAG_LIVENESS entry=0000:0000 size=5\n"
        "0000:0000  CMP AX,BX\n"
        "0000:0002  JMP 0x0000:0004\n"
        "0000:0004  JZ 0x0000:0008\n"
        "0000:0006  RET\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_FLAG_LIVENESS": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "condition_flag_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            set(block["live_in"]),
            set(block["live_out"]),
        )
        for block in analysis.value["blocks"]
    }

    assert live_sets == {
        0: (set(), {"ZF"}),
        4: ({"ZF"}, set()),
        6: (set(), set()),
        8: (set(), set()),
    }


def test_lahf_records_flag_to_ah_transfers_without_reading_overflow(
    tmp_path,
):
    routine = tmp_path / "FUN_LAHF.s"
    routine.write_text(
        "; FUN_LAHF entry=0000:0000 size=2\n"
        "0000:0000  LAHF\n"
        "0000:0002  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly("game-a", {"FUN_LAHF": routine})

    flag_accesses = {
        (fact.value["flag"], fact.value["access"])
        for fact in graph.facts.values()
        if fact.predicate == "condition_flag_access"
    }
    assert flag_accesses == {
        (flag, "read") for flag in ("CF", "PF", "AF", "ZF", "SF")
    }

    ah_access = next(
        fact for fact in graph.facts.values()
        if (
            fact.predicate == "register_storage_access"
            and fact.value["instruction"] == "LAHF"
        )
    )
    assert (
        ah_access.value["register"],
        ah_access.value["access"],
        ah_access.value["start_bit"],
        ah_access.value["end_bit"],
    ) == ("AH", "write", 8, 16)

    transfers = {
        (
            fact.value["flag"],
            fact.value["register"],
            fact.value["register_bit"],
            fact.value["direction"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "flag_register_transfer"
    }
    assert transfers == {
        (flag, "AH", bit, "flag_to_register")
        for flag, bit in (
            ("CF", 8),
            ("PF", 10),
            ("AF", 12),
            ("ZF", 14),
            ("SF", 15),
        )
    }


def test_sahf_records_ah_to_flag_transfers_and_preserves_overflow(tmp_path):
    routine = tmp_path / "FUN_SAHF.s"
    routine.write_text(
        "; FUN_SAHF entry=0000:0000 size=2\n"
        "0000:0000  SAHF\n"
        "0000:0002  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly("game-a", {"FUN_SAHF": routine})

    flag_accesses = {
        (fact.value["flag"], fact.value["access"])
        for fact in graph.facts.values()
        if fact.predicate == "condition_flag_access"
    }
    assert flag_accesses == {
        (flag, "write") for flag in ("CF", "PF", "AF", "ZF", "SF")
    }

    ah_access = next(
        fact for fact in graph.facts.values()
        if (
            fact.predicate == "register_storage_access"
            and fact.value["instruction"] == "SAHF"
        )
    )
    assert (
        ah_access.value["register"],
        ah_access.value["access"],
        ah_access.value["start_bit"],
        ah_access.value["end_bit"],
    ) == ("AH", "read", 8, 16)

    transfer_facts = [
        fact for fact in graph.facts.values()
        if fact.predicate == "flag_register_transfer"
    ]
    assert {
        (
            fact.value["flag"],
            fact.value["register"],
            fact.value["register_bit"],
            fact.value["direction"],
        )
        for fact in transfer_facts
    } == {
        (flag, "AH", bit, "register_to_flag")
        for flag, bit in (
            ("CF", 8),
            ("PF", 10),
            ("AF", 12),
            ("ZF", 14),
            ("SF", 15),
        )
    }
    instruction_listing = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "basic_block_instruction_listing"
    )
    assert all(
        fact.status == "derived"
        and fact.supports == (instruction_listing.id,)
        and fact.evidence_refs[0] == "asm:FUN_SAHF:0x0"
        for fact in transfer_facts
    )


def test_test_inc_and_adc_model_flag_clobbers_and_carry_use(tmp_path):
    routine = tmp_path / "FUN_FLAG_EFFECTS.s"
    routine.write_text(
        "; FUN_FLAG_EFFECTS entry=0000:0000 size=4\n"
        "0000:0000  TEST AX,AX\n"
        "0000:0002  INC BX\n"
        "0000:0004  ADC CX,DX\n"
        "0000:0006  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_FLAG_EFFECTS": routine}
    )

    flag_accesses = {
        (
            fact.value["instruction"],
            fact.value["flag"],
            fact.value["access"],
        )
        for fact in graph.facts.values()
        if fact.predicate == "condition_flag_access"
    }

    assert flag_accesses == {
        *{
            ("TEST AX,AX", flag, "write")
            for flag in ("CF", "OF", "PF", "SF", "ZF")
        },
        ("TEST AX,AX", "AF", "clobber"),
        *{
            ("INC BX", flag, "write")
            for flag in ("AF", "OF", "PF", "SF", "ZF")
        },
        ("ADC CX,DX", "CF", "read"),
        *{
            ("ADC CX,DX", flag, "write")
            for flag in ("AF", "CF", "OF", "PF", "SF", "ZF")
        },
    }


def test_unsigned_multiply_defines_carry_overflow_and_clobbers_other_flags(
    tmp_path,
):
    routine = tmp_path / "FUN_MULTIPLY_FLAGS.s"
    routine.write_text(
        "; FUN_MULTIPLY_FLAGS entry=0000:0000 size=4\n"
        "0000:0000  MUL BL\n"
        "0000:0002  IMUL AX,BX\n"
        "0000:0004  IMUL AX,BX,0x2\n"
        "0000:0006  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_MULTIPLY_FLAGS": routine}
    )

    expected_effects = {
        ("CF", "write"),
        ("OF", "write"),
        ("AF", "clobber"),
        ("PF", "clobber"),
        ("SF", "clobber"),
        ("ZF", "clobber"),
    }
    assert {
        instruction: {
            (fact.value["flag"], fact.value["access"])
            for fact in graph.facts.values()
            if (
                fact.predicate == "condition_flag_access"
                and fact.value["instruction"] == instruction
            )
        }
        for instruction in ("MUL BL", "IMUL AX,BX", "IMUL AX,BX,0X2")
    } == {
        "MUL BL": expected_effects,
        "IMUL AX,BX": expected_effects,
        "IMUL AX,BX,0X2": expected_effects,
    }


def test_division_leaves_all_status_flags_undefined(tmp_path):
    routine = tmp_path / "FUN_DIVISION_FLAGS.s"
    routine.write_text(
        "; FUN_DIVISION_FLAGS entry=0000:0000 size=3\n"
        "0000:0000  DIV BL\n"
        "0000:0002  IDIV word ptr [BX]\n"
        "0000:0004  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_DIVISION_FLAGS": routine}
    )

    effects_by_instruction = {
        instruction: {
            (fact.value["flag"], fact.value["access"])
            for fact in graph.facts.values()
            if (
                fact.predicate == "condition_flag_access"
                and fact.value["instruction"] == instruction
            )
        }
        for instruction in ("DIV BL", "IDIV WORD PTR [BX]")
    }
    all_clobbered = {
        (flag, "clobber")
        for flag in ("AF", "CF", "OF", "PF", "SF", "ZF")
    }
    assert effects_by_instruction == {
        "DIV BL": all_clobbered,
        "IDIV WORD PTR [BX]": all_clobbered,
    }


def test_unprefixed_string_comparison_defines_status_flags(tmp_path):
    routine = tmp_path / "FUN_STRING_COMPARE_FLAGS.s"
    routine.write_text(
        "; FUN_STRING_COMPARE_FLAGS entry=0000:0000 size=3\n"
        "0000:0000  CMPSB ES:DI,SI\n"
        "0000:0002  SCASW ES:DI\n"
        "0000:0004  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_STRING_COMPARE_FLAGS": routine}
    )

    expected = {(flag, "write") for flag in ("AF", "CF", "OF", "PF", "SF", "ZF")}
    effects_by_instruction = {
        instruction: {
            (fact.value["flag"], fact.value["access"])
            for fact in graph.facts.values()
            if (
                fact.predicate == "condition_flag_access"
                and fact.value["instruction"] == instruction
            )
        }
        for instruction in ("CMPSB ES:DI,SI", "SCASW ES:DI")
    }
    assert effects_by_instruction == {
        "CMPSB ES:DI,SI": expected,
        "SCASW ES:DI": expected,
    }


def test_repeated_string_comparison_preserves_flags_if_count_is_zero(
    tmp_path,
):
    routine = tmp_path / "FUN_REPEATED_STRING_COMPARE_FLAGS.s"
    routine.write_text(
        "; FUN_REPEATED_STRING_COMPARE_FLAGS entry=0000:0000 size=5\n"
        "0000:0000  CMPSB.REPE ES:DI,SI\n"
        "0000:0002  SCASB.REPNE ES:DI\n"
        "0000:0004  JZ 0x0000:0008\n"
        "0000:0006  RET\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_REPEATED_STRING_COMPARE_FLAGS": routine}
    )

    expected_repeated_effects = {
        (flag, "read_write")
        for flag in ("AF", "CF", "OF", "PF", "SF", "ZF")
    }
    assert {
        instruction: {
            (fact.value["flag"], fact.value["access"])
            for fact in graph.facts.values()
            if (
                fact.predicate == "condition_flag_access"
                and fact.value["instruction"] == instruction
            )
        }
        for instruction in ("CMPSB.REPE ES:DI,SI", "SCASB.REPNE ES:DI")
    } == {
        "CMPSB.REPE ES:DI,SI": expected_repeated_effects,
        "SCASB.REPNE ES:DI": expected_repeated_effects,
    }

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "condition_flag_liveness"
    )
    first_block = next(
        block for block in analysis.value["blocks"]
        if graph.nodes[block["block"]].attributes["start_address"] == 0
    )
    assert set(first_block["live_in"]) == {
        "AF", "CF", "OF", "PF", "SF", "ZF"
    }


def test_undefined_multiply_flag_does_not_flow_from_prior_comparison(
    tmp_path,
):
    routine = tmp_path / "FUN_MULTIPLY_FLAG_LIVENESS.s"
    routine.write_text(
        "; FUN_MULTIPLY_FLAG_LIVENESS entry=0000:0000 size=5\n"
        "0000:0000  CMP AX,BX\n"
        "0000:0002  MUL CL\n"
        "0000:0004  JZ 0x0000:0008\n"
        "0000:0006  RET\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_MULTIPLY_FLAG_LIVENESS": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "condition_flag_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            set(block["live_in"]),
            set(block["live_out"]),
        )
        for block in analysis.value["blocks"]
    }
    assert live_sets == {
        0: (set(), set()),
        6: (set(), set()),
        8: (set(), set()),
    }


def test_shift_by_one_models_defined_and_undefined_flags(tmp_path):
    routine = tmp_path / "FUN_SHIFT_FLAGS.s"
    routine.write_text(
        "; FUN_SHIFT_FLAGS entry=0000:0000 size=2\n"
        "0000:0000  SHL AX,0x1\n"
        "0000:0002  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_SHIFT_FLAGS": routine}
    )

    effects = {
        (fact.value["flag"], fact.value["access"])
        for fact in graph.facts.values()
        if (
            fact.predicate == "condition_flag_access"
            and fact.value["instruction"] == "SHL AX,0X1"
        )
    }
    assert effects == {
        ("CF", "write"),
        ("PF", "write"),
        ("SF", "write"),
        ("ZF", "write"),
        ("AF", "clobber"),
        ("OF", "write"),
    }


def test_variable_shift_count_preserves_flag_liveness_when_count_is_zero(
    tmp_path,
):
    routine = tmp_path / "FUN_VARIABLE_SHIFT_FLAGS.s"
    routine.write_text(
        "; FUN_VARIABLE_SHIFT_FLAGS entry=0000:0000 size=4\n"
        "0000:0000  SHL AX,CL\n"
        "0000:0002  JZ 0x0000:0008\n"
        "0000:0004  RET\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_VARIABLE_SHIFT_FLAGS": routine}
    )

    accesses = {
        (fact.value["flag"], fact.value["access"])
        for fact in graph.facts.values()
        if (
            fact.predicate == "condition_flag_access"
            and fact.value["instruction"] == "SHL AX,CL"
        )
    }
    assert accesses == {
        (flag, "read_write")
        for flag in ("AF", "CF", "OF", "PF", "SF", "ZF")
    }

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "condition_flag_liveness"
    )
    first_block = next(
        block for block in analysis.value["blocks"]
        if graph.nodes[block["block"]].attributes["start_address"] == 0
    )
    assert set(first_block["live_in"]) == {
        "AF", "CF", "OF", "PF", "SF", "ZF"
    }


def test_zero_shift_preserves_flags_and_multi_bit_shift_clobbers_overflow(
    tmp_path,
):
    routine = tmp_path / "FUN_SHIFT_COUNTS.s"
    routine.write_text(
        "; FUN_SHIFT_COUNTS entry=0000:0000 size=3\n"
        "0000:0000  SHL AX,0x0\n"
        "0000:0002  SHR BX,0x2\n"
        "0000:0004  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_SHIFT_COUNTS": routine}
    )

    effects_by_instruction = {
        instruction: {
            (fact.value["flag"], fact.value["access"])
            for fact in graph.facts.values()
            if (
                fact.predicate == "condition_flag_access"
                and fact.value["instruction"] == instruction
            )
        }
        for instruction in ("SHL AX,0X0", "SHR BX,0X2")
    }
    assert effects_by_instruction == {
        "SHL AX,0X0": set(),
        "SHR BX,0X2": {
            ("CF", "write"),
            ("PF", "write"),
            ("SF", "write"),
            ("ZF", "write"),
            ("AF", "clobber"),
            ("OF", "clobber"),
        },
    }


def test_rotate_through_carry_reads_and_writes_carry(tmp_path):
    routine = tmp_path / "FUN_ROTATE_CARRY_FLAGS.s"
    routine.write_text(
        "; FUN_ROTATE_CARRY_FLAGS entry=0000:0000 size=2\n"
        "0000:0000  RCL AX,0x1\n"
        "0000:0002  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_ROTATE_CARRY_FLAGS": routine}
    )

    effects = {
        (fact.value["flag"], fact.value["access"])
        for fact in graph.facts.values()
        if fact.predicate == "condition_flag_access"
    }
    assert effects == {("CF", "read_write"), ("OF", "write")}


def test_condition_flag_liveness_converges_through_an_adc_loop(tmp_path):
    routine = tmp_path / "FUN_FLAG_LOOP.s"
    routine.write_text(
        "; FUN_FLAG_LOOP entry=0000:0000 size=4\n"
        "0000:0000  ADC AX,BX\n"
        "0000:0002  JC 0x0000:0000\n"
        "0000:0004  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_FLAG_LOOP": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "condition_flag_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            set(block["live_in"]),
            set(block["live_out"]),
        )
        for block in analysis.value["blocks"]
    }

    assert live_sets == {
        0: ({"CF"}, {"CF"}),
        4: (set(), set()),
    }


def test_jcxz_and_loop_contribute_implicit_cx_liveness(tmp_path):
    routine = tmp_path / "FUN_CX_CONTROL_FLOW.s"
    routine.write_text(
        "; FUN_CX_CONTROL_FLOW entry=0000:0000 size=5\n"
        "0000:0000  JCXZ 0x0000:0008\n"
        "0000:0002  LOOP 0x0000:0002\n"
        "0000:0004  RET\n"
        "0000:0008  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_CX_CONTROL_FLOW": routine}
    )

    accesses = {
        (
            fact.value["instruction"],
            fact.value["register"],
            fact.value["access"],
            fact.value.get("implicit", False),
        )
        for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    }
    assert accesses == {
        ("JCXZ 0X0000:0008", "CX", "read", True),
        ("LOOP 0X0000:0002", "CX", "read_write", True),
    }

    analysis = next(
        fact for fact in graph.facts.values()
        if (
            fact.predicate == "register_storage_liveness"
            and fact.subject == "routine:game-a:FUN_CX_CONTROL_FLOW"
        )
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            {
                (item["family"], item["start_bit"], item["end_bit"])
                for item in block["live_in"]
            },
            {
                (item["family"], item["start_bit"], item["end_bit"])
                for item in block["live_out"]
            },
        )
        for block in analysis.value["blocks"]
    }
    assert live_sets == {
        0: ({("CX", 0, 16)}, {("CX", 0, 16)}),
        2: ({("CX", 0, 16)}, {("CX", 0, 16)}),
        4: (set(), set()),
        8: (set(), set()),
    }


def test_jecxz_reads_the_full_ecx_register(tmp_path):
    routine = tmp_path / "FUN_JECXZ.s"
    routine.write_text(
        "; FUN_JECXZ entry=0000:0000 size=3\n"
        "0000:0000  JECXZ 0x0000:0004\n"
        "0000:0002  RET\n"
        "0000:0004  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly("game-a", {"FUN_JECXZ": routine})

    access = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
    )
    assert access.value == {
        "address": 0,
        "instruction": "JECXZ 0X0000:0004",
        "operand_index": None,
        "register": "ECX",
        "storage_family": "CX",
        "start_bit": 0,
        "end_bit": 32,
        "access": "read",
        "implicit": True,
    }
    liveness = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_liveness"
    )
    first_block = next(
        block for block in liveness.value["blocks"]
        if graph.nodes[block["block"]].attributes["start_address"] == 0
    )
    assert first_block["live_in"] == [
        {"family": "CX", "start_bit": 0, "end_bit": 32}
    ]
    assert not any(
        fact.predicate == "condition_flag_access"
        for fact in graph.facts.values()
    )


def test_conditional_loop_forms_read_zf_and_update_cx(tmp_path):
    routine = tmp_path / "FUN_CONDITIONAL_LOOPS.s"
    routine.write_text(
        "; FUN_CONDITIONAL_LOOPS entry=0000:0000 size=5\n"
        "0000:0000  LOOPE 0x0000:0000\n"
        "0000:0002  LOOPZ 0x0000:0002\n"
        "0000:0004  LOOPNE 0x0000:0004\n"
        "0000:0006  LOOPNZ 0x0000:0006\n"
        "0000:0008  LOOP 0x0000:0008\n"
        "0000:000a  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_CONDITIONAL_LOOPS": routine}
    )

    expected_instructions = {
        "LOOPE 0X0000:0000",
        "LOOPZ 0X0000:0002",
        "LOOPNE 0X0000:0004",
        "LOOPNZ 0X0000:0006",
        "LOOP 0X0000:0008",
    }
    counter_accesses = {
        fact.value["instruction"]: fact.value["access"]
        for fact in graph.facts.values()
        if fact.predicate == "register_storage_access"
        and fact.value.get("implicit")
    }
    assert counter_accesses == {
        instruction: "read_write" for instruction in expected_instructions
    }

    flag_reads = {
        fact.value["instruction"]
        for fact in graph.facts.values()
        if fact.predicate == "condition_flag_access"
        and fact.value["flag"] == "ZF"
        and fact.value["access"] == "read"
    }
    assert flag_reads == expected_instructions - {"LOOP 0X0000:0008"}

    flag_liveness = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "condition_flag_liveness"
    )
    live_sets = {
        graph.nodes[block["block"]].attributes["start_address"]: (
            set(block["live_in"]),
            set(block["live_out"]),
        )
        for block in flag_liveness.value["blocks"]
    }
    assert live_sets == {
        0: ({"ZF"}, {"ZF"}),
        2: ({"ZF"}, {"ZF"}),
        4: ({"ZF"}, {"ZF"}),
        6: ({"ZF"}, {"ZF"}),
        8: (set(), set()),
        10: (set(), set()),
    }

    branch_edges = [
        edge for edge in graph.edges.values() if edge.relation == "cfg_branch"
    ]
    assert {
        graph.nodes[edge.source].attributes["start_address"]
        for edge in branch_edges
    } == {0, 2, 4, 6, 8}


def test_byte_register_definition_does_not_kill_the_other_byte_lane(tmp_path):
    routine = tmp_path / "FUN_BYTE_REGISTER_LIVENESS.s"
    routine.write_text(
        "; FUN_BYTE_REGISTER_LIVENESS entry=0000:0000 size=3\n"
        "0000:0000  MOV AL,BL\n"
        "0000:0002  MOV DL,AH\n"
        "0000:0004  RET\n"
    )

    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_BYTE_REGISTER_LIVENESS": routine}
    )

    analysis = next(
        fact for fact in graph.facts.values()
        if fact.predicate == "register_storage_liveness"
    )
    entry_live = {
        (item["family"], item["start_bit"], item["end_bit"])
        for item in analysis.value["blocks"][0]["live_in"]
    }

    assert entry_live == {
        ("AX", 8, 16),
        ("BX", 0, 8),
    }


def test_unresolved_call_report_explains_direct_and_indirect_targets(tmp_path):
    caller = tmp_path / "FUN_CALLER.s"
    caller.write_text(
        "; FUN_CALLER entry=0000:0200 size=3\n"
        "0000:0200  CALLF 0x0000:0300\n"
        "0000:0205  CALL AX\n"
    )
    graph = fact_graph.FactGraph.from_assembly(
        "game-a", {"FUN_CALLER": caller}
    )

    report = graph.unresolved_call_targets()

    assert report == [
        {
            "caller": "FUN_CALLER",
            "call_site": "call:game-a:FUN_CALLER:00200",
            "address": 512,
            "instruction": "CALLF 0X0000:0300",
            "resolution": "direct-unresolved",
            "target_address": 768,
            "candidate_routines": [],
            "evidence_refs": ["asm:FUN_CALLER:0x200"],
        },
        {
            "caller": "FUN_CALLER",
            "call_site": "call:game-a:FUN_CALLER:00205",
            "address": 517,
            "instruction": "CALL AX",
            "resolution": "indirect",
            "target_address": None,
            "candidate_routines": [],
            "evidence_refs": ["asm:FUN_CALLER:0x205"],
        },
    ]


def test_graph_round_trip_is_versioned_and_preserves_provenance(tmp_path):
    graph = _graph()
    graph.propagate_same_value()
    path = tmp_path / "facts.json"

    graph.save(path)
    loaded = fact_graph.FactGraph.load(path)

    assert loaded.to_dict() == graph.to_dict()
    payload = json.loads(path.read_text())
    assert payload["schema_version"] == fact_graph.SCHEMA_VERSION
    assert payload["facts"]["slot-width"]["producer"] == "assembly-observation"


def test_invalid_or_unverifiable_graphs_fail_loudly(tmp_path):
    graph = fact_graph.FactGraph()
    graph.add_node(fact_graph.Node("source", "register", "game-a"))
    with pytest.raises(ValueError, match="evidence"):
        graph.add_fact(
            fact_graph.Fact(
                "unsupported",
                "source",
                "width_bits",
                16,
                "observed",
                producer="assembly-observation",
            )
        )

    path = tmp_path / "bad.json"
    path.write_text('{"schema_version": 999}')
    with pytest.raises(ValueError, match="schema"):
        fact_graph.FactGraph.load(path)

    path.write_text('{"schema_version": 1, "nodes": [], "edges": {}, "facts": {}}')
    with pytest.raises(ValueError, match="nodes"):
        fact_graph.FactGraph.load(path)
