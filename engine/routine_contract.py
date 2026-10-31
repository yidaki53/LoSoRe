"""Load small, reviewed routine contracts shared by drafting and probes."""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any


class RoutineContractError(ValueError):
    """A checked routine contract is missing or internally inconsistent."""


def load_contracts(path: pathlib.Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RoutineContractError(f"could not read routine contracts: {path}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise RoutineContractError(f"unsupported routine contract file: {path}")
    functions = data.get("functions")
    if not isinstance(functions, dict):
        raise RoutineContractError(f"routine contract functions must be an object: {path}")
    contracts: dict[str, dict[str, Any]] = {}
    for name, contract in functions.items():
        if not isinstance(name, str) or not isinstance(contract, dict):
            raise RoutineContractError(f"invalid routine contract entry: {path}")
        declaration = contract.get("declaration")
        if not isinstance(declaration, str) or not _declaration_matches(
            declaration, name
        ):
            raise RoutineContractError(
                f"{name}: checked declaration is missing or names another routine"
            )
        prompt = contract.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise RoutineContractError(f"{name}: contract prompt must be non-empty")
        for field in ("instruction_semantics", "fixture_flag_table"):
            value = contract.get(field)
            if value is not None and (
                not isinstance(value, str) or not value.strip()
            ):
                raise RoutineContractError(
                    f"{name}: {field} must be a non-empty string"
                )
        repair_region = contract.get("localized_repair_region")
        if repair_region is not None and (
            not isinstance(repair_region, dict)
            or any(
                not isinstance(repair_region.get(field), str)
                or not repair_region[field].strip()
                or "\n" in repair_region[field]
                or "\r" in repair_region[field]
                for field in ("start", "end")
            )
        ):
            raise RoutineContractError(
                f"{name}: invalid localized repair region"
            )
        if not isinstance(contract.get("oracle"), str):
            raise RoutineContractError(f"{name}: oracle id must be a string")
        arguments = contract.get("arguments", [])
        if not isinstance(arguments, list) or any(
            not isinstance(argument, dict)
            or any(
                not isinstance(argument.get(field), str)
                or not argument[field].strip()
                for field in ("name", "role", "representation")
            )
            for argument in arguments
        ):
            raise RoutineContractError(f"{name}: invalid argument contract")
        memory_model = contract.get("memory_model")
        if memory_model is not None and not isinstance(memory_model, str):
            raise RoutineContractError(f"{name}: memory model must be a string")
        observed_outputs = contract.get("observed_outputs", [])
        if not isinstance(observed_outputs, list) or any(
            not isinstance(output, str) or not output.strip()
            for output in observed_outputs
        ):
            raise RoutineContractError(f"{name}: invalid observed outputs")
        contracts[name] = contract
    return contracts


def load_contract(
    target_root: pathlib.Path, function_name: str
) -> dict[str, Any] | None:
    contracts_path = target_root / "config" / "routine_contracts.json"
    return load_contracts(contracts_path).get(function_name)


def pascal_declaration(source: str, function_name: str) -> str | None:
    for line in source.splitlines():
        if line.lstrip().startswith("//"):
            continue
        if _declaration_matches(line.strip(), function_name):
            return line.strip()
    return None


def _declaration_matches(declaration: str, function_name: str) -> bool:
    return bool(
        re.match(
            rf"^(?:procedure|function)\s+{re.escape(function_name)}\b[^;]*;\s*$",
            declaration.strip(),
            re.IGNORECASE,
        )
    )
