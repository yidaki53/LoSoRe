"""asmcfg.py — 16-bit real-mode assembly CFG utilities (Ghidra .s dialect).

Shared by the scoring harness (tools/e6_match.py) and the chunked
decompilation tool (tools/chunk_decomp.py) so there is exactly one
definition of "block", "edge" and "loop" in this repository.

Address model
-------------
Ghidra prints real-mode addresses as `SEG:OFF` (e.g. `0x1000:5e9a`).  The
flat address used throughout this module is ``seg * 16 + off`` (0x15e9a).
"""
from __future__ import annotations

import collections
import re

_BRANCH = re.compile(
    r"^(JMP|J[ACEGLONPSZB]|LOOP(?:NE|NZ|E|Z)?(?=\s|$)|JCXZ|JECXZ)"
)
_COND = re.compile(
    r"^(J[ACEGLONPSZB]|LOOP(?:NE|NZ|E|Z)?(?=\s|$)|JCXZ|JECXZ)"
)
_CALL = re.compile(r"^(CALL|CALLF)")
_FAR_TRANSFER = re.compile(r"^(?:CALLF|JMPF)\b")
_RET = re.compile(r"^(RET|IRET|RETW|RETF)")

# Instructions that write their first operand (used by chunk def/use).
_WRITES_FIRST = re.compile(
    r"^(MOV|LEA|LES|LDS|POP|ADD|ADC|SUB|SBB|AND|OR|XOR|INC|DEC|NEG|NOT|SHL|SHR|SAR|"
    r"IMUL|MUL|IDIV|DIV|XCHG|CMP|CLC|STC|CLD|STD|CWD|CBW|IN|OUT|PUSH)$")
# Instructions that only read their operands.
_READS_ONLY = re.compile(r"^(CMP|TEST|J[A-Z]+|LOOP|PUSH)$")


def is_branch(inst: str) -> bool:
    return bool(_BRANCH.match(inst))


def is_cond_branch(inst: str) -> bool:
    return bool(_COND.match(inst))


def is_call(inst: str) -> bool:
    return bool(_CALL.match(inst))


def is_ret(inst: str) -> bool:
    return bool(_RET.match(inst))


def branch_target(inst: str) -> int | None:
    """Resolve a direct branch/call operand to a flat address, or None.

    Ghidra .s uses ``0xSEG:OFF``; objdump-style output uses a plain
    absolute address.  Instruction text reaches this function upper-cased
    in the Ghidra path, so ``0X`` must be accepted as well. Memory-indirect
    operands do not identify their runtime target.
    """
    if "[" in inst:
        return None
    m = re.search(r"0X?([0-9A-F]{1,4}):([0-9A-F]{1,4})", inst)
    if m:
        return int(m.group(1), 16) * 16 + int(m.group(2), 16)
    m = re.search(r"0X([0-9A-F]+)", inst)
    if m:
        try:
            return int(m.group(1), 16)
        except ValueError:
            return None
    return None


def resolve_branch_target(
    inst: str, source_segment: int | None = None
) -> int | None:
    """Resolve a direct transfer, applying 16-bit IP wrapping to near targets."""
    target = branch_target(inst)
    if target is None or source_segment is None or _FAR_TRANSFER.match(inst):
        return target
    if not re.search(r"0X?[0-9A-F]{1,4}:[0-9A-F]{1,4}", inst):
        return target
    segment_base = source_segment * 16
    target_offset = (target - segment_base) & 0xFFFF
    return segment_base + target_offset


def parse_ghidra_asm(text: str) -> dict:
    """Parse a Ghidra ``.s`` listing into parallel address/instruction lists."""
    addrs: list[int] = []
    segments: list[int] = []
    insts: list[str] = []
    raw: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        m = re.match(r"^([0-9a-fA-F]{4}):([0-9a-fA-F]{4})\s+(.+)$", line)
        if not m:
            continue
        segment = int(m.group(1), 16)
        offset = int(m.group(2), 16)
        segments.append(segment)
        addrs.append(segment * 16 + offset)
        insts.append(m.group(3).upper())
        raw.append(line)
    return {"addrs": addrs, "segments": segments, "insts": insts, "raw": raw}


def build_blocks(
    addrs: list[int],
    insts: list[str],
    source_segments: list[int | None] | None = None,
) -> dict:
    """Partition instructions into basic blocks and wire up the block graph.

    Leaders are: instruction 0, the instruction after any branch/call/ret,
    and every branch target that resolves inside the listing.
    """
    n = len(insts)
    if source_segments is None:
        source_segments = [None] * n
    elif len(source_segments) != n:
        raise ValueError("source_segments must match the instruction count")
    if n == 0:
        # Empty listing (a bare INCLUDE_ASM stub, e.g. FUN_2971_65df.s is a
        # single comment line): no blocks to build; callers diff against an
        # empty CFG.  Without this guard the phantom block below indexes
        # insts[-1] and raises IndexError.
        return {
            "addrs": addrs,
            "segments": source_segments,
            "insts": insts,
            "n": 0,
            "idx": {},
            "leaders": [],
            "block_of": [],
            "nblocks": 0,
            "start": [],
            "end": [],
            "size": [],
            "succ": [],
            "pred": [],
            "calls": 0,
            "rets": 0,
            "cond_edges": 0,
        }
    idx = {a: i for i, a in enumerate(addrs)}
    leader = {0}
    for i, inst in enumerate(insts):
        if is_branch(inst) or is_call(inst) or is_ret(inst):
            if i + 1 < n:
                leader.add(i + 1)
            t = resolve_branch_target(inst, source_segments[i])
            if t is not None and t in idx:
                leader.add(idx[t])
    leaders = sorted(leader)

    block_of = [0] * n
    bid = 0
    li = 0
    for i in range(n):
        if li + 1 < len(leaders) and i == leaders[li + 1]:
            bid += 1
            li += 1
        block_of[i] = bid
    nblocks = bid + 1

    # leaders[j] is the first instruction of block j; the block ends just
    # before the next leader (or at the end of the listing).
    start = list(leaders)
    end = [(leaders[j + 1] - 1) if j + 1 < len(leaders) else n - 1
           for j in range(nblocks)]
    size = [end[b] - start[b] + 1 for b in range(nblocks)]

    succ: list[set[int]] = [set() for _ in range(nblocks)]
    pred: list[set[int]] = [set() for _ in range(nblocks)]
    calls = 0
    rets = 0
    cond_edges = 0
    for b in range(nblocks):
        last = insts[end[b]]
        # Fall-through: the next block is reached unless this block ends in
        # an unconditional transfer of control.
        if not is_ret(last) and not (is_branch(last) and not is_cond_branch(last)):
            if end[b] + 1 < n:
                nb = block_of[end[b] + 1]
                succ[b].add(nb)
                pred[nb].add(b)
    for i, inst in enumerate(insts):
        if not (is_branch(inst) or is_call(inst) or is_ret(inst)):
            continue
        b = block_of[i]
        t = resolve_branch_target(inst, source_segments[i])
        if t is not None and t in idx:
            tb = block_of[idx[t]]
            succ[b].add(tb)
            pred[tb].add(b)
            if is_cond_branch(inst):
                cond_edges += 1
        if is_call(inst):
            calls += 1
        if is_ret(inst):
            rets += 1
    return {
        "addrs": addrs, "segments": source_segments, "insts": insts,
        "n": n, "idx": idx,
        "leaders": leaders, "block_of": block_of, "nblocks": nblocks,
        "start": start, "end": end, "size": size,
        "succ": succ, "pred": pred,
        "calls": calls, "rets": rets, "cond_edges": cond_edges,
    }


def cfg_stats(blocks: dict) -> dict:
    """Summary numbers used by the scoring harness."""
    edges = sum(len(s) for s in blocks["succ"])
    return {
        "blocks": blocks["nblocks"],
        "edges": edges,
        "cond": blocks["cond_edges"],
        "call": blocks["calls"],
        "ret": blocks["rets"],
        "sizes": blocks["size"],
    }


def parse_slots(inst: str) -> list[str]:
    """Stack-slot operands of an instruction, as canonical offset strings.

    Ghidra prints frame slots as ``[BP + 0xfed4]`` or ``[BP + -0x2]``.
    Both denote a slot at ``BP - 0x12c`` and ``BP - 0x2`` respectively
    (Ghidra's own naming: ``local_12c``).  We normalise every slot to its
    distance below BP so that the two spellings compare equal.
    """
    out = []
    for m in re.finditer(r"\[BP\s*([+-])\s*(0[xX][0-9a-fA-F]+|\d+)\]", inst):
        sign, num = m.group(1), m.group(2)
        val = int(num, 16) if num[:2].lower() == "0x" else int(num)
        # A positive displacement is a 16-bit wrap of a negative offset.
        if sign == "+" and val >= 0x8000:
            val -= 0x10000
        if sign == "-":
            val = -val
        out.append(f"-{abs(val):x}")
    return out


def _split_operands(inst: str) -> tuple[str, list[str]]:
    """(mnemonic, operand list) for a Ghidra instruction."""
    parts = inst.split(None, 1)
    op = parts[0].upper() if parts else ""
    ops = [o.strip() for o in parts[1].split(",")] if len(parts) > 1 else []
    return op, ops


def _read_write(inst: str) -> tuple[set[str], set[str]]:
    """(read slots, written slots) for one instruction.

    A pure store (``MOV [BP-x],AX``) writes the slot without reading it.
    A read-modify-write (``ADD [BP-x],1``) both reads and writes it.
    """
    op, ops = _split_operands(inst)
    if not ops:
        return set(), set()
    dest_is_mem = "[" in ops[0]
    dest_slots = set(parse_slots(ops[0])) if dest_is_mem else set()
    if op in ("MOV", "LEA", "POP", "LES", "LDS"):
        if dest_is_mem:
            return set(), dest_slots
        # register destination: the memory source is read
        src = ops[-1] if len(ops) > 1 else ""
        return set(parse_slots(src)), set()
    if op in ("CMP", "TEST"):
        return set(parse_slots(" ".join(ops))), set()
    if op in ("XCHG",):
        return set(parse_slots(" ".join(ops))), set(parse_slots(" ".join(ops)))
    allslots = set(parse_slots(" ".join(ops)))
    return allslots, allslots


def live_slots(blocks: dict) -> dict:
    """Backward liveness over frame slots.

    Returns a dict with, for every block, the slots live on entry
    (``live_in``) and on exit (``live_out``).  Only BP-relative slots are
    tracked: registers are re-materialised by the Pascal compiler, and
    absolute addresses are global (they need no parameter threading).
    """
    n = blocks["nblocks"]
    insts = blocks["insts"]
    start, end = blocks["start"], blocks["end"]
    use: list[set[str]] = []
    def_: list[set[str]] = []
    for b in range(n):
        u: set[str] = set()
        d: set[str] = set()
        for i in range(start[b], end[b] + 1):
            inst = insts[i]
            r, w = _read_write(inst)
            u |= (r - d)
            d |= w
        use.append(u)
        def_.append(d)

    succ = blocks["succ"]
    live_in: list[set[str]] = [set() for _ in range(n)]
    live_out: list[set[str]] = [set() for _ in range(n)]
    changed = True
    rounds = 0
    while changed and rounds < 10000:
        changed = False
        rounds += 1
        for b in reversed(range(n)):
            out: set[str] = set()
            for s in succ[b]:
                out |= live_in[s]
            new_in = use[b] | (out - def_[b])
            if out != live_out[b] or new_in != live_in[b]:
                live_out[b] = out
                live_in[b] = new_in
                changed = True
    return {
        "use": use, "def": def_, "live_in": live_in, "live_out": live_out,
        "rounds": rounds,
    }


def sccs(blocks: dict) -> list[list[int]]:
    """Strongly connected components (iterative Kosaraju).

    Each SCC with more than one block is a loop region; a single-block
    SCC is a self-loop or a plain block.  The condensation of the CFG
    (the SCC DAG) is exactly the loop-nesting hierarchy we need.
    """
    n = blocks["nblocks"]
    succ = blocks["succ"]
    pred = blocks["pred"]

    # Pass 1: iterative DFS recording finish order.
    order: list[int] = []
    visited = [False] * n
    for root in range(n):
        if visited[root]:
            continue
        visited[root] = True
        stack = [(root, iter(sorted(succ[root])))]
        while stack:
            node, it = stack[-1]
            advanced = False
            for w in it:
                if not visited[w]:
                    visited[w] = True
                    stack.append((w, iter(sorted(succ[w]))))
                    advanced = True
                    break
            if not advanced:
                order.append(stack.pop()[0])

    # Pass 2: process in reverse finish order over the reversed graph.
    comp = [-1] * n
    groups: list[list[int]] = []
    for root in reversed(order):
        if comp[root] != -1:
            continue
        cid = len(groups)
        stack = [root]
        comp[root] = cid
        group: list[int] = []
        while stack:
            x = stack.pop()
            group.append(x)
            for w in pred[x]:
                if comp[w] == -1:
                    comp[w] = cid
                    stack.append(w)
        groups.append(sorted(group))
    return groups


def dominators(blocks: dict) -> list[set[int]]:
    """Iterative dominator sets (Cooper/Harvey/Kennedy) over the block CFG.

    ``dom[b]`` is the set of blocks every path from the entry to ``b``
    passes through.  The entry block dominates itself.
    """
    n = blocks["nblocks"]
    succ = blocks["succ"]
    pred = blocks["pred"]
    order: list[int] = []
    seen = [False] * n
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        stack = [(root, iter(sorted(succ[root])))]
        while stack:
            node, it = stack[-1]
            advanced = False
            for w in it:
                if not seen[w]:
                    seen[w] = True
                    stack.append((w, iter(sorted(succ[w]))))
                    advanced = True
                    break
            if not advanced:
                order.append(stack.pop()[0])
    rpo = list(reversed(order))
    rpo_num = {b: i for i, b in enumerate(rpo)}

    dom = [set(range(n)) for _ in range(n)]
    dom[0] = {0}
    changed = True
    while changed:
        changed = False
        for b in rpo:
            if b == 0:
                continue
            new = set(range(n))
            for p in pred[b]:
                if p in rpo_num:
                    new &= dom[p]
            new.add(b)
            if new != dom[b]:
                dom[b] = new
                changed = True
    return dom


def find_loops(blocks: dict) -> list[dict]:
    """Natural loops, one entry per loop head.

    Loops are derived from the CFG's strongly connected components: a
    backward branch only counts as a loop back edge when its head and its
    latch lie on the same cycle.  This keeps spurious backward jumps
    (e.g. tail jumps at the end of a function) from swallowing the whole
    function, while still reporting one loop per head so nested loops keep
    their parent/child relationship through ``loop_nesting``.

    The body of a loop is the set of blocks in the cycle that can reach a
    latch without passing through the head -- the standard definition.
    """
    addrs = blocks["addrs"]
    insts = blocks["insts"]
    idx = blocks["idx"]
    block_of = blocks["block_of"]
    pred = blocks["pred"]

    # Block -> id of the SCC it belongs to, plus the block set of each SCC.
    scc_of: dict[int, int] = {}
    scc_blocks: list[set[int]] = []
    for cid, group in enumerate(sccs(blocks)):
        scc_blocks.append(set(group))
        for b_ in group:
            scc_of[b_] = cid

    by_head: dict[int, dict] = {}
    for i, inst in enumerate(insts):
        if not is_branch(inst):
            continue
        t = resolve_branch_target(inst, blocks["segments"][i])
        if t is None or t not in idx:
            continue
        j = idx[t]
        if j > i:
            continue
        head = block_of[j]
        latch = block_of[i]
        # A genuine loop back edge stays on a single cycle (same SCC).
        if scc_of[head] != scc_of[latch]:
            continue
        body = {head, latch}
        stack = [latch]
        while stack:
            x = stack.pop()
            for p in pred[x]:
                if p not in body and p != head:
                    body.add(p)
                    stack.append(p)
        # Confine the body to the cycle the head/latch live on.
        body &= scc_blocks[scc_of[head]]
        if head not in by_head:
            by_head[head] = {
                "head": head,
                "latches": {latch},
                "body": body,
                "head_addr": addrs[blocks["start"][head]],
            }
        else:
            lp = by_head[head]
            lp["latches"].add(latch)
            lp["body"] |= body

    loops = []
    for head, lp in by_head.items():
        body = lp["body"]
        loops.append({
            "head": head,
            "latches": lp["latches"],
            "body": body,
            "blocks": len(body),
            "instrs": sum(blocks["size"][b] for b in body),
            "head_addr": lp["head_addr"],
        })
    loops.sort(key=lambda lp: -lp["instrs"])
    return loops


def loop_nesting(loops: list[dict], blocks: dict) -> list[dict]:
    """Annotate each loop with its parent and its *residual* size.

    A loop's parent is the innermost loop whose head dominates this
    loop's head -- plain block-set containment is not enough, because two
    sibling loops can share blocks without one nesting inside the other.

    ``residual`` counts the instructions of this loop that are not
    covered by a nested loop.  That is how much code the decompiler
    actually has to write at this level, and therefore how big the
    prompt for this level has to be.
    """
    n = len(loops)
    dom = dominators(blocks)
    parent: list[int | None] = [None] * n
    for i, lp in enumerate(loops):
        best = None
        for j, lq in enumerate(loops):
            if i == j or lq["head"] == lp["head"]:
                continue
            if lq["head"] not in dom[lp["head"]]:
                continue
            if best is None or lq["instrs"] < loops[best]["instrs"]:
                best = j
        parent[i] = best

    out = []
    for i, lp in enumerate(loops):
        lp = dict(lp)
        lp["parent"] = parent[i]
        covered: set[int] = set()
        for j in range(n):
            if parent[j] == i:
                covered |= loops[j]["body"]
        lp["residual"] = sum(blocks["size"][b] for b in lp["body"] - covered)
        out.append(lp)
    return out


def region_tree(blocks: dict) -> dict:
    """Decompose a function into a hierarchy of regions.

    The function is split into

      * ``loop`` regions -- one per natural loop, and
      * ``code`` regions -- the straight-line code that sits between the
        loops, at each level of nesting.

    Every region records the blocks it contains, how many instructions
    that is, its parent region and its child regions.  The result covers
    the whole function exactly once, which is what lets a decompiler work
    on a 4000-instruction routine one manageable region at a time.
    """
    loops = loop_nesting(find_loops(blocks), blocks)
    n = len(loops)

    # Innermost owning loop for every block.
    owner: dict[int, int] = {}
    for i, lp in enumerate(loops):
        for b in lp["body"]:
            if b not in owner or lp["instrs"] < loops[owner[b]]["instrs"]:
                owner[b] = i

    children: list[list[int]] = [[] for _ in loops]
    for i, lp in enumerate(loops):
        if lp["parent"] is not None:
            children[lp["parent"]].append(i)

    regions: list[dict] = []
    for i, lp in enumerate(loops):
        nested: set[int] = set()
        for j in children[i]:
            nested |= loops[j]["body"]
        mine = lp["body"] - nested
        for run in _contiguous_runs(mine):
            regions.append({
                "kind": "code",
                "loop": i,
                "blocks": run,
                "instrs": sum(blocks["size"][b] for b in run),
                "parent": ("loop", i),
                "children": [],
            })
        regions.append({
            "kind": "loop",
            "loop": i,
            "head": lp["head"],
            "latches": sorted(lp["latches"]),
            "blocks": lp["body"],
            "instrs": lp["instrs"],
            "residual": lp["residual"],
            "parent": (("loop", lp["parent"]) if lp["parent"] is not None
                       else ("function", None)),
            "children": [],
        })
    return {"loops": loops, "regions": regions, "owner": owner,
            "nloops": n}


def _contiguous_runs(blocks_set: set[int]) -> list[list[int]]:
    """Split a set of block ids into maximal runs of consecutive ids."""
    if not blocks_set:
        return []
    out: list[list[int]] = []
    cur: list[int] = []
    for b in sorted(blocks_set):
        if cur and b == cur[-1] + 1:
            cur.append(b)
        else:
            if cur:
                out.append(cur)
            cur = [b]
    if cur:
        out.append(cur)
    return out
