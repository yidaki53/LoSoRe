"""Evidence-backed graph for partial binary-analysis facts.

Derived facts remain explicitly non-oracular. This module does not attest
source recovery or change the recovery scheduler.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import pathlib
import re
import tempfile
from collections import defaultdict, deque
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from typing import Any

from tools.asmcfg import (
    build_blocks,
    is_branch,
    is_call,
    is_cond_branch,
    is_ret,
    parse_ghidra_asm,
    resolve_branch_target,
)

SCHEMA_VERSION = 1
_FACT_STATUSES = {
    "observed",
    "oracle-verified",
    "hypothesis",
    "derived",
    "contradicted",
    "unknown",
}
_EDGE_STATUSES = {"observed", "oracle-verified"}
_GROUNDED_STATUSES = {"observed", "oracle-verified"}
_FRAME_SLOT_OPERAND = re.compile(
    r"\[BP(?:\s*([+-])\s*(-?(?:0X[0-9A-F]+|\d+)))?\]"
)
_FRAME_SLOT_READ_ONLY = {"CMP", "TEST"}
_FRAME_SLOT_READ_MODIFY_WRITE = {
    "ADC",
    "ADD",
    "AND",
    "DEC",
    "INC",
    "NEG",
    "NOT",
    "OR",
    "RCL",
    "RCR",
    "ROL",
    "ROR",
    "SAR",
    "SBB",
    "SHL",
    "SHR",
    "SUB",
    "XOR",
}
_DIRECT_REGISTER_OPERAND = re.compile(
    r"(?:(?:BYTE|WORD) PTR\s+)?"
    r"(ECX|AX|BX|CX|DX|SP|BP|SI|DI|AL|AH|BL|BH|CL|CH|DL|DH|CS|DS|ES|SS)"
)
_REGISTER_STORAGE = {
    "AX": ("AX", 0, 16),
    "AL": ("AX", 0, 8),
    "AH": ("AX", 8, 8),
    "BX": ("BX", 0, 16),
    "BL": ("BX", 0, 8),
    "BH": ("BX", 8, 8),
    "CX": ("CX", 0, 16),
    "ECX": ("CX", 0, 32),
    "CL": ("CX", 0, 8),
    "CH": ("CX", 8, 8),
    "DX": ("DX", 0, 16),
    "DL": ("DX", 0, 8),
    "DH": ("DX", 8, 8),
    "SP": ("SP", 0, 16),
    "BP": ("BP", 0, 16),
    "SI": ("SI", 0, 16),
    "DI": ("DI", 0, 16),
    "CS": ("CS", 0, 16),
    "DS": ("DS", 0, 16),
    "ES": ("ES", 0, 16),
    "SS": ("SS", 0, 16),
}
_STATUS_FLAGS = ("AF", "CF", "OF", "PF", "SF", "ZF")
_LAHF_SAHF_BITS = (
    ("CF", 8),
    ("PF", 10),
    ("AF", 12),
    ("ZF", 14),
    ("SF", 15),
)
_LOOP_MNEMONICS = {"LOOP", "LOOPE", "LOOPZ", "LOOPNE", "LOOPNZ"}
_CONDITION_FLAG_READS = {
    "JA": ("CF", "ZF"),
    "JAE": ("CF",),
    "JB": ("CF",),
    "JBE": ("CF", "ZF"),
    "JC": ("CF",),
    "JNA": ("CF", "ZF"),
    "JNAE": ("CF",),
    "JNB": ("CF",),
    "JNBE": ("CF", "ZF"),
    "JNC": ("CF",),
    "JNE": ("ZF",),
    "JNG": ("ZF", "SF", "OF"),
    "JNGE": ("SF", "OF"),
    "JNL": ("SF", "OF"),
    "JNLE": ("ZF", "SF", "OF"),
    "JNO": ("OF",),
    "JNP": ("PF",),
    "JNS": ("SF",),
    "JNZ": ("ZF",),
    "JO": ("OF",),
    "JP": ("PF",),
    "JPE": ("PF",),
    "JPO": ("PF",),
    "JS": ("SF",),
    "JZ": ("ZF",),
    "JG": ("ZF", "SF", "OF"),
    "JGE": ("SF", "OF"),
    "JL": ("SF", "OF"),
    "JLE": ("ZF", "SF", "OF"),
    "JE": ("ZF",),
    "LOOPE": ("ZF",),
    "LOOPZ": ("ZF",),
    "LOOPNE": ("ZF",),
    "LOOPNZ": ("ZF",),
}
_ALL_STATUS_FLAG_WRITES = {"CMP", "ADD", "ADC", "SUB", "SBB", "NEG"}
_LOGICAL_STATUS_FLAG_WRITES = {"TEST", "AND", "OR", "XOR"}
_PARTIAL_STATUS_FLAG_WRITES = {"INC", "DEC"}


@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    target: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    relation: str
    evidence_refs: tuple[str, ...]
    status: str = "observed"


@dataclass(frozen=True)
class Fact:
    id: str
    subject: str
    predicate: str
    value: Any
    status: str
    evidence_refs: tuple[str, ...] = ()
    producer: str = ""
    supports: tuple[str, ...] = ()
    via_edges: tuple[str, ...] = ()
    assembly_sha256: str | None = None
    binary_sha256: str | None = None
    confidence: float | None = None


@dataclass(frozen=True)
class Conflict:
    subject: str
    predicate: str
    fact_ids: tuple[str, ...]
    values: tuple[Any, ...]


class FactGraph:
    """Validated, serializable facts and evidence-linked graph relations."""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, Edge] = {}
        self.facts: dict[str, Fact] = {}

    def add_node(self, node: Node) -> None:
        _require_text(node.id, "node id")
        _require_text(node.kind, "node kind")
        _require_text(node.target, "node target")
        if not isinstance(node.attributes, dict):
            raise TypeError("node attributes must be a JSON object")
        _require_json_value(node.attributes, "node attributes")
        self._add_unique(self.nodes, node.id, node, "node")

    def add_edge(self, edge: Edge) -> None:
        _require_text(edge.id, "edge id")
        _require_text(edge.relation, "edge relation")
        _require_text(edge.status, "edge status")
        self._require_node(edge.source)
        self._require_node(edge.target)
        self._require_evidence(edge.evidence_refs, "edge evidence")
        if edge.status not in _EDGE_STATUSES:
            raise ValueError(f"unsupported edge status: {edge.status}")
        self._add_unique(self.edges, edge.id, edge, "edge")

    def add_fact(self, fact: Fact) -> None:
        _require_text(fact.id, "fact id")
        _require_text(fact.predicate, "fact predicate")
        _require_text(fact.status, "fact status")
        _require_text(fact.producer, "fact producer")
        self._require_node(fact.subject)
        _require_json_value(fact.value, "fact value")
        if fact.status not in _FACT_STATUSES:
            raise ValueError(f"unsupported fact status: {fact.status}")
        if fact.status in _GROUNDED_STATUSES | {"contradicted"}:
            self._require_evidence(fact.evidence_refs, "fact evidence")
        elif fact.evidence_refs:
            self._validate_ref_values(fact.evidence_refs, "fact evidence")
        self._validate_ref_values(fact.supports, "fact supports", allow_empty=True)
        self._validate_ref_values(fact.via_edges, "fact edge references", allow_empty=True)
        if fact.status == "derived":
            if not fact.supports or not fact.via_edges:
                raise ValueError("derived facts require supporting facts and edges")
            missing_facts = set(fact.supports) - self.facts.keys()
            missing_edges = set(fact.via_edges) - self.edges.keys()
            if missing_facts or missing_edges:
                raise ValueError(
                    f"derived fact references missing inputs: "
                    f"facts={sorted(missing_facts)}, edges={sorted(missing_edges)}"
                )
        elif fact.supports or fact.via_edges:
            raise ValueError("only derived facts may reference supporting graph records")
        if fact.confidence is not None and (
            isinstance(fact.confidence, bool)
            or not isinstance(fact.confidence, (int, float))
            or not math.isfinite(fact.confidence)
            or not 0.0 <= fact.confidence <= 1.0
        ):
            raise ValueError("fact confidence must be between 0 and 1")
        for digest_name in ("assembly_sha256", "binary_sha256"):
            digest = getattr(fact, digest_name)
            if digest is not None and (
                not isinstance(digest, str) or not _is_sha256(digest)
            ):
                raise ValueError(f"{digest_name} must be a SHA-256 hex digest")
        self._add_unique(self.facts, fact.id, fact, "fact")

    def facts_for(self, subject: str, predicate: str | None = None) -> list[Fact]:
        return sorted(
            (
                fact for fact in self.facts.values()
                if fact.subject == subject
                and (predicate is None or fact.predicate == predicate)
            ),
            key=lambda fact: fact.id,
        )

    def propagate_same_value(self) -> list[Fact]:
        """Copy grounded facts over explicitly evidenced symmetric value edges."""
        adjacency = self._same_value_adjacency()
        source_facts = sorted(
            (fact for fact in self.facts.values()
             if fact.status in _GROUNDED_STATUSES),
            key=lambda fact: fact.id,
        )
        derived: list[Fact] = []
        for source_fact in source_facts:
            for subject, edge_path in self._same_value_paths(
                source_fact.subject, adjacency
            ).items():
                if self._has_same_value_fact(
                    subject, source_fact.predicate, source_fact.value
                ):
                    continue
                fact = self._derived_fact(source_fact, subject, edge_path)
                if fact.id not in self.facts:
                    self.add_fact(fact)
                    derived.append(fact)
        return derived

    def conflicts(self) -> list[Conflict]:
        grouped: dict[tuple[str, str], list[Fact]] = defaultdict(list)
        for fact in self.facts.values():
            if fact.status in {"observed", "oracle-verified", "derived"}:
                grouped[(fact.subject, fact.predicate)].append(fact)

        conflicts = []
        for (subject, predicate), facts in sorted(grouped.items()):
            values_by_key: dict[str, list[Fact]] = defaultdict(list)
            for fact in facts:
                values_by_key[_canonical_json(fact.value)].append(fact)
            if len(values_by_key) < 2:
                continue
            conflicts.append(
                Conflict(
                    subject,
                    predicate,
                    tuple(sorted(fact.id for fact in facts)),
                    tuple(
                        values_by_key[key][0].value
                        for key in sorted(values_by_key)
                    ),
                )
            )
        return conflicts

    def unresolved_call_targets(self) -> list[dict[str, Any]]:
        """Explain direct unmatched and indirect call targets without judging them."""
        report = []
        for edge in self.edges.values():
            if edge.relation not in {
                "unresolved_direct_target",
                "unresolved_indirect_target",
            }:
                continue
            call_site = self.nodes[edge.source]
            unresolved = self.nodes[edge.target]
            report.append(
                {
                    "caller": call_site.attributes["caller"],
                    "call_site": call_site.id,
                    "address": call_site.attributes["address"],
                    "instruction": call_site.attributes["instruction"],
                    "resolution": (
                        "direct-unresolved"
                        if edge.relation == "unresolved_direct_target"
                        else "indirect"
                    ),
                    "target_address": unresolved.attributes.get("flat_address"),
                    "candidate_routines": unresolved.attributes.get(
                        "candidate_routines", []
                    ),
                    "evidence_refs": list(edge.evidence_refs),
                }
            )
        return sorted(
            report,
            key=lambda item: (item["caller"], item["address"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "nodes": {
                key: _record_to_dict(record)
                for key, record in sorted(self.nodes.items())
            },
            "edges": {
                key: _record_to_dict(record)
                for key, record in sorted(self.edges.items())
            },
            "facts": {
                key: _record_to_dict(record)
                for key, record in sorted(self.facts.items())
            },
        }

    def save(self, path: pathlib.Path) -> None:
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(
            self.to_dict(), indent=2, sort_keys=True, allow_nan=False
        ) + "\n"
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as output:
                output.write(content)
                output.flush()
                os.fsync(output.fileno())
            pathlib.Path(temporary_name).replace(path)
        except Exception:
            pathlib.Path(temporary_name).unlink(missing_ok=True)
            raise

    @classmethod
    def load(cls, path: pathlib.Path) -> FactGraph:
        path = pathlib.Path(path)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot load fact graph at {path}: {exc}") from exc
        if (
            not isinstance(payload, dict)
            or payload.get("schema_version") != SCHEMA_VERSION
        ):
            raise ValueError(
                f"unsupported fact graph schema in {path}; "
                f"expected {SCHEMA_VERSION}"
            )
        graph = cls()
        try:
            for node in _record_collection(payload, "nodes"):
                graph.add_node(Node(**node))
            for edge in _record_collection(payload, "edges"):
                edge["evidence_refs"] = _sequence_field(
                    edge, "evidence_refs", required=True
                )
                graph.add_edge(Edge(**edge))
            pending_facts = _record_collection(payload, "facts")
            while pending_facts:
                ready_facts = []
                waiting_facts = []
                for fact in pending_facts:
                    supports = fact.get("supports", ())
                    if set(supports) <= graph.facts.keys():
                        ready_facts.append(fact)
                    else:
                        waiting_facts.append(fact)
                if not ready_facts:
                    raise ValueError("fact support references are missing or cyclic")
                for fact in ready_facts:
                    for field_name in ("evidence_refs", "supports", "via_edges"):
                        fact[field_name] = _sequence_field(fact, field_name)
                    graph.add_fact(Fact(**fact))
                pending_facts = waiting_facts
            graph._validate_references()
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid fact graph at {path}: {exc}") from exc
        return graph

    @classmethod
    def from_assembly(
        cls,
        target: str,
        assembly_paths: Mapping[str, pathlib.Path],
        entries: Mapping[str, str] | None = None,
        binary_sha256: str | None = None,
    ) -> FactGraph:
        """Extract routines and direct/indirect call observations from listings."""
        _require_text(target, "target")
        if binary_sha256 is not None and not _is_sha256(binary_sha256):
            raise ValueError("binary_sha256 must be a SHA-256 hex digest")
        entries = entries or {}
        graph = cls()
        routine_ids = {
            name: f"routine:{target}:{name}" for name in assembly_paths
        }
        source_by_name: dict[str, tuple[pathlib.Path, str, str]] = {}
        address_to_routines: dict[int, list[str]] = defaultdict(list)

        for name, path in sorted(assembly_paths.items()):
            _require_text(name, "routine name")
            path = pathlib.Path(path)
            raw_assembly = path.read_bytes()
            assembly = raw_assembly.decode("utf-8", errors="replace")
            assembly_hash = hashlib.sha256(raw_assembly).hexdigest()
            entry = _parse_real_mode_address(entries.get(name))
            entry_source = "metadata"
            if entry is None:
                entry = _parse_entry_header(name, assembly)
                entry_source = "assembly"
            node_id = routine_ids[name]
            graph.add_node(
                Node(
                    node_id,
                    "routine",
                    target,
                    {
                        "name": name,
                        "assembly_path": str(path),
                        "assembly_sha256": assembly_hash,
                        "entry_flat_address": entry,
                    },
                )
            )
            source_by_name[name] = (path, assembly, assembly_hash)
            if entry is not None:
                address_to_routines[entry].append(node_id)
                evidence_ref = (
                    f"metadata:functions.json#{name}.entry"
                    if entry_source == "metadata"
                    else f"asm:{name}:entry"
                )
                graph.add_fact(
                    Fact(
                        id=_stable_id(
                            "entry", target, name, entry, assembly_hash
                        ),
                        subject=node_id,
                        predicate="entry_flat_address",
                        value=entry,
                        status="observed",
                        evidence_refs=(evidence_ref,),
                        producer=f"{entry_source}-entry-extractor",
                        assembly_sha256=assembly_hash,
                        binary_sha256=binary_sha256,
                    )
                )

        for name, (path, assembly, assembly_hash) in sorted(source_by_name.items()):
            caller_id = routine_ids[name]
            parsed = parse_ghidra_asm(assembly)
            graph._add_cfg_observations(
                target, name, caller_id, assembly_hash, parsed
            )
            graph._add_condition_flag_observations(
                target, name, parsed
            )
            graph._add_frame_slot_observations(
                target,
                name,
                caller_id,
                assembly_hash,
                parsed,
                binary_sha256,
            )
            graph._add_block_frame_slot_summaries(
                target, name, parsed
            )
            graph._add_frame_slot_liveness(
                target, name, parsed
            )
            graph._add_register_operand_observations(
                target,
                name,
                caller_id,
                assembly_hash,
                parsed,
                binary_sha256,
            )
            graph._add_register_storage_liveness(target, name, parsed)
            graph._add_condition_flag_liveness(target, name, parsed)
            for address, instruction, source_segment in zip(
                parsed["addrs"],
                parsed["insts"],
                parsed["segments"],
                strict=True,
            ):
                if not is_call(instruction):
                    continue
                graph._add_call_observation(
                    target,
                    name,
                    caller_id,
                    path,
                    assembly_hash,
                    address,
                    instruction,
                    source_segment,
                    routine_ids,
                    address_to_routines,
                    binary_sha256,
                )
        return graph

    def _add_condition_flag_observations(
        self,
        target: str,
        routine_name: str,
        parsed: dict[str, Any],
    ) -> None:
        cfg = build_blocks(
            parsed["addrs"], parsed["insts"], parsed["segments"]
        )
        instruction_facts = {
            instruction["address"]: fact
            for fact in self.facts.values()
            if (
                fact.predicate == "basic_block_instruction_listing"
                and self.nodes[fact.subject].attributes["routine"]
                == routine_name
            )
            for instruction in fact.value["instructions"]
        }
        block_edges = {
            edge.target: edge.id
            for edge in self.edges.values()
            if (
                edge.relation == "contains_basic_block"
                and self.nodes[edge.source].attributes.get("name")
                == routine_name
            )
        }
        for address, instruction in zip(
            parsed["addrs"], parsed["insts"], strict=True
        ):
            mnemonic, operands = _split_assembly_operands(instruction)
            instruction_index = cfg["idx"][address]
            block_id = (
                f"block:{target}:{routine_name}:"
                f"{cfg['block_of'][instruction_index]}"
            )
            for flag, access in _condition_flag_effects(mnemonic, operands):
                evidence_ref = f"asm:{routine_name}:0x{address:x}"
                self.add_fact(
                    Fact(
                        id=_stable_id(
                            "condition-flag-access",
                            target,
                            routine_name,
                            address,
                            flag,
                            access,
                            instruction_facts[address].id,
                        ),
                        subject=f"routine:{target}:{routine_name}",
                        predicate="condition_flag_access",
                        value={
                            "address": address,
                            "instruction": instruction,
                            "flag": flag,
                            "access": access,
                        },
                        status="derived",
                        evidence_refs=(
                            evidence_ref,
                            f"isa:x86-16:flags:{mnemonic.lower()}",
                        ),
                        producer="x86-16-condition-flag-interpreter",
                        supports=(instruction_facts[address].id,),
                        via_edges=(block_edges[block_id],),
                    )
                )
            for flag, register_bit, direction in _flag_register_transfers(
                mnemonic
            ):
                evidence_ref = f"asm:{routine_name}:0x{address:x}"
                self.add_fact(
                    Fact(
                        id=_stable_id(
                            "flag-register-transfer",
                            target,
                            routine_name,
                            address,
                            flag,
                            register_bit,
                            direction,
                            instruction_facts[address].id,
                        ),
                        subject=f"routine:{target}:{routine_name}",
                        predicate="flag_register_transfer",
                        value={
                            "address": address,
                            "instruction": instruction,
                            "flag": flag,
                            "register": "AH",
                            "register_bit": register_bit,
                            "direction": direction,
                        },
                        status="derived",
                        evidence_refs=(
                            evidence_ref,
                            f"isa:x86-16:lahf-sahf:{mnemonic.lower()}",
                        ),
                        producer="x86-16-flag-register-transfer-interpreter",
                        supports=(instruction_facts[address].id,),
                        via_edges=(block_edges[block_id],),
                    )
                )

    def _add_frame_slot_observations(
        self,
        target: str,
        routine_name: str,
        routine_id: str,
        assembly_hash: str,
        parsed: dict[str, Any],
        binary_sha256: str | None,
    ) -> None:
        for address, instruction in zip(
            parsed["addrs"], parsed["insts"], strict=True
        ):
            mnemonic, operands = _split_assembly_operands(instruction)
            for operand_index, operand in enumerate(operands):
                match = _FRAME_SLOT_OPERAND.search(operand)
                if match is None:
                    continue
                displacement = _parse_frame_displacement(match)
                slot_id = (
                    f"stack-slot:{target}:{routine_name}:bp:"
                    f"{displacement:+x}"
                )
                evidence_ref = (
                    f"asm:{routine_name}:0x{address:x}:operand:{operand_index}"
                )
                fact_id = _stable_id(
                    "frame-operand",
                    target,
                    routine_name,
                    address,
                    operand_index,
                    assembly_hash,
                )
                observation_id = (
                    f"frame-operand:{target}:{routine_name}:"
                    f"{address:x}:{operand_index}"
                )
                self.add_node(
                    Node(
                        slot_id,
                        "stack-slot",
                        target,
                        {
                            "routine": routine_name,
                            "frame_base": "BP",
                            "displacement_bytes": displacement,
                            "assembly_sha256": assembly_hash,
                        },
                    )
                )
                self.add_node(
                    Node(
                        observation_id,
                        "frame-operand",
                        target,
                        {
                            "routine": routine_name,
                            "address": address,
                            "instruction": instruction,
                            "operand_index": operand_index,
                            "operand_text": operand,
                            "displacement_bytes": displacement,
                            "assembly_sha256": assembly_hash,
                        },
                    )
                )
                edge_id = (
                    f"edge:{routine_id}:frame-slot:"
                    f"{address:x}:{operand_index}"
                )
                observation_edge_id = (
                    f"edge:{observation_id}:references:{slot_id}"
                )
                self.add_edge(
                    Edge(
                        edge_id,
                        routine_id,
                        slot_id,
                        "accesses_frame_slot",
                        (evidence_ref,),
                    )
                )
                self.add_edge(
                    Edge(
                        observation_edge_id,
                        observation_id,
                        slot_id,
                        "references_frame_slot",
                        (evidence_ref,),
                    )
                )
                self.add_fact(
                    Fact(
                        id=fact_id,
                        subject=observation_id,
                        predicate="frame_operand_observed",
                        value={
                            "address": address,
                            "instruction": instruction,
                            "operand_index": operand_index,
                            "operand_text": operand,
                            "displacement_bytes": displacement,
                        },
                        status="observed",
                        evidence_refs=(evidence_ref,),
                        producer="assembly-frame-operand-extractor",
                        assembly_sha256=assembly_hash,
                        binary_sha256=binary_sha256,
                    )
                )
                access = _frame_slot_access(
                    mnemonic, operand_index, len(operands)
                )
                if access is not None:
                    self.add_fact(
                        Fact(
                            id=_stable_id("frame-access", fact_id, access),
                            subject=observation_id,
                            predicate="frame_operand_access",
                            value={
                                "address": address,
                                "instruction": instruction,
                                "operand_index": operand_index,
                                "access": access,
                            },
                            status="derived",
                            evidence_refs=(evidence_ref,),
                            producer="assembly-frame-access-interpreter",
                            supports=(fact_id,),
                            via_edges=(observation_edge_id,),
                            assembly_sha256=assembly_hash,
                            binary_sha256=binary_sha256,
                        )
                    )

    def _add_block_frame_slot_summaries(
        self,
        target: str,
        routine_name: str,
        parsed: dict[str, Any],
    ) -> None:
        cfg = build_blocks(
            parsed["addrs"], parsed["insts"], parsed["segments"]
        )
        frame_accesses: dict[int, list[Fact]] = defaultdict(list)
        for fact in self.facts.values():
            if (
                fact.predicate != "frame_operand_access"
                or self.nodes[fact.subject].attributes["routine"] != routine_name
            ):
                continue
            frame_accesses[fact.value["address"]].append(fact)

        block_edges = {
            edge.target: edge.id
            for edge in self.edges.values()
            if edge.relation == "contains_basic_block"
            and self.nodes[edge.source].attributes.get("name") == routine_name
        }
        for block_index, (start, end) in enumerate(
            zip(cfg["start"], cfg["end"], strict=True)
        ):
            block_id = f"block:{target}:{routine_name}:{block_index}"
            used_before_definition: dict[str, Fact] = {}
            defined: dict[str, Fact] = {}
            for instruction_index in range(start, end + 1):
                address = parsed["addrs"][instruction_index]
                for access_fact in frame_accesses[address]:
                    slot_edge_id = access_fact.via_edges[0]
                    slot_id = self.edges[slot_edge_id].target
                    access = access_fact.value["access"]
                    if "read" in access and slot_id not in defined:
                        used_before_definition.setdefault(slot_id, access_fact)
                    if access in {"write", "read_write"}:
                        defined.setdefault(slot_id, access_fact)
            self._add_frame_slot_summary_fact(
                block_id,
                "frame_slots_used",
                used_before_definition,
                block_edges.get(block_id),
            )
            self._add_frame_slot_summary_fact(
                block_id,
                "frame_slots_defined",
                defined,
                block_edges.get(block_id),
            )

    def _add_frame_slot_summary_fact(
        self,
        block_id: str,
        predicate: str,
        slot_accesses: dict[str, Fact],
        block_edge_id: str | None,
    ) -> None:
        if not slot_accesses or block_edge_id is None:
            return
        slot_ids = sorted(slot_accesses)
        supports = tuple(
            slot_accesses[slot_id].id for slot_id in slot_ids
        )
        slot_edges = tuple(
            slot_accesses[slot_id].via_edges[0] for slot_id in slot_ids
        )
        evidence_refs = set(self.edges[block_edge_id].evidence_refs)
        for fact in slot_accesses.values():
            evidence_refs.update(fact.evidence_refs)
        self.add_fact(
            Fact(
                id=_stable_id(
                    "frame-block-summary",
                    block_id,
                    predicate,
                    slot_ids,
                    supports,
                ),
                subject=block_id,
                predicate=predicate,
                value={"slots": slot_ids},
                status="derived",
                evidence_refs=tuple(sorted(evidence_refs)),
                producer="assembly-frame-block-summary",
                supports=supports,
                via_edges=(block_edge_id, *slot_edges),
            )
        )

    def _add_frame_slot_liveness(
        self,
        target: str,
        routine_name: str,
        parsed: dict[str, Any],
    ) -> None:
        cfg = build_blocks(
            parsed["addrs"], parsed["insts"], parsed["segments"]
        )
        if cfg["n"] == 0:
            return

        block_ids = [
            f"block:{target}:{routine_name}:{index}"
            for index in range(cfg["nblocks"])
        ]
        frame_accesses: dict[int, list[Fact]] = defaultdict(list)
        for fact in self.facts.values():
            if (
                fact.predicate == "frame_operand_access"
                and self.nodes[fact.subject].attributes["routine"] == routine_name
            ):
                frame_accesses[fact.value["address"]].append(fact)
        if not frame_accesses:
            return

        uses = {block_id: set() for block_id in block_ids}
        definitions = {block_id: set() for block_id in block_ids}
        for instruction_index, address in enumerate(parsed["addrs"]):
            block_id = block_ids[cfg["block_of"][instruction_index]]
            for fact in frame_accesses[address]:
                slot_id = self.edges[fact.via_edges[0]].target
                access = fact.value["access"]
                if "read" in access and slot_id not in definitions[block_id]:
                    uses[block_id].add(slot_id)
                if access in {"write", "read_write"}:
                    definitions[block_id].add(slot_id)

        live_in = {block_id: set() for block_id in block_ids}
        live_out = {block_id: set() for block_id in block_ids}
        changed = True
        while changed:
            changed = False
            for block_index in reversed(range(cfg["nblocks"])):
                block_id = block_ids[block_index]
                successors = {
                    block_ids[successor]
                    for successor in cfg["succ"][block_index]
                }
                next_out = set().union(
                    *(live_in[successor] for successor in successors)
                )
                next_in = uses[block_id] | (next_out - definitions[block_id])
                if next_in != live_in[block_id] or next_out != live_out[block_id]:
                    live_in[block_id] = next_in
                    live_out[block_id] = next_out
                    changed = True

        supports = {
            fact.id
            for fact in self.facts.values()
            if fact.subject in block_ids
            and fact.predicate in {
                "basic_block_instruction_listing",
                "frame_slots_used",
                "frame_slots_defined",
            }
        }
        if not supports:
            return
        relevant_edges = {
            edge.id
            for edge in self.edges.values()
            if edge.relation == "contains_basic_block"
            and edge.target in block_ids
        }
        relevant_edges.update(
            edge.id
            for edge in self.edges.values()
            if edge.relation in {"cfg_branch", "cfg_fallthrough"}
            and edge.source in block_ids
            and edge.target in block_ids
        )
        if not relevant_edges:
            return
        support_ids = tuple(sorted(supports))
        edge_ids = tuple(sorted(relevant_edges))
        evidence_refs = {
            evidence_ref
            for fact_id in support_ids
            for evidence_ref in self.facts[fact_id].evidence_refs
        }
        evidence_refs.update(
            evidence_ref
            for edge_id in edge_ids
            for evidence_ref in self.edges[edge_id].evidence_refs
        )
        block_results = [
            {
                "block": block_id,
                "live_in": sorted(live_in[block_id]),
                "live_out": sorted(live_out[block_id]),
            }
            for block_id in block_ids
        ]
        self.add_fact(
            Fact(
                id=_stable_id(
                    "frame-slot-liveness",
                    target,
                    routine_name,
                    support_ids,
                    edge_ids,
                ),
                subject=f"routine:{target}:{routine_name}",
                predicate="frame_slot_liveness",
                value={"blocks": block_results},
                status="derived",
                evidence_refs=tuple(sorted(evidence_refs)),
                producer="assembly-frame-liveness-analysis",
                supports=support_ids,
                via_edges=edge_ids,
            )
        )

    def _add_register_operand_observations(
        self,
        target: str,
        routine_name: str,
        routine_id: str,
        assembly_hash: str,
        parsed: dict[str, Any],
        binary_sha256: str | None,
    ) -> None:
        instruction_facts = {
            instruction["address"]: fact
            for fact in self.facts.values()
            if (
                fact.predicate == "basic_block_instruction_listing"
                and self.nodes[fact.subject].attributes["routine"]
                == routine_name
            )
            for instruction in fact.value["instructions"]
        }
        for address, instruction in zip(
            parsed["addrs"], parsed["insts"], strict=True
        ):
            mnemonic, operands = _split_assembly_operands(instruction)
            for operand_index, operand in enumerate(operands):
                match = _DIRECT_REGISTER_OPERAND.fullmatch(operand)
                if match is None:
                    continue
                register = match.group(1)
                self._add_register_operand_observation(
                    target,
                    routine_name,
                    routine_id,
                    assembly_hash,
                    binary_sha256,
                    address,
                    instruction,
                    mnemonic,
                    len(operands),
                    operand_index,
                    operand,
                    register,
                )
            for register, access in _implicit_register_effects(
                mnemonic, operands
            ):
                self._add_implicit_register_access(
                    target,
                    routine_name,
                    routine_id,
                    assembly_hash,
                    binary_sha256,
                    address,
                    instruction,
                    register,
                    access,
                    instruction_facts[address],
                )
        self._add_register_storage_relations(target, routine_name)

    def _add_implicit_register_access(
        self,
        target: str,
        routine_name: str,
        routine_id: str,
        assembly_hash: str,
        binary_sha256: str | None,
        address: int,
        instruction: str,
        register: str,
        access: str,
        instruction_fact: Fact,
    ) -> None:
        register_id = f"register:{target}:{routine_name}:{register}"
        if register_id not in self.nodes:
            family, bit_offset, width = _REGISTER_STORAGE[register]
            self.add_node(
                Node(
                    register_id,
                    "register",
                    target,
                    {
                        "routine": routine_name,
                        "register": register,
                        "storage_family": family,
                        "storage_bit_offset": bit_offset,
                        "storage_width_bits": width,
                        "assembly_sha256": assembly_hash,
                    },
                )
            )
        evidence_ref = f"asm:{routine_name}:0x{address:x}"
        edge_id = (
            f"edge:{routine_id}:implicit-register:{address:x}:{register}"
        )
        self.add_edge(
            Edge(
                edge_id,
                routine_id,
                register_id,
                "implicitly_uses_register",
                (
                    evidence_ref,
                    f"isa:x86-16:{instruction.split()[0].lower()}",
                ),
            )
        )
        family, bit_offset, width = _REGISTER_STORAGE[register]
        self.add_fact(
            Fact(
                id=_stable_id(
                    "implicit-register-storage-access",
                    target,
                    routine_name,
                    address,
                    register,
                    access,
                    assembly_hash,
                ),
                subject=register_id,
                predicate="register_storage_access",
                value={
                    "address": address,
                    "instruction": instruction,
                    "operand_index": None,
                    "register": register,
                    "storage_family": family,
                    "start_bit": bit_offset,
                    "end_bit": bit_offset + width,
                    "access": access,
                    "implicit": True,
                },
                status="derived",
                evidence_refs=(
                    evidence_ref,
                    f"isa:x86-16:{instruction.split()[0].lower()}",
                ),
                producer="x86-16-implicit-register-effect-interpreter",
                supports=(instruction_fact.id,),
                via_edges=(edge_id,),
                assembly_sha256=assembly_hash,
                binary_sha256=binary_sha256,
            )
        )

    def _add_register_storage_relations(
        self, target: str, routine_name: str
    ) -> None:
        registers = {
            node.attributes["register"]: node
            for node in self.nodes.values()
            if node.kind == "register"
            and node.target == target
            and node.attributes.get("routine") == routine_name
        }
        for register, register_node in registers.items():
            family, bit_offset, width = _REGISTER_STORAGE[register]
            for other_register, other_node in registers.items():
                if register >= other_register:
                    continue
                other_family, other_offset, other_width = (
                    _REGISTER_STORAGE[other_register]
                )
                if family != other_family or not _ranges_overlap(
                    bit_offset, width, other_offset, other_width
                ):
                    continue
                start = max(bit_offset, other_offset)
                end = min(bit_offset + width, other_offset + other_width)
                architecture = (
                    "x86" if "ECX" in {register, other_register} else "x86-16"
                )
                self.add_edge(
                    Edge(
                        f"edge:register-storage-overlap:"
                        f"{register_node.id}:{other_node.id}",
                        register_node.id,
                        other_node.id,
                        "overlaps_register_storage",
                        (
                            (
                                f"isa:{architecture}:{register}[{start}:{end}]"
                                f":{other_register}[{start}:{end}]"
                            ),
                        ),
                    )
                )

    def _add_register_storage_liveness(
        self,
        target: str,
        routine_name: str,
        parsed: dict[str, Any],
    ) -> None:
        cfg = build_blocks(
            parsed["addrs"], parsed["insts"], parsed["segments"]
        )
        if cfg["n"] == 0:
            return
        block_ids = [
            f"block:{target}:{routine_name}:{index}"
            for index in range(cfg["nblocks"])
        ]
        accesses_by_address: dict[int, list[Fact]] = defaultdict(list)
        for fact in self.facts.values():
            if (
                fact.predicate == "register_storage_access"
                and self.nodes[fact.subject].attributes["routine"] == routine_name
            ):
                accesses_by_address[fact.value["address"]].append(fact)
        if not accesses_by_address:
            return

        uses = {block_id: set() for block_id in block_ids}
        definitions = {block_id: set() for block_id in block_ids}
        for instruction_index, address in enumerate(parsed["addrs"]):
            block_id = block_ids[cfg["block_of"][instruction_index]]
            for fact in accesses_by_address[address]:
                value = fact.value
                bits = {
                    (value["storage_family"], bit)
                    for bit in range(value["start_bit"], value["end_bit"])
                }
                if "read" in value["access"]:
                    uses[block_id].update(bits - definitions[block_id])
                if value["access"] in {"write", "read_write"}:
                    definitions[block_id].update(bits)

        live_in = {block_id: set() for block_id in block_ids}
        live_out = {block_id: set() for block_id in block_ids}
        changed = True
        while changed:
            changed = False
            for block_index in reversed(range(cfg["nblocks"])):
                block_id = block_ids[block_index]
                successors = {
                    block_ids[successor]
                    for successor in cfg["succ"][block_index]
                }
                next_out = set().union(
                    *(live_in[successor] for successor in successors)
                )
                next_in = uses[block_id] | (next_out - definitions[block_id])
                if next_in != live_in[block_id] or next_out != live_out[block_id]:
                    live_in[block_id] = next_in
                    live_out[block_id] = next_out
                    changed = True

        self._add_register_liveness_fact(
            target,
            routine_name,
            block_ids,
            live_in,
            live_out,
            accesses_by_address,
        )

    def _add_register_liveness_fact(
        self,
        target: str,
        routine_name: str,
        block_ids: list[str],
        live_in: dict[str, set[tuple[str, int]]],
        live_out: dict[str, set[tuple[str, int]]],
        accesses_by_address: dict[int, list[Fact]],
    ) -> None:
        support_ids = {
            fact.id
            for fact in self.facts.values()
            if (
                fact.predicate == "basic_block_instruction_listing"
                and self.nodes[fact.subject].attributes["routine"]
                == routine_name
            )
        }
        support_ids.update(
            fact.id
            for facts in accesses_by_address.values()
            for fact in facts
        )
        if not support_ids:
            return
        block_edges = {
            edge.id
            for edge in self.edges.values()
            if edge.relation == "contains_basic_block"
            and edge.target in block_ids
        }
        cfg_edges = {
            edge.id
            for edge in self.edges.values()
            if edge.relation in {"cfg_branch", "cfg_fallthrough"}
            and edge.source in block_ids
            and edge.target in block_ids
        }
        edge_ids = block_edges | cfg_edges
        if not edge_ids:
            return
        evidence_refs = {
            evidence_ref
            for fact_id in support_ids
            for evidence_ref in self.facts[fact_id].evidence_refs
        }
        evidence_refs.update(
            evidence_ref
            for edge_id in edge_ids
            for evidence_ref in self.edges[edge_id].evidence_refs
        )
        block_results = [
            {
                "block": block_id,
                "live_in": _register_storage_ranges(live_in[block_id]),
                "live_out": _register_storage_ranges(live_out[block_id]),
            }
            for block_id in block_ids
        ]
        self.add_fact(
            Fact(
                id=_stable_id(
                    "register-storage-liveness",
                    target,
                    routine_name,
                    tuple(sorted(support_ids)),
                    tuple(sorted(edge_ids)),
                ),
                subject=f"routine:{target}:{routine_name}",
                predicate="register_storage_liveness",
                value={"blocks": block_results},
                status="derived",
                evidence_refs=tuple(sorted(evidence_refs)),
                producer="assembly-register-liveness-analysis",
                supports=tuple(sorted(support_ids)),
                via_edges=tuple(sorted(edge_ids)),
            )
        )

    def _add_condition_flag_liveness(
        self,
        target: str,
        routine_name: str,
        parsed: dict[str, Any],
    ) -> None:
        cfg = build_blocks(
            parsed["addrs"], parsed["insts"], parsed["segments"]
        )
        if cfg["n"] == 0:
            return
        block_ids = [
            f"block:{target}:{routine_name}:{index}"
            for index in range(cfg["nblocks"])
        ]
        accesses_by_address: dict[int, list[Fact]] = defaultdict(list)
        for fact in self.facts.values():
            if (
                fact.predicate == "condition_flag_access"
                and fact.subject == f"routine:{target}:{routine_name}"
            ):
                accesses_by_address[fact.value["address"]].append(fact)
        if not accesses_by_address:
            return

        uses = {block_id: set() for block_id in block_ids}
        definitions = {block_id: set() for block_id in block_ids}
        for instruction_index, address in enumerate(parsed["addrs"]):
            block_id = block_ids[cfg["block_of"][instruction_index]]
            for fact in accesses_by_address[address]:
                flag = fact.value["flag"]
                access = fact.value["access"]
                if (
                    access in {"read", "read_write"}
                    and flag not in definitions[block_id]
                ):
                    uses[block_id].add(flag)
                if access in {"write", "read_write", "clobber"}:
                    definitions[block_id].add(flag)

        live_in = {block_id: set() for block_id in block_ids}
        live_out = {block_id: set() for block_id in block_ids}
        changed = True
        while changed:
            changed = False
            for block_index in reversed(range(cfg["nblocks"])):
                block_id = block_ids[block_index]
                successors = {
                    block_ids[successor]
                    for successor in cfg["succ"][block_index]
                }
                next_out = set().union(
                    *(live_in[successor] for successor in successors)
                )
                next_in = uses[block_id] | (next_out - definitions[block_id])
                if next_in != live_in[block_id] or next_out != live_out[block_id]:
                    live_in[block_id] = next_in
                    live_out[block_id] = next_out
                    changed = True

        self._add_condition_flag_liveness_fact(
            target,
            routine_name,
            block_ids,
            live_in,
            live_out,
            accesses_by_address,
        )

    def _add_condition_flag_liveness_fact(
        self,
        target: str,
        routine_name: str,
        block_ids: list[str],
        live_in: dict[str, set[str]],
        live_out: dict[str, set[str]],
        accesses_by_address: dict[int, list[Fact]],
    ) -> None:
        support_ids = {
            fact.id
            for fact in self.facts.values()
            if (
                fact.predicate == "basic_block_instruction_listing"
                and self.nodes[fact.subject].attributes["routine"]
                == routine_name
            )
        }
        support_ids.update(
            fact.id
            for facts in accesses_by_address.values()
            for fact in facts
        )
        block_edges = {
            edge.id
            for edge in self.edges.values()
            if edge.relation == "contains_basic_block"
            and edge.target in block_ids
        }
        cfg_edges = {
            edge.id
            for edge in self.edges.values()
            if edge.relation in {"cfg_branch", "cfg_fallthrough"}
            and edge.source in block_ids
            and edge.target in block_ids
        }
        edge_ids = block_edges | cfg_edges
        if not support_ids or not edge_ids:
            return
        evidence_refs = {
            evidence_ref
            for fact_id in support_ids
            for evidence_ref in self.facts[fact_id].evidence_refs
        }
        evidence_refs.update(
            evidence_ref
            for edge_id in edge_ids
            for evidence_ref in self.edges[edge_id].evidence_refs
        )
        self.add_fact(
            Fact(
                id=_stable_id(
                    "condition-flag-liveness",
                    target,
                    routine_name,
                    tuple(sorted(support_ids)),
                    tuple(sorted(edge_ids)),
                ),
                subject=f"routine:{target}:{routine_name}",
                predicate="condition_flag_liveness",
                value={
                    "blocks": [
                        {
                            "block": block_id,
                            "live_in": sorted(live_in[block_id]),
                            "live_out": sorted(live_out[block_id]),
                        }
                        for block_id in block_ids
                    ]
                },
                status="derived",
                evidence_refs=tuple(sorted(evidence_refs)),
                producer="assembly-condition-flag-liveness-analysis",
                supports=tuple(sorted(support_ids)),
                via_edges=tuple(sorted(edge_ids)),
            )
        )

    def _add_register_operand_observation(
        self,
        target: str,
        routine_name: str,
        routine_id: str,
        assembly_hash: str,
        binary_sha256: str | None,
        address: int,
        instruction: str,
        mnemonic: str,
        operand_count: int,
        operand_index: int,
        operand: str,
        register: str,
    ) -> None:
        evidence_ref = (
            f"asm:{routine_name}:0x{address:x}:operand:{operand_index}"
        )
        register_id = f"register:{target}:{routine_name}:{register}"
        observation_id = (
            f"register-operand:{target}:{routine_name}:"
            f"{address:x}:{operand_index}"
        )
        observation_fact_id = _stable_id(
            "register-operand",
            target,
            routine_name,
            address,
            operand_index,
            assembly_hash,
        )
        self.add_node(
            Node(
                register_id,
                "register",
                target,
                {
                    "routine": routine_name,
                    "register": register,
                    "storage_family": _REGISTER_STORAGE[register][0],
                    "storage_bit_offset": _REGISTER_STORAGE[register][1],
                    "storage_width_bits": _REGISTER_STORAGE[register][2],
                    "assembly_sha256": assembly_hash,
                },
            )
        )
        self.add_node(
            Node(
                observation_id,
                "register-operand",
                target,
                {
                    "routine": routine_name,
                    "address": address,
                    "instruction": instruction,
                    "operand_index": operand_index,
                    "operand_text": operand,
                    "register": register,
                    "assembly_sha256": assembly_hash,
                },
            )
        )
        self.add_edge(
            Edge(
                f"edge:{routine_id}:register:{address:x}:{operand_index}",
                routine_id,
                register_id,
                "uses_register",
                (evidence_ref,),
            )
        )
        register_edge_id = f"edge:{observation_id}:references:{register_id}"
        self.add_edge(
            Edge(
                register_edge_id,
                observation_id,
                register_id,
                "references_register",
                (evidence_ref,),
            )
        )
        self.add_fact(
            Fact(
                id=observation_fact_id,
                subject=observation_id,
                predicate="register_operand_observed",
                value={
                    "address": address,
                    "instruction": instruction,
                    "operand_index": operand_index,
                    "operand_text": operand,
                    "register": register,
                },
                status="observed",
                evidence_refs=(evidence_ref,),
                producer="assembly-register-operand-extractor",
                assembly_sha256=assembly_hash,
                binary_sha256=binary_sha256,
            )
        )
        access = _explicit_operand_access(
            mnemonic, operand_index, operand_count
        )
        if access is None:
            return
        access_fact_id = _stable_id(
            "register-access", observation_fact_id, access
        )
        self.add_fact(
            Fact(
                id=access_fact_id,
                subject=observation_id,
                predicate="register_operand_access",
                value={
                    "address": address,
                    "instruction": instruction,
                    "operand_index": operand_index,
                    "register": register,
                    "access": access,
                },
                status="derived",
                evidence_refs=(evidence_ref,),
                producer="assembly-register-access-interpreter",
                supports=(observation_fact_id,),
                via_edges=(register_edge_id,),
                assembly_sha256=assembly_hash,
                binary_sha256=binary_sha256,
            )
        )
        storage_family, start_bit, width = _REGISTER_STORAGE[register]
        end_bit = start_bit + width
        self.add_fact(
            Fact(
                id=_stable_id(
                    "register-storage-access",
                    access_fact_id,
                    storage_family,
                    start_bit,
                    end_bit,
                ),
                subject=observation_id,
                predicate="register_storage_access",
                value={
                    "address": address,
                    "instruction": instruction,
                    "operand_index": operand_index,
                    "register": register,
                    "storage_family": storage_family,
                    "start_bit": start_bit,
                    "end_bit": end_bit,
                    "access": access,
                },
                status="derived",
                evidence_refs=(
                    *self.facts[access_fact_id].evidence_refs,
                    (
                        f"isa:x86:{register}[{start_bit}:{end_bit}]"
                        if register == "ECX"
                        else f"isa:x86-16:{register}[{start_bit}:{end_bit}]"
                    ),
                ),
                producer="assembly-register-storage-interpreter",
                supports=(access_fact_id,),
                via_edges=(register_edge_id,),
                assembly_sha256=assembly_hash,
                binary_sha256=binary_sha256,
            )
        )

    def _add_cfg_observations(
        self,
        target: str,
        routine_name: str,
        routine_id: str,
        assembly_hash: str,
        parsed: dict[str, Any],
    ) -> None:
        cfg = build_blocks(
            parsed["addrs"], parsed["insts"], parsed["segments"]
        )
        block_ids = []
        for block_number, (start, end) in enumerate(
            zip(cfg["start"], cfg["end"], strict=True)
        ):
            block_id = f"block:{target}:{routine_name}:{block_number}"
            block_ids.append(block_id)
            self.add_node(
                Node(
                    block_id,
                    "basic-block",
                    target,
                    {
                        "routine": routine_name,
                        "start_address": parsed["addrs"][start],
                        "end_address": parsed["addrs"][end],
                        "instruction_count": cfg["size"][block_number],
                        "assembly_sha256": assembly_hash,
                    },
                )
            )
            self.add_edge(
                Edge(
                    f"edge:{routine_id}:contains:{block_number}",
                    routine_id,
                    block_id,
                    "contains_basic_block",
                    (f"asm:{routine_name}:0x{parsed['addrs'][start]:x}",),
                )
            )
            block_instructions = [
                {
                    "address": parsed["addrs"][instruction_index],
                    "instruction": parsed["insts"][instruction_index],
                }
                for instruction_index in range(start, end + 1)
            ]
            self.add_fact(
                Fact(
                    id=_stable_id(
                        "block-instruction-listing",
                        target,
                        routine_name,
                        block_number,
                        assembly_hash,
                    ),
                    subject=block_id,
                    predicate="basic_block_instruction_listing",
                    value={"instructions": block_instructions},
                    status="observed",
                    evidence_refs=tuple(
                        f"asm:{routine_name}:0x{item['address']:x}"
                        for item in block_instructions
                    ),
                    producer="assembly-block-instruction-extractor",
                    assembly_sha256=assembly_hash,
                )
            )

        for block_number, block_id in enumerate(block_ids):
            last_instruction_index = cfg["end"][block_number]
            last_instruction = parsed["insts"][last_instruction_index]
            last_address = parsed["addrs"][last_instruction_index]
            branch_target_address = resolve_branch_target(
                last_instruction,
                parsed["segments"][last_instruction_index],
            )
            target_index = cfg["idx"].get(branch_target_address)
            if (
                is_branch(last_instruction)
                and target_index is not None
            ):
                destination_block = block_ids[cfg["block_of"][target_index]]
                self._add_cfg_edge(
                    block_id,
                    destination_block,
                    routine_name,
                    last_address,
                    "cfg_branch",
                )

            next_instruction_index = last_instruction_index + 1
            has_fallthrough = (
                next_instruction_index < len(parsed["insts"])
                and not is_ret(last_instruction)
                and not (
                    is_branch(last_instruction)
                    and not is_cond_branch(last_instruction)
                )
            )
            if has_fallthrough:
                next_block = block_ids[cfg["block_of"][next_instruction_index]]
                self._add_cfg_edge(
                    block_id,
                    next_block,
                    routine_name,
                    last_address,
                    "cfg_fallthrough",
                )

    def _add_cfg_edge(
        self,
        source: str,
        destination: str,
        routine_name: str,
        instruction_address: int,
        relation: str,
    ) -> None:
        self.add_edge(
            Edge(
                f"edge:{source}:{relation}:{destination}",
                source,
                destination,
                relation,
                (f"asm:{routine_name}:0x{instruction_address:x}",),
            )
        )

    def _same_value_adjacency(self) -> dict[str, list[tuple[str, str]]]:
        adjacent: dict[str, list[tuple[str, str]]] = {
            node_id: [] for node_id in self.nodes
        }
        for edge in self.edges.values():
            if edge.relation != "same_value" or edge.status not in _EDGE_STATUSES:
                continue
            adjacent[edge.source].append((edge.target, edge.id))
            adjacent[edge.target].append((edge.source, edge.id))
        return {
            node_id: sorted(neighbors)
            for node_id, neighbors in adjacent.items()
        }

    @staticmethod
    def _same_value_paths(
        start: str, adjacency: dict[str, list[tuple[str, str]]]
    ) -> dict[str, tuple[str, ...]]:
        paths = {start: ()}
        pending = deque([start])
        while pending:
            current = pending.popleft()
            for neighbor, edge_id in adjacency[current]:
                if neighbor in paths:
                    continue
                paths[neighbor] = (*paths[current], edge_id)
                pending.append(neighbor)
        return paths

    def _derived_fact(
        self, source: Fact, subject: str, edge_ids: tuple[str, ...]
    ) -> Fact:
        evidence = set(source.evidence_refs)
        for edge_id in edge_ids:
            evidence.update(self.edges[edge_id].evidence_refs)
        fact_id = _stable_id(
            "derived",
            source.id,
            subject,
            source.predicate,
            source.value,
            edge_ids,
        )
        return Fact(
            id=fact_id,
            subject=subject,
            predicate=source.predicate,
            value=source.value,
            status="derived",
            evidence_refs=tuple(sorted(evidence)),
            producer="same-value-propagation",
            supports=(source.id,),
            via_edges=edge_ids,
            assembly_sha256=source.assembly_sha256,
            binary_sha256=source.binary_sha256,
            confidence=source.confidence,
        )

    def _has_same_value_fact(
        self, subject: str, predicate: str, value: Any
    ) -> bool:
        value_key = _canonical_json(value)
        return any(
            fact.predicate == predicate
            and _canonical_json(fact.value) == value_key
            for fact in self.facts_for(subject, predicate)
        )

    def _require_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            raise ValueError(f"fact graph references unknown node: {node_id}")

    def _require_evidence(self, refs: tuple[str, ...], name: str) -> None:
        if (
            not isinstance(refs, (tuple, list))
            or not refs
            or any(not isinstance(ref, str) or not ref.strip() for ref in refs)
        ):
            raise ValueError(f"{name} must contain at least one non-empty reference")

    @staticmethod
    def _validate_ref_values(
        refs: tuple[str, ...], name: str, allow_empty: bool = False
    ) -> None:
        if (
            not isinstance(refs, (tuple, list))
            or (not allow_empty and not refs)
            or any(not isinstance(ref, str) or not ref.strip() for ref in refs)
        ):
            raise ValueError(f"{name} must contain valid non-empty references")

    def _validate_references(self) -> None:
        for fact in self.facts.values():
            missing_facts = set(fact.supports) - self.facts.keys()
            missing_edges = set(fact.via_edges) - self.edges.keys()
            if missing_facts or missing_edges:
                raise ValueError(
                    f"fact {fact.id} has missing references: "
                    f"facts={sorted(missing_facts)}, edges={sorted(missing_edges)}"
                )

    def _add_call_observation(
        self,
        target: str,
        caller_name: str,
        caller_id: str,
        assembly_path: pathlib.Path,
        assembly_hash: str,
        address: int,
        instruction: str,
        source_segment: int,
        routine_ids: dict[str, str],
        address_to_routines: dict[int, list[str]],
        binary_sha256: str | None,
    ) -> None:
        call_id = f"call:{target}:{caller_name}:{address:05x}"
        evidence_ref = f"asm:{caller_name}:0x{address:x}"
        self.add_node(
            Node(
                call_id,
                "call-site",
                target,
                {
                    "caller": caller_name,
                    "address": address,
                    "instruction": instruction,
                    "assembly_path": str(assembly_path),
                    "assembly_sha256": assembly_hash,
                },
            )
        )
        self.add_edge(
            Edge(
                f"edge:{call_id}:contained-by",
                caller_id,
                call_id,
                "contains_call_site",
                (evidence_ref,),
            )
        )
        destination = resolve_branch_target(instruction, source_segment)
        if destination is None:
            self._add_unresolved_call(
                call_id, target, evidence_ref, assembly_hash, binary_sha256
            )
            return

        self.add_fact(
            Fact(
                id=_stable_id(
                    "call-target", target, caller_name, address, destination
                ),
                subject=call_id,
                predicate="direct_target_flat_address",
                value=destination,
                status="observed",
                evidence_refs=(evidence_ref,),
                producer="assembly-call-extractor",
                assembly_sha256=assembly_hash,
                binary_sha256=binary_sha256,
            )
        )
        callees = address_to_routines.get(destination, [])
        if len(callees) == 1:
            callee_id = callees[0]
            callee_name = next(
                name for name, node_id in routine_ids.items()
                if node_id == callee_id
            )
            self.add_edge(
                Edge(
                    f"edge:{call_id}:calls:{callee_name}",
                    call_id,
                    callee_id,
                    "direct_call",
                    (evidence_ref,),
                )
            )
            return

        unresolved_id = f"address-target:{target}:{destination:05x}"
        self.add_node(
            Node(
                unresolved_id,
                "unresolved-address",
                target,
                {
                    "flat_address": destination,
                    "candidate_routines": sorted(callees),
                },
            )
        )
        self.add_edge(
            Edge(
                f"edge:{call_id}:target:{destination:05x}",
                call_id,
                unresolved_id,
                "unresolved_direct_target",
                (evidence_ref,),
            )
        )

    def _add_unresolved_call(
        self,
        call_id: str,
        target: str,
        evidence_ref: str,
        assembly_hash: str,
        binary_sha256: str | None,
    ) -> None:
        unresolved_id = f"unresolved-target:{call_id}"
        self.add_node(
            Node(
                unresolved_id,
                "unresolved-call-target",
                target,
                {"call_site": call_id},
            )
        )
        self.add_edge(
            Edge(
                f"edge:{call_id}:unresolved-target",
                call_id,
                unresolved_id,
                "unresolved_indirect_target",
                (evidence_ref,),
            )
        )
        self.add_fact(
            Fact(
                id=_stable_id("unresolved-call", call_id),
                subject=call_id,
                predicate="target_resolution",
                value="indirect-or-unparsed",
                status="unknown",
                evidence_refs=(evidence_ref,),
                producer="assembly-call-extractor",
                assembly_sha256=assembly_hash,
                binary_sha256=binary_sha256,
            )
        )

    @staticmethod
    def _add_unique(records: dict, key: str, record: Any, label: str) -> None:
        existing = records.get(key)
        if existing is not None and existing != record:
            raise ValueError(f"{label} id already exists with different content: {key}")
        records[key] = record


def _record_to_dict(record: Any) -> dict[str, Any]:
    result = asdict(record)
    for key, value in result.items():
        if isinstance(value, tuple):
            result[key] = list(value)
    return result


def _record_collection(payload: dict[str, Any], name: str) -> list[dict[str, Any]]:
    records = payload.get(name)
    if not isinstance(records, dict):
        raise TypeError(f"{name} must be a JSON object")
    values = []
    for record_id, record in records.items():
        if not isinstance(record, dict):
            raise TypeError(f"{name} record {record_id} must be a JSON object")
        if record.get("id") != record_id:
            raise ValueError(f"{name} key does not match record id: {record_id}")
        values.append(record)
    return values


def _sequence_field(
    record: dict[str, Any], name: str, required: bool = False
) -> tuple[str, ...]:
    values = record.get(name, ())
    if not isinstance(values, (list, tuple)):
        raise TypeError(f"{name} must be a JSON array")
    if required and not values:
        raise ValueError(f"{name} must not be empty")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(f"{name} must contain non-empty strings")
    return tuple(values)


def _require_text(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")


def _require_json_value(value: Any, label: str) -> None:
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be JSON-serializable") from exc


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _stable_id(*parts: Any) -> str:
    return hashlib.sha256(_canonical_json(parts).encode("utf-8")).hexdigest()


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def _parse_real_mode_address(value: str | None) -> int | None:
    if not value:
        return None
    parts = value.lower().removeprefix("0x").split(":")
    if len(parts) != 2 or any(
        not part or len(part) > 4
        or any(char not in "0123456789abcdef" for char in part)
        for part in parts
    ):
        return None
    return int(parts[0], 16) * 16 + int(parts[1], 16)


def _parse_entry_header(name: str, assembly: str) -> int | None:
    match = re.search(
        rf"(?m)^;\s*{re.escape(name)}\s+entry=([0-9A-Fa-f]{{1,4}}):"
        r"([0-9A-Fa-f]{1,4})\b",
        assembly,
    )
    if not match:
        return None
    return int(match.group(1), 16) * 16 + int(match.group(2), 16)


def _split_assembly_operands(instruction: str) -> tuple[str, list[str]]:
    parts = instruction.split(None, 1)
    if len(parts) == 1:
        return parts[0], []
    operands = []
    start = 0
    bracket_depth = 0
    for index, character in enumerate(parts[1]):
        if character == "[":
            bracket_depth += 1
        elif character == "]":
            bracket_depth -= 1
        elif character == "," and bracket_depth == 0:
            operands.append(parts[1][start:index].strip())
            start = index + 1
    operands.append(parts[1][start:].strip())
    return parts[0], operands


def _frame_slot_access(
    mnemonic: str, operand_index: int, operand_count: int
) -> str | None:
    if mnemonic == "LEA":
        return None
    return _explicit_operand_access(mnemonic, operand_index, operand_count)


def _explicit_operand_access(
    mnemonic: str, operand_index: int, operand_count: int
) -> str | None:
    if mnemonic in {"LDS", "LES"}:
        if operand_index == 0:
            return "write"
        if operand_index == 1:
            return "read"
    if mnemonic == "IN":
        if operand_index == 0:
            return "write"
        if operand_index == 1:
            return "read"
    if mnemonic == "OUT":
        return "read"
    if mnemonic in {"CALL", "CALLF"} and operand_index == 0:
        return "read"
    if mnemonic in {"SHLD", "SHRD"}:
        if operand_index == 0:
            return "read_write"
        if operand_index in {1, 2}:
            return "read"
    if mnemonic in {"MUL", "IMUL", "DIV", "IDIV"}:
        if operand_index == 0 and operand_count == 1:
            return "read"
        if mnemonic == "IMUL" and operand_count == 2:
            if operand_index == 0:
                return "read_write"
            if operand_index == 1:
                return "read"
        if mnemonic == "IMUL" and operand_count == 3:
            if operand_index == 0:
                return "write"
            if operand_index == 1:
                return "read"
    if mnemonic == "MOV":
        if operand_index == 0:
            return "write"
        if operand_index == 1:
            return "read"
    if mnemonic in _FRAME_SLOT_READ_ONLY or mnemonic == "PUSH":
        return "read"
    if mnemonic == "POP":
        return "write" if operand_index == 0 else None
    if mnemonic == "XCHG":
        return "read_write"
    if mnemonic == "LEA" and operand_index == 0:
        return "write"
    if mnemonic in _FRAME_SLOT_READ_MODIFY_WRITE:
        if operand_index == 0:
            return "read_write"
        if operand_index == 1:
            return "read"
    return None


def _implicit_register_effects(
    mnemonic: str, operands: list[str]
) -> list[tuple[str, str]]:
    if mnemonic == "LAHF":
        return [("AH", "write")]
    if mnemonic == "SAHF":
        return [("AH", "read")]
    if mnemonic == "JECXZ":
        return [("ECX", "read")]
    if mnemonic == "JCXZ":
        return [("CX", "read")]
    if mnemonic in _LOOP_MNEMONICS:
        return [("CX", "read_write")]

    base_mnemonic, separator, repeat_prefix = mnemonic.partition(".")
    string_widths = {
        "MOVSB": 8,
        "MOVSW": 16,
        "MOVSD": 32,
        "LODSB": 8,
        "LODSW": 16,
        "STOSB": 8,
        "STOSW": 16,
        "CMPSB": 8,
        "CMPSW": 16,
        "SCASB": 8,
        "SCASW": 16,
        "INSB": 8,
        "INSW": 16,
        "OUTSB": 8,
        "OUTSW": 16,
    }
    if base_mnemonic in string_widths:
        if separator and repeat_prefix not in {
            "REP",
            "REPE",
            "REPZ",
            "REPNE",
            "REPNZ",
        }:
            return []
        width = string_widths[base_mnemonic]
        effects: list[tuple[str, str]] = []
        if base_mnemonic.startswith(("MOVS", "CMPS")):
            effects.extend((("SI", "read_write"), ("DI", "read_write")))
        elif base_mnemonic.startswith(("LODS", "OUTS")):
            effects.append(("SI", "read_write"))
        elif base_mnemonic.startswith(("STOS", "SCAS", "INS")):
            effects.append(("DI", "read_write"))

        if base_mnemonic.startswith("LODS"):
            effects.append(("AL" if width == 8 else "AX", "write"))
        elif base_mnemonic.startswith(("STOS", "SCAS")):
            effects.append(("AL" if width == 8 else "AX", "read"))
        if base_mnemonic.startswith(("INS", "OUTS")):
            effects.append(("DX", "read"))
        if separator:
            effects.append(("CX", "read_write"))
        return effects

    if mnemonic not in {"MUL", "IMUL", "DIV", "IDIV"}:
        return []
    if len(operands) != 1:
        return []
    register_match = _DIRECT_REGISTER_OPERAND.fullmatch(operands[0])
    if register_match is not None:
        operand_register = register_match.group(1)
        operand_width = _REGISTER_STORAGE[operand_register][2]
    else:
        width_match = re.match(r"^(BYTE|WORD)\s+PTR\b", operands[0])
        if width_match is None:
            return []
        operand_width = 8 if width_match.group(1) == "BYTE" else 16

    if mnemonic in {"MUL", "IMUL"}:
        if operand_width == 8:
            return [("AL", "read"), ("AX", "write")]
        return [("AX", "read_write"), ("DX", "write")]
    if operand_width == 8:
        return [("AX", "read_write")]
    return [("AX", "read_write"), ("DX", "read_write")]


def _condition_flag_effects(
    mnemonic: str, operands: list[str]
) -> list[tuple[str, str]]:
    if mnemonic == "LAHF":
        return [(flag, "read") for flag, _ in _LAHF_SAHF_BITS]
    if mnemonic == "SAHF":
        return [(flag, "write") for flag, _ in _LAHF_SAHF_BITS]

    string_compare_effects = _string_compare_flag_effects(mnemonic)
    if string_compare_effects is not None:
        return string_compare_effects

    effects = [
        (flag, "read")
        for flag in _CONDITION_FLAG_READS.get(mnemonic, ())
    ]
    if mnemonic in {"ADC", "SBB", "CMC"}:
        effects.append(("CF", "read"))

    shift_rotate_effects = _shift_rotate_flag_effects(mnemonic, operands)
    if shift_rotate_effects is not None:
        return [*effects, *shift_rotate_effects]

    if mnemonic in {"MUL", "IMUL"}:
        effects.extend((flag, "write") for flag in ("CF", "OF"))
        effects.extend(
            (flag, "clobber") for flag in ("AF", "PF", "SF", "ZF")
        )
    elif mnemonic in {"DIV", "IDIV"}:
        effects.extend((flag, "clobber") for flag in _STATUS_FLAGS)
    elif mnemonic in _ALL_STATUS_FLAG_WRITES:
        effects.extend((flag, "write") for flag in _STATUS_FLAGS)
    elif mnemonic in _LOGICAL_STATUS_FLAG_WRITES:
        effects.extend(
            (flag, "write")
            for flag in ("CF", "OF", "PF", "SF", "ZF")
        )
        effects.append(("AF", "clobber"))
    elif mnemonic in _PARTIAL_STATUS_FLAG_WRITES:
        effects.extend(
            (flag, "write")
            for flag in ("AF", "OF", "PF", "SF", "ZF")
        )
    elif mnemonic in {"CLC", "STC", "CMC"}:
        effects.append(("CF", "write"))

    return effects


def _flag_register_transfers(
    mnemonic: str,
) -> list[tuple[str, int, str]]:
    if mnemonic == "LAHF":
        direction = "flag_to_register"
    elif mnemonic == "SAHF":
        direction = "register_to_flag"
    else:
        return []
    return [
        (flag, register_bit, direction)
        for flag, register_bit in _LAHF_SAHF_BITS
    ]


def _string_compare_flag_effects(
    mnemonic: str,
) -> list[tuple[str, str]] | None:
    base_mnemonic, separator, repeat_prefix = mnemonic.partition(".")
    if base_mnemonic not in {"CMPSB", "CMPSW", "SCASB", "SCASW"}:
        return None

    if separator:
        if repeat_prefix not in {"REP", "REPE", "REPZ", "REPNE", "REPNZ"}:
            return None
        access = "read_write"
    else:
        access = "write"
    return [(flag, access) for flag in _STATUS_FLAGS]


def _shift_rotate_flag_effects(
    mnemonic: str, operands: list[str]
) -> list[tuple[str, str]] | None:
    shifts = {"SAL", "SAR", "SHL", "SHR"}
    rotates = {"RCL", "RCR", "ROL", "ROR"}
    if mnemonic not in shifts | rotates:
        return None

    count = _immediate_shift_count(operands)
    if count == 0:
        return []
    if mnemonic in shifts:
        if count is None:
            return [(flag, "read_write") for flag in _STATUS_FLAGS]
        effects = [
            (flag, "write") for flag in ("CF", "PF", "SF", "ZF")
        ]
        effects.extend(
            (("AF", "clobber"), ("OF", "write" if count == 1 else "clobber"))
        )
        return effects

    carry_access = (
        "read_write"
        if mnemonic in {"RCL", "RCR"} or count is None
        else "write"
    )
    overflow_access = (
        "write" if count == 1 else "clobber" if count is not None else "read_write"
    )
    return [("CF", carry_access), ("OF", overflow_access)]


def _immediate_shift_count(operands: list[str]) -> int | None:
    if len(operands) != 2:
        return None
    count_operand = operands[1]
    if re.fullmatch(r"0X[0-9A-F]+", count_operand):
        return int(count_operand, 16)
    if count_operand.isdecimal():
        return int(count_operand)
    return None


def _ranges_overlap(
    first_offset: int,
    first_width: int,
    second_offset: int,
    second_width: int,
) -> bool:
    return max(first_offset, second_offset) < min(
        first_offset + first_width,
        second_offset + second_width,
    )


def _register_storage_ranges(
    register_bits: set[tuple[str, int]],
) -> list[dict[str, int | str]]:
    ranges = []
    by_family: dict[str, list[int]] = defaultdict(list)
    for family, bit in register_bits:
        by_family[family].append(bit)
    for family, bits in sorted(by_family.items()):
        ordered_bits = sorted(set(bits))
        start = previous = ordered_bits[0]
        for bit in ordered_bits[1:]:
            if bit == previous + 1:
                previous = bit
                continue
            ranges.append(
                {"family": family, "start_bit": start, "end_bit": previous + 1}
            )
            start = previous = bit
        ranges.append(
            {"family": family, "start_bit": start, "end_bit": previous + 1}
        )
    return ranges


def _parse_frame_displacement(match: re.Match[str]) -> int:
    sign, raw_value = match.groups()
    if raw_value is None:
        return 0
    unsigned_value = raw_value.removeprefix("-")
    base = 16 if unsigned_value.startswith("0X") else 10
    magnitude = int(raw_value, base)
    if sign == "-":
        return -magnitude
    if sign == "+" and magnitude < 0:
        return magnitude
    if sign == "+" and magnitude >= 0x8000:
        return magnitude - 0x10000
    return magnitude
