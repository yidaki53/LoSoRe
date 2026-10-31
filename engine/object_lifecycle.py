"""Restricted static oracle for Liero input-open, close and input method effects."""

from __future__ import annotations

from dataclasses import dataclass, replace

from engine.alternate_streams import _mz_relocation_locations
from engine.callbacks import _bound_region

_INPUT_STREAMS = {
    "input_entry": (0x36B7, "bab1d7 eb08"),
    "open": (
        0x36C4,
        """
        55 8bec c47e06 268b4502 3db1d7 7412 3db2d7 740d 3db0d7 7410
        c70610646600 eb24 52 06 57 0e e82500 5a 33c0 26895502
        26894508 2689450a bb1000 e84c00 7406 26c74502b0d7 5d ca0400
    """,
    ),
    "close": (
        0x3711,
        """
        b001 55 8bec c47e06 26817d02b1d7 7418 26817d02b2d7 7408
        c70610646700 eb18 50 bb1400 e81500 58 0ac0 740c bb1c00
        e80a00 26c74502b0d7 5d ca0400
    """,
    ),
    "dispatch": (0x374D, "06 57 06 57 26ff19 0bc0 7403 a31064 5f 07 c3"),
    "read_handler": (
        0x375E,
        """
        8bdc 1e 36c47f04 26c5550c 268b4d04 268b1d b43f cd21 7210
        2689450a 33c0 26c745080000 1f ca0400 26c7450a0000 ebee
    """,
    ),
    "close_handler": (
        0x37D3,
        """
        8bdc 36c47f04 268b1d 83fb04 7606 b43e cd21 7202 33c0 ca0400
    """,
    ),
}


@dataclass(frozen=True)
class _State:
    """Oracle: finite wrapper state; method effects are separately checked summaries."""

    pc: int
    mode: int
    methods: tuple[tuple[str, str], ...]
    ax: int | None = None
    bx: int | None = None
    zero: bool | None = None
    status: str = "incoming"
    calls: tuple[str, ...] = ()
    method_returns: tuple[str, ...] = ()
    resets: tuple[str, ...] = ()


def _streams(regions: dict, binary: bytes, header: int, load_segment: int) -> dict:
    """Oracle: fixed-entry exact instructions and absence of loader code rewrites."""
    if not isinstance(regions, dict) or set(regions) != set(_INPUT_STREAMS):
        raise ValueError("input lifecycle requires all reviewed regions")
    result = {}
    occupied = set()
    segment_base = ((load_segment + 0x14DD) & 0xFFFF) * 16
    for name, (entry, template) in _INPUT_STREAMS.items():
        address, data = _bound_region(regions[name], binary, header, load_segment * 16)
        tokens = [bytes.fromhex(raw) for raw in template.split()]
        if address != segment_base + entry or data != b"".join(tokens):
            raise ValueError(f"region disagrees with reviewed input lifecycle {name}")
        instructions = {}
        cursor = address
        for raw in tokens:
            instructions[cursor] = raw
            cursor += len(raw)
        if cursor > segment_base + 0x10000:
            raise ValueError("input lifecycle crosses code segment")
        offset = header + address - load_segment * 16
        occupied.update(range(offset, offset + len(data)))
        result[name] = instructions
    if any(
        location in occupied or location + 1 in occupied
        for location in _mz_relocation_locations(binary, header)
    ):
        raise ValueError("input lifecycle has an unexpected relocation")
    boundaries = {site for stream in result.values() for site in stream}
    for stream in result.values():
        for site, raw in stream.items():
            if raw[0] in {0x72, 0x74, 0x76, 0xEB, 0xE8}:
                target = (
                    site + len(raw) + int.from_bytes(raw[1:], "little", signed=True)
                )
                if target not in boundaries:
                    raise ValueError("input lifecycle edge misses a reviewed boundary")
    return result


def _method_call(state: _State, setup_outcomes: list[dict]) -> list[_State]:
    """Oracle: setup return alternatives or slot-preserving DOS close summary."""
    if state.bx == 0x10:
        result = []
        for outcome in setup_outcomes:
            methods = dict(state.methods)
            methods.update(outcome["method_slots"])
            success = outcome["writes_methods"]
            result.append(
                replace(
                    state,
                    mode=int(outcome["resulting_mode"], 16),
                    methods=tuple(sorted(methods.items())),
                    ax=0 if success else None,
                    zero=success,
                    status=state.status if success else "setup_error",
                    calls=(*state.calls, "setup:0x10"),
                    method_returns=(
                        *state.method_returns,
                        "setup:zero" if success else "setup:nonzero",
                    ),
                )
            )
        return result
    if state.bx == 0x1C:
        return [
            replace(
                state,
                ax=0 if success else None,
                zero=success,
                status=state.status if success else "close_error",
                calls=(*state.calls, "close:0x1c"),
                method_returns=(
                    *state.method_returns,
                    "close:zero" if success else "close:nonzero",
                ),
            )
            for success in (True, False)
        ]
    raise ValueError("input lifecycle reached an unmodeled method slot")


def _walk(
    name: str,
    initial: _State,
    streams: dict,
    setup_outcomes: list[dict],
    requested_mode: int,
) -> list[_State]:
    """Oracle: all local wrapper branches under explicit method-return summaries."""
    instructions = streams[name]
    pending = [replace(initial, pc=min(instructions))]
    returns = []
    while pending:
        state = pending.pop()
        raw = instructions[state.pc]
        successor = state.pc + len(raw)
        next_states = [state]
        if raw == b"\x26\x8b\x45\x02":
            next_states = [replace(state, ax=state.mode)]
        elif raw[0] == 0x3D:
            next_states = [
                replace(state, zero=state.ax == int.from_bytes(raw[1:], "little"))
            ]
        elif raw[:4] == b"\x26\x81\x7d\x02":
            next_states = [
                replace(state, zero=state.mode == int.from_bytes(raw[4:], "little"))
            ]
        elif raw == b"\xb0\x01":
            next_states = [replace(state, ax=1)]
        elif raw == b"\x0a\xc0":
            if state.ax is None:
                raise ValueError("input lifecycle has unknown AL at close decision")
            next_states = [replace(state, zero=(state.ax & 0xFF) == 0)]
        elif raw == b"\x33\xc0":
            next_states = [replace(state, ax=0, zero=True)]
        elif raw[0] == 0xBB:
            next_states = [replace(state, bx=int.from_bytes(raw[1:], "little"))]
        elif raw[:4] == b"\xc7\x06\x10\x64":
            next_states = [
                replace(state, status=f"0x{int.from_bytes(raw[4:], 'little'):04x}")
            ]
        elif raw == b"\x26\x89\x55\x02":
            next_states = [replace(state, mode=requested_mode)]
        elif raw[:3] == b"\x26\xc7\x45" and raw[3] == 2:
            next_states = [replace(state, mode=int.from_bytes(raw[4:], "little"))]
        elif raw in {b"\x26\x89\x45\x08", b"\x26\x89\x45\x0a"}:
            if state.ax != 0:
                raise ValueError("input lifecycle buffer reset is not zero")
            next_states = [replace(state, resets=(*state.resets, f"0x{raw[3]:x}"))]
        elif raw[0] == 0xE8:
            target = successor + int.from_bytes(raw[1:], "little", signed=True)
            if target == min(streams["close"]) and name == "open":
                next_states = _walk(
                    "close", state, streams, setup_outcomes, requested_mode
                )
            elif target == min(streams["dispatch"]):
                next_states = _method_call(state, setup_outcomes)
            else:
                raise ValueError("input lifecycle reached an unmodeled call")
        elif raw[0] in {0x74, 0xEB}:
            if raw[0] == 0x74 and state.zero is None:
                raise ValueError("input lifecycle branch condition is unknown")
            if raw[0] == 0xEB or state.zero:
                successor += int.from_bytes(raw[1:], "little", signed=True)
        elif raw[0] == 0xCA:
            returns.append(state)
            continue
        elif raw not in {
            b"\x55",
            b"\x8b\xec",
            b"\xc4\x7e\x06",
            b"\x52",
            b"\x06",
            b"\x57",
            b"\x0e",
            b"\x5a",
            b"\x5d",
        }:
            raise ValueError("input lifecycle wrapper instruction is not modeled")
        pending.extend(replace(item, pc=successor) for item in next_states)
    return returns


def _rows(states: list[_State]) -> list[dict]:
    """Oracle: retain each normal-return path, including sticky failure status."""
    return [
        {
            "mode": f"0x{state.mode:04x}",
            "method_slots": dict(state.methods),
            "status": state.status,
            "calls": list(state.calls),
            "method_returns": list(state.method_returns),
            "buffer_resets": list(state.resets),
        }
        for state in states
    ]


def verify_input_lifecycle(
    regions: dict,
    binary: bytes,
    header: int,
    load_segment: int,
    setup: dict,
) -> dict:
    """Oracle: conditional closed/input lifecycle only, not global indirect coverage."""
    streams = _streams(regions, binary, header, load_segment)
    outcomes = setup["mode_outcomes"]["0xd7b1"]
    constructor_methods = tuple(sorted(setup["constructor_method_slots"].items()))
    (success,) = [outcome for outcome in outcomes if outcome["writes_methods"]]
    active_methods = dict(constructor_methods)
    active_methods.update(success["method_slots"])
    segment = (load_segment + 0x14DD) & 0xFFFF
    if (
        active_methods["0x14"] != f"0x{segment:04x}:375e"
        or active_methods["0x1c"] != f"0x{segment:04x}:37d3"
    ):
        raise ValueError("input setup method targets disagree with reviewed handlers")
    requested = int.from_bytes(
        next(iter(streams["input_entry"].values()))[1:], "little"
    )
    closed = _State(0, 0xD7B0, constructor_methods)
    active = _State(0, 0xD7B1, tuple(sorted(active_methods.items())))
    invalid = _State(0, 0xD7B3, active.methods)
    return {
        "analysis": "conditional_static_input_lifecycle",
        "streams": {
            name: {
                "entry": min(instructions),
                "byte_count": sum(map(len, instructions.values())),
                "instruction_count": len(instructions),
            }
            for name, instructions in streams.items()
        },
        "open_from_closed": _rows(_walk("open", closed, streams, outcomes, requested)),
        "reopen_from_input": _rows(_walk("open", active, streams, outcomes, requested)),
        "close_from_input": _rows(_walk("close", active, streams, outcomes, requested)),
        "open_from_invalid_mode": _rows(
            _walk("open", invalid, streams, outcomes, requested)
        ),
        "close_from_closed": _rows(
            _walk("close", closed, streams, outcomes, requested)
        ),
        "open_cleanup_bytes": int.from_bytes(
            list(streams["open"].values())[-1][1:], "little"
        ),
        "close_cleanup_bytes": int.from_bytes(
            list(streams["close"].values())[-1][1:], "little"
        ),
        "input_handler_method_slots_preserved": True,
        "read_handler_object_writes": ["0x8", "0xa"],
        "close_handler_object_writes": [],
        "dispatch_preserves_object_pointer": True,
        "resolves_call_sites": False,
        "assumptions": [
            "The same valid object is passed to the wrappers and their method calls.",
            "Setup slot 0x10 and active input/close slots still equal the checked setup values.",
            "DOS returns normally and preserves DS, ES, DI, BP, SS and live stack words.",
            "DOS open failures return nonzero AX error codes.",
            "Buffers, filename, status word and external writes do not alias method slots or stack.",
            "The constructor initializes the object before its first open.",
        ],
        "remaining_obligations": [
            "Prove slot continuity across the complete caller loops, callbacks and unknown callees.",
            "Output-mode close/flush and arbitrary user-replaced methods are outside this input proof.",
            "Observe actual DOS open/read/close results in the original executable.",
        ],
    }
