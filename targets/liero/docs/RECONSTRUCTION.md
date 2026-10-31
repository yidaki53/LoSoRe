# Liero source reconstruction status

## Current session checkpoint and next work

As of 2026-10-31, the latest shared-rule milestone is complete, with
**184 focused regression tests**, lint/syntax checks and replayed original
memory evidence. This count is not a fresh full-repository suite result.
The active limit is return/caller/ABI evidence, not compilation.

- Close/refill automatic trials meet a narrow developer-sketch PoC.
- The first constructor expansion failed; byte constraints later repaired
  the known slice without changing the historical failed trial.
- Global initializer `FUN_24dd_492c` now has bounded static write facts and
  three original-only guarded-memory measurements. `RET` remains residue;
  no Pascal parity, normal-program safety or new routine recovery follows.
- No generated body was installed or promoted by these recent trials.

Next resolve the 492c entry/return contract, then measure Pascal under those
same preconditions before a frozen one-slice portability evaluation.
See [persistent TODOs](../../../docs/RECOVERY_TODO.md) for dependencies,
acceptance checks and stop rules, and
[the latest measurement](#shared-segmentglobal-rules-bounded-original-memory-check)
for exact evidence. Sections below are historical milestones; their "next"
recommendations describe their own checkpoint, not parallel current tasks.

The Pascal files are a clean-room reconstruction from the BYOD executable's
assembly and decompiler artifacts. A meaningful Pascal body is not, by itself,
evidence of behavioral parity with the original executable.

The objective is source recovery, not a behaviorally similar clone. A stripped
binary cannot uniquely recover the original comments, formatting, identifiers,
or all source-level type choices. The project therefore records evidence-backed
reconstruction of the original routine structure, ABI, control flow, calls,
state effects, and data references, with uncertainty retained rather than
replacing unknown source with invented game behavior.

## Source-recovery ledger

`targets/liero/recovery.json` is the per-routine review ledger. Initialize or
synchronize it after ingesting an inventory change with:

```sh
make recovery-audit TARGET=liero
```

The audit reports inventory and assembly coverage, instruction/CFG evidence,
available decompiler output, Pascal bodies, explicit recovery states, and stale
source attestations. A routine counts as `source_recovered` only when every
required evidence category is cited, the Pascal body is non-placeholder, a
reviewer and review note are recorded, and its assembly/source hashes still
match. Marking a routine `unrecoverable` requires a reviewer and reason;
unreviewed or in-progress routines do not count as accounted.

To attest a reviewed routine, cite each evidence category and provide a reviewer
and rationale; the command fingerprints its current assembly and Pascal source
so later edits make the attestation stale:

```sh
python3 -m engine.recovery --target liero --attest FUN_24dd_02cb \
  --reviewer "reviewer" \
  --review-notes "Pointer-copy body and four destination writes match the evidence." \
  --evidence signature_and_abi=functions.json#FUN_24dd_02cb \
  --evidence control_flow=asm/FUN_24dd_02cb.s \
  --evidence call_targets=asm/FUN_24dd_02cb.s \
  --evidence state_and_memory_effects=asm/FUN_24dd_02cb.s \
  --evidence data_references=asm/FUN_24dd_02cb.s
```

The audit also inventories direct and indirect jump/call edges for each
assembly listing. A `source_recovered` attestation is rejected if a transfer
does not land on a decoded instruction in the target's assembly inventory.
Static far-indirect calls are accepted only when a verified stream record binds
the exact call bytes and pointer initializer to the binary and assembly
inventory. Near `CALL BX` edges may instead supply a binary-bound register path
from an exported `MOV BX,imm16` entry. The validator requires the complete
entry-to-call prefix, checks every encoded successor, accepts only a small
reviewed set of BX-preserving encodings, and rejects known entries or transfers
that bypass initialization. The target must be a decoded boundary in the same
code segment; it may be inside the recorded stream rather than at its start.
This proof is scoped to the current assembly and verified-stream inventory,
not unknown runtime entries or self-modifying code. Other register patterns,
indirect calls, and unparsed targets remain unresolved.
Segment:offset aliases are compared by their real-mode linear address, so a
transfer into the middle of another exported listing is accepted when that
exact instruction is present. Unresolved edges remain visible in the audit
output and must be decoded or accounted for before source recovery can be
attested.

### Current unresolved-transfer investigation

The current audit reports 13 unresolved transfers for the binary whose
SHA-256 is recorded in [BINARY_CENSUS.md](BINARY_CENSUS.md). The direct edges
have now been compared with the raw executable bytes using the MZ load mapping.
Edges into the ten verified alternate entries below are resolved through
binary-bound stream records in `targets/liero/alternate_streams.json`. The
manifest also records the statically initialized far-pointer target and the
register-seeded `CALL BX` stream described below: 12 verified stream records
in total. These records establish decoded destinations, not source or behavior
recovery.

| Group | Edges | Evidence and remaining work |
| --- | ---: | --- |
| File-backed alternate entries still unresolved | 0 edges, 0 targets | All ten file-backed destinations found in this investigation now have binary-bound instruction-stream evidence. |
| Verified alternate entries | 10 edges, 10 targets | `1000:398B`, `1000:E7D0`, `2000:7E29`, `2000:7FF7`, `2000:800B`, `2000:8012`, `2000:801A`, `2000:8030`, `2000:82A2`, and `2000:832C` are hash-bound to the original executable with exact instruction boundaries and verified source edges. These are control-flow findings, not source or behavior recovery. |
| Caller-CS near calls (resolved) | 5 edges, 2 exports | The five near `CALL` instructions printed with flattened operands `2000:FF06` and `2000:FCEF` wrap in the caller's 16-bit code segment. They resolve to the already-decoded entries `1ec2:12e6` and `1ec2:10cf`, respectively, rather than into the MZ allocation tail. The recovery audit and CFG now apply this near-transfer rule; far and indirect transfers remain unchanged. |
| Static far-indirect calls (resolved) | 2 edges, 1 target | Both `CALLF [0x63FE]` sites in `FUN_24dd_0353` use the pointer initialized by `FUN_24dd_0000` to `24DD:00D6`. The target maps to file offset `0x16616`, where the independently decoded bytes are `XOR AX,AX; RETF 2` (returns zero and removes one word argument). The intervening `FUN_24dd_04dc` helper does not modify DS. The manifest binds both calls and both pointer writes to the executable hash and assembly inventory. |
| Static register-indirect call (resolved) | 1 edge, 1 target | `CALL BX` at `24DD:033E` uses `BX=031Ch`, initialized at the exported entry `24DD:0303`. The target at `24DD:031C` is inside the newly recorded `24DD:0308..0322` stream. Its local branches and the complete entry-to-call register path are binary-bound and validated. |
| Null far jump | 1 far jump | The encoded destination is `0000:0000`. Its role is unknown; do not treat it as a valid routine or dismiss it as a bad target without runtime evidence. |
| Outside the module allocation | 2 far calls | Destinations are `FFFF:BD66` and `A000:4D2E`. They are outside the file-backed image and the declared minimum allocation; their runtime meaning is unresolved. |
| Indirect transfers still unresolved | 10 transfers | Five `CALLF [0x7838]` sites use the XMS entry pointer returned by `INT 2Fh` with `AX=4310`; one `JMPF SS:[0xD0]` uses the interrupt-2 vector; three far-call sites read object-relative pointers; and `CALL AX` has caller-seeded and callback-returned target candidates not yet resolved by the audit. See the provenance inventory below. |

#### Indirect-target provenance and confidence

The confidence column describes confidence in the listed source/data provenance,
not behavioral parity. "Unresolved" means the recovery audit still requires a
binary-bound decoded target record or runtime observation.

| Call sites | Provenance and current finding | Confidence |
| --- | --- | --- |
| `2494:0020`, `002F`, `0048`, `0058`, `0069` | `FUN_2494_0010` requests `INT 2Fh/AX=4310h`, then stores returned `BX` and `ES` at DS offsets `7838h` and `783Ah`. The five wrappers set AH to `08h`, `09h`, `0Fh`, `0Ah`, and `0Bh`; their far target is supplied by the installed XMS manager. | High that setup is correct; target remains runtime-dependent. |
| `24DD:0402`, `040E` | Resolved above. `FUN_24dd_0000` writes offset `00D6h` and current CS to DS:`63FEh`; no other assembly reference to either pointer word is present. `FUN_24dd_0353` and its `FUN_24dd_04dc` helper preserve DS before use. | High; both call edges are binary-bound and validated. |
| `24DD:23BB` | `FUN_24dd_2361` obtains vector 2 with `INT 21h/AX=3502h`, saves returned `BX:ES` at SS:`00D0h:00D2h`, restores the interrupted register/segment state, then far-jumps through the saved vector. This is an external interrupt handler, not a file-backed Liero routine. | High for vector setup; runtime handler target unresolved. |
| `24DD:033E` (`CALL BX`) | Resolved for the exported entry path. `24DD:0303` sets `BX=031Ch` and jumps to `24DD:0323`; all instructions through the call are binary-bound and preserve BX. The target at `24DD:031C` compares DS with DI through BX, then either returns or branches to `24DD:0308`, traverses the far-linked record, and repeats. The full loop is now a verified stream. | High for this static edge and decoded loop; no source or behavioral parity claim. |
| `24DD:3817` (`CALL AX`) | Four callers seed AX with `390Eh`, `39ABh`, `3A26h`, or `3ABAh`. Callbacks can return a new nonzero AX; the dispatcher preserves it through refill and calls it again. The validator now derives all seven initial/continuation candidates and checks known initialization bypasses. External refill behavior and unknown entries remain obligations, so the call stays unresolved. | High for bounded static closure; no runtime parity claim. |
| `24DD:3751` (`CALLF ES:[BX+DI]`) | The wrapper is called from `FUN_24dd_36c4` and `FUN_24dd_3711`; those callers pass BX values `10h`, `14h`, or `1Ch` and a runtime object offset in DI. Raw bytes `26 FF 19` prove that the far pointer is read from **ES**, correcting the exported operand that omitted the override. | High for segment and indexed operand; pointer values remain object-state dependent. |
| `24DD:396E` (`CALLF ES:[BX+14h]`), `24DD:397C` (`CALLF ES:[BX+18h]`) | Bytes `26 FF 5F 14` and `26 FF 5F 18` prove both wrappers read their far pointers from ES. The object initializer and open handler establish the standard method-slot candidates described below; caller object identity and later writes are not yet proven. | High for encoded operand provenance; complete runtime target set unresolved. |

#### AX callback continuations

Raw 16-bit decoding shows a buffered-input callback state machine, not a
single fixed callback per caller. All offsets in this table use CS `24DD`.
The byte spans include every instruction in each observed callback family.

| Caller export and seed instruction | Initial AX | Decoded file span (inclusive) | Nonzero AX values returned for another buffer |
| --- | --- | --- | --- |
| `FUN_24dd_38f0`, `38F6: B8 0E 39` | `390E` | `19E4E..19E6F` | `390E`, `3923` |
| `FUN_24dd_3988`, `398E: B8 AB 39` | `39AB` | `19EEB..19F02` | `39AB` |
| `FUN_2000_87bf`, `39F8: B8 26 3A` | `3A26` | `19F66..19F8A` | `3A26`, `3A37` |
| `FUN_2000_884f`, `3A88: B8 BA 3A` | `3ABA` | `19FFA..1A01E` | `3ABA`, `3ACB` |

The first family skips to CR or DOS EOF (`1Ah`), with `3923h` resuming the
optional LF check after CR crosses a buffer boundary. The second copies bytes
until CR, EOF, or the count is exhausted. The last two skip leading bytes at
or below space and then copy a token; `3A37h` and `3ACBh` resume the copying
phase. Each family also has a zero-AX completion path.

The dispatch bytes at linear `285F4` are `0B C0 75 08` (`OR AX,AX; JNZ
28600`). At `28600`, `PUSH AX` saves the returned continuation; the refill
call at `28606` targets `24DD:396C`, and `POP AX` at `2860E` restores it.
The branch at `28617` (`75 BC`) returns to `24DD:3805`, before `CALL AX`.
Thus recording just the four caller seeds would omit three real candidate
targets. These seven candidates are static findings, not runtime traces, and
do not yet establish callback ABI, refill behavior, or original-game parity.

#### Machine-checked AX callback closure

The `callback_protocols` section of `targets/liero/alternate_streams.json`
now binds the complete 94-byte dispatcher, four seed-to-call paths, and four
callback-family byte spans to the executable hash and real-mode mapping.
`engine/callbacks.py` validates this deliberately restricted
`liero_buffered_ax_v1` protocol. The full recovery audit includes its results
under `callback_protocols`; use the audit without `--summary-only` to see them:

```sh
python3 -m engine.recovery --target liero
```

The validator decodes the callback bytes rather than trusting instruction
labels or a manually supplied target list. It follows both outcomes of every
supported conditional branch, treats `LODSB` as an unknown AX value, and
requires every modeled return to establish a constant AX. Nonzero returns
become new callback entries until the closure stops growing. Unsupported
instructions, branches outside decoded boundaries, unknown AX returns, and
missing continuation targets fail validation. This is a conservative static
overapproximation, not a path-feasibility or termination proof.

The four seed paths preserve AX between `MOV AX,imm16` and their near calls.
They cover all direct calls to the dispatcher found in exported assembly.
The exact reviewed dispatcher bytes check the zero-AX exit, six-word
save/restore sequence around the refill call, and back-edge to `CALL AX`.
The resulting closure contains these seven entries:

| Callback entry (CS=`24DD`) | Modeled AX returns (hex) |
| --- | --- |
| `390E` | `0000`, `390E`, `3923` |
| `3923` | `0000` |
| `39AB` | `0000`, `39AB` |
| `3A26` | `0000`, `3A26`, `3A37` |
| `3A37` | `0000`, `3A37` |
| `3ABA` | `0000`, `3ABA`, `3ACB` |
| `3ACB` | `0000`, `3ACB` |

The validator also checks all 295 exported assembly listings and all 12
verified alternate streams for known initialization bypasses. It rejects
transfers into protected seed/dispatcher interiors, unseeded jumps to the
dispatcher entry, and overlapping exports or verified streams. Direct entry
at a seed's `MOV AX` initializer is allowed; the dispatcher's reviewed
internal branches are allowed. The byte ranges, not just primary instruction
boundaries, are protected against incoming direct transfers. The full audit
reports these results under `known_entry_bypass_check`.

This local proof assumes execution starts on a recorded seed path, immutable
code, valid non-aliasing buffers/stack, and a refill routine that returns
normally without changing saved stack words. Direct-call coverage does not
prove the absence of unknown runtime entries or unexported transfers. The
refill routine's object-relative far calls also remain unresolved. Accordingly
the report explicitly sets `resolves_call_site` to `false`: the audit still
reports **13 unresolved transfers**, and neither attestation nor behavior
verification is promoted by callback evidence.

#### Refill far-pointer segment correction and standard method setup

Independent raw-byte decoding found an `ES` override (`26h`) missing from
all three exported object-relative `CALLF` operands. The corrected listings
are `FUN_24dd_374d.s`, `FUN_24dd_396c.s`, and `FUN_24dd_397a.s`.
Their exact call bytes are now recorded under `indirect_operands` in the
binary-bound manifest. The audit decodes the segment register and indexed
operand from these bytes and rejects disagreement with the assembly listing.
This proves the **storage operand**, not the far pointer's runtime value.
The historical Ghidra C comments in the unmatched Pascal stubs are not an
oracle for these operands; they also omit the segment override.

| Linear call site | File offset | Bytes | Correct storage operand |
| --- | --- | --- | --- |
| `28521` | `19C91` | `26 FF 19` | `ES:[BX+DI]` |
| `2873E` | `19EAE` | `26 FF 5F 14` | `ES:[BX+14h]` |
| `2874C` | `19EBC` | `26 FF 5F 18` | `ES:[BX+18h]` |

This removes the previous DS-versus-ES uncertainty. The wrapper pushes
`ES:BX` (or `ES:DI`) as a far argument, matching the same object whose
method slot is read. The candidate handlers use `RETF 4` to remove that
argument; this observation does not establish that arbitrary slot contents
obey that ABI.

The following standard setup was independently decoded from this executable
hash. It is provenance evidence, **not yet a validated whole-object dataflow
proof**:

- The constructor at `24DD:3639` loads the destination object into `ES:DI`,
  clears DF, and uses `STOSW` to initialize it. The buffer pointer at object
  offset `0Ch` is object-base plus `80h`, in the same segment. The method at
  `10h:12h` is initialized to `24DD:420C`. The next 14 words, offsets
  `14h..2Fh`, are zeroed. Raw file span `19B79..19BAC` covers this prefix.
- The unexported handler at `24DD:420C` (linear `28FDC`, file `1A74C`)
  loads the passed object into `DS:DI`, opens/creates or uses its DOS handle,
  and assigns the standard methods. Its raw span through `RETF 4` is
  `1A74C..1A7D8`. Failed DOS open/create paths bypass the method writes.
- On the successful input-mode path (`D7B1h`), the handler assigns
  `24DD:375E` to slot `14h` and zero to slot `18h`. `375E` performs DOS
  `INT 21h/AH=3Fh` reads, updates the buffer-end field at `0Ah`, and
  resets its cursor at `08h`.
- Output paths assign either `24DD:378E` to slot `14h` with zero slot
  `18h`, or `24DD:37B3` to **both** slots. Both candidates perform DOS
  `INT 21h/AH=40h` writes; `378E` additionally detects a short write.
  The local helper at `24DD:4299` is now decoded completely; its external
  DOS behavior is not runtime-verified.
- Successful setup writes `24DD:37D3` to slot `1Ch`. This candidate uses
  DOS `INT 21h/AH=3Eh` to close handles above 4.

The code-segment immediates are stored as `14DDh` on disk, not `24DDh`.
The MZ relocation table contains the exact segment-word locations at file
offsets `19BA3`, `1A781`, `1A79C`, `1A7B2`, and `1A7D1`; adding the load
segment `1000h` yields `24DDh`. Treating the unrelocated constants as runtime
segments would point at the wrong code.

#### Complete setup/helper streams and conditional object states

The manifest's `object_setup_protocols` section now records the complete
141-byte setup routine (`24DD:420C..4298`), complete 90-byte helper
(`24DD:4299..42F2`), and the reviewed 52-byte constructor prefix.
`engine/object_setup.py` checks exact reviewed instruction templates:
27 constructor-prefix instructions, 51 setup instructions, and 40 helper
instructions. It rejects byte variants instead of assuming their effects.
Every local branch must land on a decoded boundary; the setup's only near
call must target the helper. The constructor's relocated method pointer must
target the setup entry. All five expected segment-word relocations are
required, and unexpected relocations overlapping these regions are rejected.

The full recovery audit exposes these streams separately under
`object_setup_protocols`, including instruction bytes, branches, near calls,
return sites, DOS interrupt sites, and the relocation records. They do
**not** enter the `verified_alternate_streams` count or automatically resolve
any indirect call.

A bounded constant-propagation analysis follows the setup's branches for
the three observed input modes. Unknown filename, DOS results, and device
status are overapproximated rather than guessed. The local helper is treated
as potentially clobbering all four tracked registers (AX, DX, CX, BX);
the subsequent explicit initializers must re-establish method values.

| Initial object mode | Method-slot outcome after setup | Resulting mode | Helper called |
| --- | --- | --- | --- |
| `D7B1` | `14h=24DD:375E`, `18h=null`, `1Ch=24DD:37D3` | `D7B1` | No |
| `D7B2` | `14h=24DD:378E`, `18h=null`, `1Ch=24DD:37D3` | `D7B2` | No |
| `D7B2` | `14h=18h=24DD:37B3`, `1Ch=24DD:37D3` | `D7B2` | No |
| `D7B3` | `14h=24DD:378E`, `18h=null`, `1Ch=24DD:37D3` | `D7B2` | Yes |
| `D7B3` | `14h=18h=24DD:37B3`, `1Ch=24DD:37D3` | `D7B2` | No |
| Any of these modes, open/create failure | Method slots unchanged (not necessarily null) | Initial mode retained | No |

These are conditional static outcomes, not a proof that every row is feasible
or that the same runtime object reaches a refill call. The input dispatcher
checks `D7B1` in its already-bound bytes; connecting that check to this setup
requires object identity and absence of intervening method-slot writes.

The helper first seeks to EOF and subtracts `80h` from the returned position,
clamping arithmetic underflow to zero. It seeks to that position, reads up to
`80h` bytes into object offset `80h`, then scans the returned byte count for
the first `1Ah`. If found, it seeks by `index - bytes_read` relative to EOF
and issues a zero-count DOS write, which is the truncation request. It returns
at `24DD:42F2`. The five `INT 21h` sites remain external effects: notably,
the code does not test carry after either initial seek, and this analysis
does not manufacture successful I/O outcomes or prove error handling.

The analysis assumes a valid object and stack, immutable relocated code, DOS
preservation of DS/DI, and buffer writes that do not alias method slots, live
stack words, or code. Next, runtime object identity, reachability, later slot
writes, and DOS effects must be checked before either refill call can be
resolved or behavior verification claimed. `CALL AX` and all three
object-relative far calls remain unresolved; the total remains **13**.

### Alternate-entry byte checks

The ten file-backed destinations were independently disassembled from their
exact raw offsets with GNU `objdump` 2.47 in 16-bit mode. For this binary,
`file_offset = linear_address - 0x10000 + 0x1770`; `objdump` was given
`--adjust-vma=0xe890`. These observations are bound to the executable SHA-256
above. They confirm the bytes at each destination, but do not by themselves
establish that every overlapping stream is semantically correct.

| Destination | File offset | Observed stream from the exact entry |
| --- | ---: | --- |
| `1000:398B` | `0x050FB` | Verified 459-byte primary stream. Its overlapping entries at `1000:39EA` and `1000:3A4A` were decoded independently; all branch targets resolve to recorded instruction boundaries, and the streams rejoin at exported boundary `1000:3A56`. Both far calls resolve through MZ relocations to `24DD:3268` inside decoded export `FUN_24dd_3249`. |
| `1000:E7D0` | `0x0FF40` | Verified alternate stream. The near `CALL` at `0x1E97F` encodes `E8 4E FE` and reaches this entry; it starts `C8 04 02 00` and reaches `RET 4` at `1000:E84B`. Its two far calls have relocation-checked destinations `24DD:4919` and `24DD:3EAF`, matching decoded exports `FUN_24dd_4919` and `FUN_24dd_3eaf`. Local conditional and short-jump targets match recorded instruction boundaries. |
| `2000:7E29` | `0x19599` | Verified 383-byte stream, decoded from its exact entry. All 29 short/near branches reach recorded boundaries or decoded exports; it includes a near jump to `24DD:011A` and an `IRET` exit. The encoded null far jump at `2000:7E91` remains unresolved. |
| `2000:7FF7` | `0x19767` | Verified 34-byte stream. Its local `JB` and `JNE` targets are instruction boundaries; it returns with `RETF` at `2000:8007` and `2000:800E`, or jumps to decoded instruction `24DD:010F` at `2000:4EDF`. |
| `2000:800B` | `0x1977B` | Verified 14-byte stream. `DB 33` is recorded as a two-byte x87 ESC with its FPU operation unresolved; the remaining instructions loop to `2000:8001` or jump to decoded `24DD:010F`. |
| `2000:8012` | `0x19782` | Verified 7-byte alternate entry: `OUT DX,AL`, `MOV AX,0xCD`, then a near jump to decoded instruction `24DD:010F`. It begins at the displacement byte of the neighboring `JNE` at `2000:8011`. |
| `2000:801A` | `0x1978A` | Verified 99-byte stream with 49 instruction boundaries. Its short-branch targets resolve to this stream, verified sibling streams, or decoded assembly exports; it reaches `RETF` at `2000:807C`. |
| `2000:8030` | `0x197A0` | Starts at the displacement byte of a neighboring short branch; decoded independently, it is `MOV AX,[7B40]`, `MOV DX,[7B42]`, `RETF` at `2000:8037`. |
| `2000:82A2` | `0x19A12` | Verified 60-byte number-formatting stream. The incoming `LOOP` at `24DD:3503` is `E2 CD`; the stream returns at `2000:82DD`. Its interrupt effects remain unverified. |
| `2000:832C` | `0x19A9C` | Verified 87-byte exponent-parsing stream. Incoming `JCXZ`/`JNZ` bytes are `E3 0E`/`75 07`; it returns at `2000:8382`. It calls `2000:9502` and decoded export `24DD:35D4`; the first helper's full behavior remains unverified. |

This narrows the address-mapping question: all ten destinations are
file-backed, and the original source instructions encode the reported
destinations. The verified `2000:8030` stream consists of `MOV AX,[7B40]`,
`MOV DX,[7B42]`, and `RETF`; its entry is the displacement byte of an
overlapping neighboring short branch. The audit accepts this exact entry only when the binary hash, file mapping,
source-branch bytes, and contiguous instruction bytes match the manifest.
Branch destinations may be boundaries in the same stream, another verified
stream, or exported assembly. The `2000:800B` instruction boundary is
verified, but its x87 operation remains unresolved. The `2000:7E29` entry
evidence resolves its incoming control-flow edge, but the null far jump
remains unresolved. No routine has been promoted to `source_recovered` by
this entry evidence.

The verified `2000:7E29` stream begins with `25 B9 0A` at file offset `0x19599`
and covers 383 contiguous bytes through linear address `0x27FA7`. Its source
`JNP` at `24DD:308C` has bytes `7B CB` and resolves to `2000:7E29`. The local
near-branch targets resolve to instruction boundaries in the stream or to
decoded exports `24DD:304F`, `24DD:3056`, and `24DD:011A`. The stream contains
an `IRET` at `2000:7F75`, helper returns, and an encoded far jump at
`2000:7E91` to `0000:0000`; that far-jump destination remains unresolved. This
verifies instruction-boundary evidence only, not the interrupt, hardware, or
DOS behavior.

The verified `2000:8012` stream is seven bytes, `EE B8 CD 00 E9 C6 CE`, at
file offset `0x19782`. It starts at the displacement byte of the neighboring
`JNE` at `2000:8011`, where the alternate decode is `OUT DX,AL`. Its incoming
`JNP` at `24DD:3275` has bytes `7B CB` and resolves to `2000:8012`; the near
`JMP` at `2000:8016` resolves to decoded instruction `24DD:010F`. This verifies
the alternate instruction boundaries, not runtime behavior.

The verified `2000:800B` stream covers 14 bytes from file offset `0x1977B`.
Its opening bytes `DB 33` are an x87 ESC with an unresolved FPU operation; the
record preserves that uncertainty instead of assigning an operation. The
subsequent `JNE` at `2000:8011` targets decoded `2000:8001`, and the near
`JMP` at `2000:8016` reaches decoded instruction `24DD:010F`. The incoming
`JNP` at `24DD:326C` has bytes `7B CD`. This confirms instruction boundaries
and direct edges, not FPU behavior.

The verified `2000:801A` stream covers 99 bytes from file offset `0x1978A`
through `2000:807C`. Its incoming `JNP` at `24DD:327B` has bytes `7B CD`.
Its branch targets were checked against this stream, the sibling entries
`2000:7FF7`, `2000:800B`, and `2000:8012`, and decoded assembly boundaries.
The stream reaches `RETF` at `2000:807C`; this is control-flow evidence only.

The verified `2000:82A2` stream covers 60 bytes from file offset `0x19A12`
through `2000:82DD`. Its incoming `LOOP` at `24DD:3503` has bytes `E2 CD` and
returns to this exact entry. The stream includes `INT 37h` and `INT 3Dh`;
their effects are unresolved, so this record establishes boundaries and the
direct loop edge only.

The verified `2000:832C` stream covers 87 bytes from file offset `0x19A9C`
through `2000:8382`. Its incoming `JCXZ` at `24DD:354C` and `JNZ` at
`24DD:3553` have bytes `E3 0E` and `75 07`. The call at `2000:8341` encodes
`E8 BE 11` and reaches `2000:9502`, whose entry bytes independently decode as
`XOR AX,AX`; the full helper boundary and behavior are not established here.
The call at `2000:835C` reaches decoded export `24DD:35D4`. This alternate
stream also contains interrupt and loop effects that remain unverified.

The verified `2000:7FF7` stream begins with `D4 00 83 D3 00` at file offset
`0x19767`. Its incoming `JNP` at linear address `0x28028` has bytes `7B CD`
and resolves to `2000:7FF7` in caller segment `24DD`. The internal `JB` at
`2000:7FFF` targets `2000:800F`; the `JNE` at `2000:8011` loops to
`2000:8001`. The two `RETF` exits are at `2000:8007` and `2000:800E`.
The near `JMP` at `2000:8016` resolves to `2000:4EDF`, the same linear address
as decoded instruction `24DD:010F`. This confirms the control-flow evidence
for this entry, not its source or behavior.

The verified `1000:398B` stream begins with `0C 00 8B 46 EE`. Its source edge
is the `JLE` at `1000:39B5`, whose raw bytes `7E D4` target `1000:398B`.
Prefixed `CS LOOP` instructions target `1000:39EB` and `1000:3A4A`; the `JLE`
at `1000:3A14` targets the overlapping entry `1000:39EA`. These entries join
the primary stream at `1000:39EC` and `1000:3A4B`, while the full stream joins
the exported instruction at `1000:3A56`. The `CALLF` instructions at
`1000:39E4` and `1000:3A43` contain the on-disk segment `14DD`; relocation
records at file offsets `0x5157` and `0x51B6` resolve both to runtime
`24DD:3268`, a decoded instruction inside `FUN_24dd_3249`. This verifies the
alternate control-flow boundaries and calls, not the behavior or source body.

The verified `1000:E7D0` stream's two far-call operands are stored with segment
`14DD` in the file. MZ relocation records 1160 and 1161 point to the segment
words at file offsets `0x0FF8D` and `0x0FFB8` (image offsets `0x0E81D` and
`0x0E848`); loading at segment `0x1000` changes each segment to `24DD`.
Consequently, the runtime destinations are `24DD:4919` and `24DD:3EAF`,
whose bytes at file offsets `0x1AE59` and `0x1A3EF` match the exported
instruction listings. Their in-stream conditional branches also land on
instruction boundaries in those same routines via equivalent segmented
addresses. The alternate-stream validator checks the near-call source edge,
the exact bytes and boundaries, every direct local branch, both MZ relocation
records, and the decoded runtime destination entries. The recovery audit now
counts E7D0 as a verified alternate entry; this is control-flow evidence only,
not source or behavior recovery.

These are classifications, not blanket waivers. The five near calls are
resolved by the instruction-set's caller-CS semantics and matching decoded
entries; the ten file-backed alternate entries listed above are resolved
only by their hash-bound streams; the remaining unresolved edges have not
been waived.
The acceptance gate remains strict, and no routine is promoted to
`source_recovered` by this investigation. All ten file-backed entries listed
above have independent byte-boundary checks; next investigate the unresolved
dynamic callback contracts.

For a resumable local-model review of unresolved file-backed entries, run:

```sh
python3 -u tools/overnight7.py --budget-hours 8
```

The script maps each direct target to the original MZ image, disassembles from
that exact byte, and asks the configured local Ollama model to produce notes
and a separate critique. The full configured byte window is preserved in the
disassembly; completed entries are resumed only when their analysis version
and byte-window size still match. It prioritizes `1000:398B`, then continues
with unresolved file-backed targets selected from the current audit. Verified
entries such as `1000:E7D0` and `2000:8030` are no longer candidates. Progress
is checkpointed to `reports/overnight7/analysis.json`; the readable report is
`reports/overnight7/CONTROL_FLOW_REVIEW.md`. These model outputs are explicitly
hypotheses: the script does not change assembly, Pascal source, the recovery
ledger, or acceptance gates. Human review and independently verified
instruction boundaries are still required before alternate streams can count
as resolved.

Source review and behavior validation are separate ledger records. Record a
passing host test with its test-file reference. A routine without external
effects may use `not_required` for original-binary validation only with an
explicit rationale; a routine with DOS, BIOS, hardware, overlay, or comparable
external effects must have a passing DOSBox/equivalent result and reference:

A DOSBox 0.74-3 probe using temporary copies confirmed scripted command
execution and writes to the mounted directory. Launching `LIERO.EXE` with the
dummy video driver remained active until an 8-second timeout, without
observable input/output. This is setup evidence only, not original-binary
behavior validation; the game may not have reached gameplay.

```sh
python3 -m engine.recovery --target liero \
  --record-validation FUN_24dd_4919 \
  --host-test-status passed \
  --host-test-reference targets/liero/tests/test_liero_runtime.pas \
  --no-external-effects \
  --original-binary-status not_required \
  --original-binary-reason "Pure byte transform; no external effects." \
  --validation-notes "Exhaustive 256-value host test passed."
```

The audit reports host-test passes, original-binary passes, and
`behavior_verified` separately. That last count requires current source
recovery, passing focused host tests, and either a passing original-binary
check or a reviewed `not_required` decision for a routine with no external
effects. Host stubs and mocked effects never satisfy the real-environment
requirement.

This ledger measures reviewed source reconstruction, not original-source text
identity or runtime equivalence. Compilation and behavioral/oracle results
remain separate. In particular, a successful `-Mtp` build or DAT-format
round-trip cannot promote a routine to recovered source. The current ledger is
function-scoped: its 295 entries matching the Ghidra export count do not prove
that every executable byte, embedded routine, or code/data boundary in the
original image has been identified. Full-program completion also requires that
binary-wide census and explicit accounting for unclassified ranges.
Unmatched routines remain visibly incomplete. Do not assign fabricated return
values merely to silence compiler warnings: an unset-result warning is evidence
that a routine still needs translation or an explicit runtime/ABI model. A
successful build does not make an incomplete routine recovered.
The current MZ header, routine-span, relocation, and unclassified-range
baseline is recorded in [BINARY_CENSUS.md](BINARY_CENSUS.md) and can be
regenerated with `make binary-census TARGET=liero`.

## Implemented assembly-derived routines

| Routine | Current model | Verification |
| --- | --- | --- |
| `FUN_1ea2_01f0` | Reset logical state byte corresponding to `DS:$65EE` | Pascal unit harness only |
| `FUN_1ea2_01a8` | Copy a rectangular byte region into 320-byte destination rows, using the supplied source stride | Pascal host-model tests cover odd/even widths, multiple rows, and untouched padding |
| `FUN_1000_5e66` (partial) | Check frame stack space; gate framebuffer clear and viewport rendering on the signed frame-counter remainder; update and clamp both camera offsets; chase inactive players, average matching owned entities, apply shake from the signed 16-bit magnitude, copy the two camera viewports, and draw the health, ammunition, and reload-progress bars | Pascal host-model checks cover positive and negative render intervals, skipped off-tick framebuffer writes, camera behavior and shake, viewport row/stride/placement, and bar dimensions, colors, and boundaries; remaining gameplay/HUD/draw logic and original-binary parity are unmatched |
| `FUN_24dd_04ed` | Read and clear logical word corresponding to `DS:$6410` | Pascal unit harness only |
| `FUN_24dd_0530` | Check requested stack allocation against the modeled stack pointer and guard word | Caller/helper/error-entry bytes and relocations match the original image; Pascal unit harness covers the exact-boundary success case; shared error handling after the entry test remains unreviewed |
| `FUN_24dd_0582` | Load `AX=$0576`, copy six words through the shared helper, and return source-end `AX=$0582` modulo 16 bits. | Host tests and the scoped original-byte training/held-out fixtures pass; routine-wide parity and other flags remain unverified. |
| `FUN_24dd_05e8` | Load `AX=$05DC`, copy six words through the shared helper, and return source-end `AX=$05E8` modulo 16 bits. | Host tests and the scoped original-byte training/held-out fixtures pass; routine-wide parity and other flags remain unverified. |
| `FUN_24dd_05fd` | Initialize a six-word record at `ES:DI` with four zero words, the original AX, then zero-extended CL; restore DI | Pascal unit harness with boundary guards |
| `FUN_24dd_0642` | Reserve 12 bytes below the logical stack pointer and copy six words from the modeled code segment at `SI` into the saved DS segment | Pascal unit harness; checks copied bytes, stack update, and preserved registers |
| `FUN_235c_135f` | Clear the three DS-relative state bytes at `$67FA`, `$7688`, and `$7690` | Pascal unit harness with neighboring-byte guards |
| `FUN_24dd_02cb` | Copy an input far-pointer value into four logical global words | Pascal unit harness only |
| `FUN_24dd_02b9` | Write the logical global far pointer to a caller-provided pointer value | Pascal unit harness only |
| `FUN_24dd_0628` | Reserve 12 bytes at a logical stack offset and copy six words from the same segment | Pascal unit harness only |
| `FUN_24dd_0673` | Reserve 12 bytes and copy six words from the previous logical stack location | Pascal unit harness only |
| `FUN_24dd_350e` | Read `SS:[BP+SI-$28]`, advance SI for nonzero bytes, and map NUL to `'0'` without advancing SI | Host tests cover nonzero, NUL, 16-bit offset wraparound, and 20-bit real-mode address wraparound; original-binary parity is unverified |
| `FUN_24dd_3dbd` | Signed 32-bit division from DX:AX by BX:CX, returning the quotient in DX:AX and remainder in BX:CX | Pascal unit harness covers positive, negative, and nonzero-high-word cases |
| `FUN_24dd_46b1` | Advance the 32-bit random state using the multiplier word in the modeled code segment at `$46E7`; return the new state in DX:AX | Pascal host-model vector with an explicitly initialized multiplier; original-image parity is unverified |
| `FUN_24dd_4654` | Scale the next random value to a 16-bit range using the caller's bound | Pascal host-model vector; original-image parity is unverified |
| `FUN_24dd_3c03` | Compare the logical word at `ES:DI+2`, preserve compare ZF, and set the error word on mismatch | Pascal unit harness only |
| `FUN_24dd_3639` | Construct a fixed-layout file-control record and copy a capped length-prefixed name | Pascal unit harness only |
| `FUN_1ec2_0000` | Copy `floor(byte_count / 4)` dwords, forward | Pascal unit harness only |
| `FUN_1ec2_00a5` | Copy rows of bytes with a 320-byte stride | Pascal unit harness only |
| `FUN_1ec2_13b0` | Copy 16000 dwords (64000 bytes), forward | Pascal unit harness only |
| `FUN_1ec2_13d3` | Clear 16000 dwords (64000 bytes) | Pascal unit harness only |
| `FUN_24dd_04dc` | Model the 16-bit AX/DX arithmetic and return DX:AX | Exhaustive host test across all 65,536 AX values against an independent instruction-level reference; checks AX, DX, carry, zero, and direction flags |
| `FUN_1ec2_086b` | Return the sign of a signed word as -1, 0, or 1 | Pascal unit harness only |
| `FUN_1ec2_09bd` | Return the sign of a signed word as -1, 0, or 1 | Pascal unit harness only |
| `FUN_1ec2_0ae3` | Return the sign of a signed word as -1, 0, or 1 | Pascal unit harness only |
| `FUN_1ec2_0c11` | Return the sign of a signed word as -1, 0, or 1 | Pascal unit harness only |
| `FUN_24dd_4919` | Convert ASCII lowercase bytes to uppercase; preserve other byte values | Exhaustive host test across all 256 inputs |
| `FUN_24dd_40d6` | Store one word, then clear the following 15 words | Pascal unit harness, including guard word |
| `FUN_24dd_3d68` | Copy bytes forward using the 16-bit count | Pascal unit harness, including zero count and overlapping buffers |
| `FUN_24dd_4905` | Fill caller memory with one byte using a 16-bit count | Host tests for zero, 257, and 65535 bytes with guards; segmented-pointer/register effects remain unverified |
| `FUN_24dd_492c` | Clear 2,966 words in the logical DS memory range `$6426..$7B51` | Exhaustive host test of the range and boundary guards |
| `FUN_235c_04f3` | Clear DS-relative bytes `$7690` and `$7692` | Guarded host test verifies both writes and preserves neighboring bytes |
| `FUN_24dd_3e63` | Logical 32-bit right shift of DX:AX by CL masked to 5 bits; selects an optimized or fallback implementation from DS:`$6420` | Register-state cases cover both CPU paths and counts 0, 1, 16, 31, 32, and `$FF1F` |
| `FUN_24dd_3e7c` | Logical 32-bit left shift of DX:AX by CL masked to 5 bits; selects an optimized or fallback implementation from DS:`$6420` | Register-state cases cover both CPU paths and counts 0, 1, 16, 31, 32, and `$FF1F` |
| `FUN_1ec2_0c3b` | Rasterize a line with alternating `$3F`/`$3E` colors | Host runtime assertions; no original-binary comparison |
| `FUN_1ec2_09e7` | Rasterize a line and apply the conditional pixel adjustment at each point | Host runtime assertion; no original-binary comparison |
| `FUN_1ec2_0810` | Load one indexed RGB triplet from a 768-byte palette table | Host runtime assertion against the modeled VGA palette |
| `FUN_1ec2_0734` | Render nonzero pixels from a 9-by-10 glyph bitmap, with the assembly's orientation variant | Host runtime assertion; no original-binary comparison |
| `FUN_1ec2_01df` | Render a 9-by-10 sprite through the raw-pixel or adjusted-pixel helper | Host runtime assertion; no original-binary comparison |
| `FUN_1ec2_152f` | Read one indexed RGB triplet from the modeled VGA palette | Host runtime assertion; hardware I/O not exercised |
| `FUN_1ec2_13a4` | Model BIOS video-mode service 0 by retaining the requested mode byte | Host runtime assertion; BIOS/DOSBox behavior not exercised |
| `FUN_1ec2_0386` | Render a 16-by-12 sprite with the three color-threshold modes and mirrored orientation | Host runtime assertion; no original-binary comparison |
| `FUN_1ec2_13c5` | Wait for VGA vertical retrace to become inactive and then active | Host runtime assertion with a sequenced port-read model; no hardware comparison |
| `FUN_1ec2_15bb` | Read the full modeled VGA palette into RGB triplets | Host runtime assertions; hardware I/O not exercised |
| `FUN_24dd_0232` | Model DOS function 06 output of the low byte of AX | Host runtime assertion against the output buffer model |
| `FUN_24dd_020a` | Divide the low byte of AX by CL, print the quotient digit, and return the remainder in both bytes | Host runtime assertion through the DOS output model |
| `FUN_24dd_022a` | Convert a low-byte nibble to a hexadecimal character and emit it | Host runtime assertion through the DOS output model |
| `FUN_24dd_01fe` | Emit a three-digit decimal representation using the quotient/remainder helper | Host runtime assertion through the DOS output model |
| `FUN_1ec2_155e` | Upload all 256 RGB palette entries to the modeled VGA palette | Host runtime assertion; hardware I/O not exercised |
| `FUN_24dd_021f` | Emit both hexadecimal nibbles of AL | Host runtime assertion through the DOS output model |
| `FUN_24dd_0218` | Emit the high byte of AX as two hexadecimal digits while restoring AX | Host runtime assertion through the DOS output model |

### Shared segment/global rules: bounded original-memory check

The next changed-strategy batch addressed the blocker below in shared
`engine/instruction_facts.py` rules, not a `492c`-specific sketch. Segment
push/pop provenance, unsigned word `SUB` and one-bit `SHR` now allow
bounded entry-DS `STOSW`/`REP STOSW` facts. Changed SP/SS, source-segment
loads and potentially stack-aliasing object stores invalidate applicable
bindings rather than reuse stale segment/stack claims. Generic tests vary
immediates, segment origins and bounds, including subtraction wrap, odd
spans and a last word ending at offset 65536.

```sh
uv run python tools/liero_four_routine_pilot.py \
  --prefix-transfer-routine FUN_24dd_492c \
  --prefix-data-window 0x6000 0x8000 --output <new-empty-directory>
```

The supplied half-open window is a **caller precondition**: entry DS has
valid writable memory disjoint from the stack, code and other tracked
objects. It is not a discovered allocation or proof of arbitrary caller
safety. Without a window the new rules decode **15/18 bytes**, stopping
before `REP STOSW` without publishing writes. With this window they decode
**17/18 bytes**, deriving zero writes to `[6426h,7B52h)`: `B96h` words
(2966 words / 5932 bytes). DI ends at `7B52h` and CX is zero.
`RET` at `493Dh` remains unsupported residue, so the CLI deliberately exits
nonzero and reports `routine_recovered: false`.

**Measured 2026-10-31:** three DOSBox COM executions embed the original
18 bytes at their original offset, initialize `[6000h,8000h)` with
`A5h`, `5Ah` or `FFh`, then check all **8192 observed bytes** against the
derived writes. All three match; all **2260 bytes outside the clear range
within that window** retain their seeds. Observed SP before/after the call
is `FFFEh` for each execution. These are original-only guarded COM
contexts, not Pascal differential tests, full flags/register ABI checks
or normal-program observations.

Final static evidence is session artifact
`liero-global-range-492c-20261031-final/`; rule SHA-256 is
`490ec7b9bdb952b7b3c860bcb1451c43fb924748020ed204e1c6de858e9e996e`.
Original execution artifacts are in
`liero-global-clear-measurements-20261031-final/`, with harnesses, original
bytes, COM binaries, traces and per-seed `measurement.json` hash manifests.
The final static report and snapshots rederived exactly; each distinct
measurement's artifact hashes, full memory output and SP pair replayed.
The earlier development snapshots are not the final rule identity.

Reproduce the original-only checks with:

```sh
uv run python -m pytest tests/test_instruction_facts.py \
  -k original_global_clear --basetemp=<new-empty-measurement-directory> -q
```

BYOD or missing DOS probe tools yield an explicit skip, not a pass.
The combined instruction-fact, pilot, constructor, close and refill
regressions pass **184 tests**; Ruff passes. Four protected Pascal
constructor/comparator/refill/close body hashes remain unchanged.
There are **zero newly recovered routines**, no model calls, installation
or training/source promotion. The historical 4/18 frozen failure below is
preserved; this is a measured repair of shared rules on a known routine,
not untouched-routine generalization. No frontier expansion follows this
bounded milestone.

### Frozen prefix transfer: distinct global initializer remains unsupported

The next check froze the final `engine/instruction_facts.py` implementation
and selected `FUN_24dd_492c`, a callee-free global-clear initializer outside
the constructor/read/close generated sketch trials. This routine was already
manually reconstructed: it is untouched by the new transfer method, **not**
a blind-source or previously unknown routine benchmark. Its frozen-rule
SHA-256 is
`98cc48ace0b2f294978224fc056b190835f019537167b936f03dc3e33badd1b3`.
No opcode rule, candidate sketch or mutation operator was added after
observing this result.

```sh
uv run python tools/liero_four_routine_pilot.py \
  --prefix-transfer-routine FUN_24dd_492c --output <new-empty-directory>
```

The reusable evidence-only mode reads the exported entry/size, binds exact
bytes through the existing binary manifest/MZ loader, and runs the supported
prefix rules. It saves original bytes, the exported listing, frozen rule
source and the recomputable report. `validate_prefix_transfer(root, output)`
rejects changed rule/binary/report identities or tampered snapshots.
Unsupported coverage returns a nonzero CLI exit; it is not success-shaped
routine recovery. Exported assembly is retained for provenance, not used
as the semantic oracle or supplied as a recovered-source example.

**Measured 2026-10-31:** original bytes at file offset 110188 are
`bf26641e07b9527b2bcfd1e933c0fcf3abc3`.
The frozen method decodes only **4/18 bytes**: `MOV DI,6426h` and `PUSH DS`.
It stops at `24DD:4930` (`POP ES`, opcode `07h`) and retains all fourteen
remaining bytes as unsupported residue. DI is a constant absolute offset,
not an established object-relative pointer. The prefix's legacy
`next_object_offset` diagnostic is not a usable object-field fact unless
the recorded DI kind is `object_offset`; it is **not** one for this routine.
No memory-write facts, candidate synthesis, model calls or differential
routine passes were produced. The decoder's object/source entry assumptions
are conditional and are not established for this global initializer.

Evidence is session artifact `liero-frozen-prefix-transfer-492c-20261031/`.
The saved report and three snapshots replayed; the rule source remained
identical to its evaluation snapshot. The earlier live constructor workspace
contains the pre-final JSON-native-provenance/type-validation implementation,
so its file hash is not identical. Executing that trusted historical rule
snapshot on these bytes produces the same JSON-normalized prefix result.
Do not relabel those historical files as byte-identical.

This check establishes a concrete transfer blocker, not an end-to-end
generalization result: object-relative initialization rules do not yet
handle DS-to-ES stack transfer or global range arithmetic/write effects.
The supported byte fraction is coverage, not a recovery pass rate.
There are **zero newly recovered routines** in this check, and no wider
frontier or second model batch follows. Future support must address shared
segment provenance and absolute/global memory bounds with independent
evidence, rather than append a `492c`-specific answer after seeing it.
Generalization of automatic source recovery remains unverified.

### Constructor instruction constraints: changed strategy, scoped pass

After the failed expansion below, the next batch stayed on `FUN_24dd_3639`
and changed the information flow instead of widening mutations or routines.
Supported straight-line 8086 transfer rules derive initialization writes
directly from the hash-bound original bytes. Constants are no longer left
to the model. The existing MZ loader and relocation-table checker bind the
stream; the prefix report retains instruction-relative offsets, exact bytes,
value provenance, entry assumptions and the unprocessed residue.

The decoder supports a limited set of register-immediate/register-register
MOVs, same-register XOR, the recorded stack far-pointer loads, CLD, LEA
AX relative to DI, MOV AX from ES, STOSW and REP STOSW. Unknown instructions,
unknown store operands, direction or bounds stop extraction; no instruction
is skipped and no guessed value crosses an unsupported transfer.
This is not a complete emulator, CFG solver or compiler-pattern recognizer.

Seven fields are constrained by the initialization prefix:

| Field | Derived value | Original support |
| --- | ---: | --- |
| Mode | `D7B0h` | Immediate loaded at `364Ah`, stored at object+2 |
| Capacity | 128 | Immediate at `364Eh`, stored at object+4 |
| Buffer relative offset | 128 | At `3657h`, advanced DI is object+12; LEA adds `74h` |
| Setup offset | `420Ch` | Immediate at `365Eh`, stored at object+16 |
| Setup logical segment | `24DDh` | Immediate `14DDh` at `3662h`, with an actual MZ fixup and load segment `1000h` |
| Zero-word span | 14 | CX at `3668h`, REP STOSW at `366Bh` |
| Following copy destination | 48 | DI advances through ten words and fourteen further words |

The prefix stops at `3670h`. Initial CX=79 is recorded, but not promoted
to a proven loop contract. `name_limit`, `stop_at_nul` and
`use_length_prefix` remain unresolved fields. The model still selects them
from the original instructions, within the existing constructor sketch.
Known numeric fields have singleton schema choices; explicit contradiction
checking also rejects raw model responses that ignore those choices.
Neither the model's saved sketch nor the renderer silently replaces a
contradictory value. Repair re-derives/checks the same constraints and uses
the **unchanged** four name-cap/prefix/NUL alternatives.

```sh
uv run python tools/liero_four_routine_pilot.py --routine constructor \
  --constructor-instruction-constraints --output <new-empty-directory>
```

**Measured 2026-10-31:** one fresh Qwen2.5-Coder 14B instruct proposal
selected the constrained initialization correctly, name cap 79 and early
NUL termination, but selected no length prefix. It passed 2/514 training
cases. The decrement/increment cap alternatives each passed 2/514; the
NUL toggle passed 0/514. The existing length-prefix toggle was selected
by training, passed **514/514**, and then passed **264/264 held-out** cases.
Five unique candidates were measured, with no second model request and
only one generated held-out evaluation. Initialization facts alone were
not counted as candidate acceptance.

Evidence is session artifact `liero-constructor-instruction-facts-20261031/`.
All eight original/Pascal reports (two controls, four failures and two
selected-candidate suites) replayed against their source snapshots.
Both saved instruction-fact reports re-derived from the bound bytes;
JSON-native provenance records permit exact saved/recomputed comparison.
Modified-constant, relative-offset and relocation-wrap fixtures test the
transfer rules; unknown/unsafe prefixes, stale binaries and tampered saved
facts are rejected. Those fixtures are software tests, not unseen-routine
generalization results. Repository routine/ledger hashes remain unchanged.

This establishes a **scoped model-plus-static-constraints-plus-repair pass**
on the previously failing constructor. It does not retroactively change
the earlier 0/1 trial, prove absence of over-specialization, certify historical
source/TP7 ABI or establish universal routine equivalence.
The argument bindings, initialization/copy topology and repair choices are
still developer-supplied. No new routine set, wider run, source attestation,
candidate installation, corpus promotion or model-weight learning follows.
Generalization still needs the method frozen before an untouched-routine
evaluation; passing a repaired known slice is not that evaluation.

### Bounded constructor expansion: no new automatic pass

The first expansion beyond close/refill selected `FUN_24dd_3639`.
Its independently decoded 83-byte body executes no call: it initializes the
object, stores a setup pointer, and copies a bounded name. Storing the pointer
does not require guessing or executing the setup callee. The existing
constructor oracle remains unchanged: 514 training cases and 264 held-out
cases, checking original bytes, candidate bytes and the independent write
contract, including unchanged input, guards and object tail.

```sh
uv run python tools/liero_four_routine_pilot.py --routine constructor \
  --automatic-constructor-repair --output <new-empty-directory>
```

The developer-supplied sketch fixes the sequential ten-word initialization,
subsequent zero-word span and bounded byte-copy topology. The model chooses
mode, capacity, buffer-relative offset, setup offset/segment, clear count,
copy destination/cap and length-prefix/NUL handling. Strict integer/Boolean
bounds prevent out-of-object host writes but do not establish correctness.
The prompt explicitly describes the probe's logical segment mapping
(image-relative segment plus `1000h`); the renderer does not silently fix
the model's segment or other constants. No reviewed target body is supplied
as an example.

Repair reuses the existing replay-bound loop. At most four alternatives
modify one field each: decrement/increment the name cap within bounds,
toggle early NUL termination, or toggle Pascal length-prefix handling.
It does not rewrite initialization constants, combine mutations or expand
the hypothesis space after observing failures. The first training pass
would gate one held-out suite; a held-out failure would end the run.

**Measured 2026-10-31:** both original/current-source positive controls passed.
Four Qwen2.5-Coder 14B instruct requests produced four distinct compiled
sketches and thirteen distinct compiled repair alternatives: **17 hypotheses,
zero training passes**. All 514 training cases failed for each hypothesis.
No generated candidate reached held-out execution. The model generally
selected zero for nonzero initialization constants and wrong buffer/name
offsets; copy-cap and Boolean mutations cannot repair those errors.
The limited name cap was not the sole blocking question in this live trial.

All 19 saved original/Pascal reports (two controls and seventeen failures)
replayed successfully against their source snapshots. Protected repository
routine includes and the recovery ledger remained unchanged. Evidence is
retained in session artifact `liero-automatic-constructor-20261031/`, with
raw responses, prompts, sketches, lineage and byte counterexamples.
The trial's original retry feedback was valid JSON; no feedback-transport
failure is established as the explanation for the model errors.
Constructor feedback now additionally caps representative byte differences
and records omitted counts, ensuring large future reports remain valid JSON.
No new model run was performed after this output-bounding change.

A separate deliberate `name_limit=78` integration fixture failed original
training and was repaired to 79, passing 514 training and 264 held-out cases.
This verifies the repair mechanism on a known off-by-one fault, **not** a live
model success or another newly recovered routine.

The new slice's yield is **0/1**, below the 25% expansion floor. Expansion stops:
no comparator batch, model sweep, source installation, source attestation,
knowledge promotion or training update follows. Close/refill PoC results
remain valid; the constructor is still manually reconstructed and unproven
as an automatic recovery. The next strategy must address inference/accounting
of initialization constants and relative offsets from instructions, rather
than broadening string-loop mutations or counting generated stubs.

### Automatic bounded recovery PoC: close and refill

The runner now invokes replay-bound repair directly after a failed structured
proposal. There is no operator-selected failed seed in automatic mode.
Training chooses the first passing candidate; its held-out evaluation ends
the run whether it passes or fails. Held-out failures never become retry
feedback. Source hashes deduplicate model proposals and repair alternatives;
the already-measured failed seed is replayed, not executed again.

Each run allows at most four local-model requests. Close permits one
return-branch swap per proposal; refill permits five one-field alternatives:
toggle error clearing, change successful count expression, or change return
expression. Offsets and other semantic fields remain unchanged during repair.
These are developer-defined hypothesis spaces, not unrestricted decompilation
or a population-based evolutionary optimizer.

One command per bounded slice, using new empty output directories:

```sh
uv run python tools/liero_four_routine_pilot.py --routine close \
  --automatic-close-repair --output <new-empty-close-directory>
uv run python tools/liero_four_routine_pilot.py --routine read \
  --automatic-read-repair --output <new-empty-read-directory>
```

Both require the BYOD executable, assembler/linker, DOSBox, FPC, objdump and
the local Ollama service. Missing BYOD skips; failed controls prevent proposals.
Schema, original instructions, raw responses, sketches, counterexamples,
compiled candidates, lineage and replay-checked reports remain in the output.
The report distinguishes `selected_by` from `accepted_by`; acceptance here
means only a scoped held-out pass. No repository candidate installation,
source attestation, corpus promotion or model-weight update occurs.

**Measured 2026-10-31, Qwen2.5-Coder 14B instruct, temperature zero:**

| Slice | Fresh model outcome | Automatic repair | Training | Held-out |
| --- | --- | --- | ---: | ---: |
| Close `FUN_24dd_37d3` | One proposal reversed branch returns; 0/8 passed | Return swap, selected without operator intervention | 8/8 | 16/16 |
| Refill `FUN_24dd_375e` | One proposal passed directly | Not needed in the live model trial | 64/64 | 32/32 |

Evidence directories are session artifacts `liero-automatic-close-20261031/`
and `liero-automatic-read-20261031/`. All five close reports and all four
refill reports were independently replay-validated. The four protected
repository includes and recovery ledger hashes were unchanged.
The refill source SHA-256 was
`325914121428dc5eb32a6519cb862ce161fe5b37ff0a173bd5adb9e941183093`.

The close `heldout-v2` suite adds invalid handles 6, 7, 255, 32768 and 65534
before live/repeated/FFFF close, alongside the earlier lifecycle fixture.
Original DOSBox returns 6 for those invalid handles; a live-handle collision
aborts instead of normalizing the handle. The suite rejects a compiled
signed-comparison mutant that would misclassify high-bit handles as reserved.
Legacy `heldout` remains the original payload-only suite; older evidence is
not relabeled as having stronger coverage.

Refill uses the existing disjoint held-out lengths 127/129/257 and capacity
seven. Its supplied topology has one DOS-read call followed by position/count
updates; the model selects four word offsets, error clearing, successful
count value and return value. A separate deliberately wrong `clear_on_error`
fixture failed training; the shared loop selected the toggle alternative,
passing 64 training and 32 held-out calls. This is an integration test of
repair, **not** an additional live model recovery. The host read adapter
aborts requests exceeding its 128-byte reserved buffer rather than allowing
a wrong offset hypothesis to corrupt the host fixture.

This meets the narrow PoC gate: a fresh model-plus-repair close candidate and
an independent fresh refill candidate pass binary-backed scoped oracles
without human semantic intervention during execution. The sketch topologies,
callback abstractions and mutation spaces were supplied by developers.
Finite adapter fixtures do not prove complete DOS semantics, TP7 codegen/ABI
parity, universal routine equivalence, normal-program behavior or automatic
whole-Liero recovery. Other routines remain unresolved; no wider frontier or
model sweep was started. An MVP may package this bounded assisted-recovery
path, but continual model learning remains a separate, unproven milestone.

Validation covers the runner and the shared file-harness callers (read,
close, dispatch, setup, open, line callbacks, buffer and reader/skip probes).
Ruff and Pylance syntax checks pass; deliberate branch, signed-handle and
error-clear mutants are rejected rather than counted as recovered source.

### Two-hypothesis close branch repair

The follow-up consumed the saved failed conditional-sketch candidate, checked
its original-binary report and raw-response/sketch/source correspondence, and
tested exactly two hypotheses in separate current-source snapshots:
the unchanged model sketch and a sketch swapping only `then_return` and
`else_return`. Object offset 0, unsigned `<=` and threshold 4 were unchanged.
No model request, reviewed target-body example or additional mutation was used.

**Measured result:** unchanged failed all eight training calls; swapped passed
all eight training calls and then all eight held-out calls. The passing source
returns zero for handles 0..4 and calls `dosClose(handle)` for larger handles.
The comparison checks returned status, all 512 memory bytes, original stack/
segment preservation, and host adapter call counts. The originally matching
live-handle zero return is insufficient without the required service call.
Only the training-passing hypothesis reached held-out testing.

The rendered passing source SHA-256 is
`ad1ccf5decc2b5bb30d76f570da036b08b229b466d0e4daa7134e81405aedae0`.
Evidence is retained in session artifact
`liero-close-branch-repair-20261031/result.json`, with both selected sketches,
source snapshots and reports. All three fresh reports were replay-validated;
the four repository bodies and recovery ledger hashes remain unchanged.
The fixed two-hypothesis budget is complete and the candidate was not installed
or promoted into recovery, retrieval or training state.

This establishes **scoped repair success for a human-localized branch swap**,
not autonomous model correction, general decompilation or universal routine
equivalence. The shape was already constrained; the host DOS adapter covers
only the tested lifecycle. Held-out changes payload but repeats the same
handles/errors, so the 16 matching calls do not represent 16 independent
behavioral contexts. This result does not retroactively improve the failed
four-routine pilot's model success rate.

Reproduce from the original failed proposal directory in a new output directory:

```sh
uv run python tools/liero_four_routine_pilot.py --routine close \
  --branch-repair-seed <failed-proposal-directory> \
  --output <new-empty-directory>
```

The actionable lesson is to keep binary-tested competing branch hypotheses
instead of asking the same model to repeat a disproven answer. Any expansion
still requires an independently scoped routine and its own acceptance gate.

### Constrained close conditional sketch

The next bounded trial replaced free-form Pascal generation with a strict
five-field JSON sketch: object-word byte offset, unsigned comparison
operator, word threshold, and true/false return expressions. The renderer
supplies the known callback signature, one word load and an `if/else`;
the model chooses each semantic field. Allowed returns are zero, loaded
handle, or the status of one `dosClose(handle)` adapter call. Word alignment,
ranges, exact keys and vocabulary are independently validated before
rendering. Inline assembly, arbitrary helpers and interface changes cannot
be represented.

This is **human-scoped hypothesis selection**, not unrestricted decompilation:
the branch topology, word-read shape and service abstraction are supplied.
The field ranges do not hard-code the correct offset, threshold, branch
direction or return choice. Tests compile both a matching sketch and a wrong
threshold sketch; the original-byte oracle rejects the latter. A structurally
valid sketch is not automatically accepted as behaviorally correct.

Run the same single-routine trial with the current recovered examples:

```sh
uv run python tools/liero_four_routine_pilot.py \
  --routine close --recovered-examples --constrained-close \
  --output <new-empty-directory>
```

**Measured 2026-10-31 result:** both reviewed controls passed eight calls.
Two model requests produced one unique, successfully compiled candidate.
Qwen selected byte offset 0, `handle <= 4`, true return
`dos_close_status`, and false return `zero`: it reversed the reserved-handle
and service-call branches. The candidate failed all eight training calls.
For handles 0..4 it called the host adapter and returned error 6 instead of
the original zero; for the live, repeated-close and invalid handles it
skipped the service call. The live-handle return happened to match zero,
but its required adapter call count was wrong, so that case correctly failed.
All 512 memory bytes remained as expected.

The second request received the original/Pascal return mismatches and host
adapter counts for all training calls, but repeated the identical sketch.
The duplicate gate stopped further requests. No candidate held-out test
ran, no source/ledger/knowledge promotion occurred, and protected repository
hashes remained unchanged. Controls and the failed candidate's saved evidence
were replay-validated against their own immutable workspaces.

The constrained strategy **resolved the compilation/output-language blocker**
for this narrow shape; it did not resolve behavior or establish generalization.
Recovered examples remained `FUN_24dd_4919`, `FUN_24dd_492c` and
`FUN_235c_04f3`, with their prior scope labels. This was not an ablation of
examples versus grammar. Close held-out still varies payload only and repeats
the same handle lifecycle, so it cannot support a stronger independence claim.
Evidence is retained in session artifact
`liero-close-conditional-sketch-20261031/result.json`, with the schema,
raw responses, selected sketches, rendered Pascal and training/control traces.

The next blocking question is the model's branch-direction interpretation and
failure to revise a disproven sketch, not Pascal syntax. Do not expand the
panel or treat compilation as recovery. Any follow-up should discriminate
conditional-jump/fallthrough hypotheses against these existing counterexamples
under a new explicit budget, rather than repeat unmodified prompts.

### Reusing manually recovered routines

Manually recovered routines can supply fixed dependencies and source-level
examples without being treated as universally binary-equivalent. The bounded
pilot now offers an explicit same-target retrieval mode: it audits current
ledger hashes, requires both `source_recovered` and `behavior_verified`,
excludes all four pilot routines, and ranks at most three remaining pairs
using the existing Pascal structural-anchor retriever. The retrieval view is
ephemeral: it does not write to the knowledge store or promote examples for
training. Each retained example records assembly/source hashes and review/
host-validation notes. Prompts label this evidence as static review plus
recorded host tests, **not** original-binary equivalence.

A single close-leaf trial used recovered examples `FUN_24dd_4919`,
`FUN_24dd_492c` and `FUN_235c_04f3`. Its callback type/function signature was
required verbatim, and the prompt specified the available pointer operations
and DOS adapter. The target's own recovered implementation was not supplied
as an example, initial candidate or repair. The checked implementation was
used only as an isolated positive control.

**Measured result: both control suites passed (8 calls each), but all four
model requests were rejected for inline assembly.** The model declared the
requested callback/interface and a valid `^Word` local pointer, but used
`asm; MOV AH,3E; INT 21h` instead of calling the supplied `dosClose` adapter.
The responses repeated this wrong strategy despite rejection feedback.
No candidate was compiled, compared behaviorally, or evaluated on held-out
fixtures. This is an output/interface-adherence failure, not evidence that
the algorithm is wrong or that manual recovery cannot help.

The trial combines recovered examples, exact-interface checking and the
previously repaired compiler feedback; it is not a controlled ablation that
isolates the effect of examples. Compiler feedback was never exercised here
because all proposals failed the earlier source gate. Close held-out still
varies file payload only, not the tested handle lifecycle. No broader run or
extra requests followed the four-request budget. Hashes confirm repository
bodies and recovery ledger were unchanged.

Evidence is retained in session artifact
`liero-close-recovered-context-20261030/result.json`, with the exact retrieved
pairs in `recovered-examples.json`, prompts and raw responses beside the
control reports. Reproduce in a new directory:

```sh
uv run python tools/liero_four_routine_pilot.py \
  --routine close --recovered-examples --output <new-empty-directory>
```

The reusable pieces are the checked dependencies, scoped source examples and
retrieval gates. They do not yet justify a larger model run. The next
discriminator is a materially constrained output strategy that cannot emit
inline assembly while preserving the explicit adapter contract; another
unmodified retry batch is not warranted.

### Four-routine generalization pilot

The bounded pilot in
[tools/liero_four_routine_pilot.py](../../../tools/liero_four_routine_pilot.py)
tested local `qwen2.5-coder:14b-instruct` beyond the favorable shared-copy
example. It generated complete Pascal includes from independently decoded
original bytes and explicit host interfaces, without including the reviewed
Pascal bodies in prompts. Each selected body has no calls to another selected
body; read and close use the existing explicit DOS adapters. Original
constructor/open/setup remain fixture code for the leaf comparisons, not
claims about generated callees.

The fixed panel used at most four requests per routine and stopped duplicates.
Training feedback never included held-out results; a candidate could reach
held-out evaluation only after a full training pass. Reviewed sources first
passed both suites as controls:

| Routine | Training / held-out control observations | Model requests | Unique candidates submitted to FPC | Scoped candidate passes |
| --- | --- | --- | --- | --- |
| `FUN_24dd_3639` constructor | 514 / 264 guarded cases | 4 | 2 | 0 |
| `FUN_24dd_3f86` comparator | 9 / 64 string cases | 4 | 0 | 0 |
| `FUN_24dd_375e` refill | 64 / 32 calls | 3 | 2 | 0 |
| `FUN_24dd_37d3` close | 8 / 8 calls | 4 | 1 | 0 |

Constructor training uses the zero/ones arenas and the earlier named
fixtures; held-out uses patterned arenas and embedded-NUL fixtures. Refill
held-out selects lengths 127, 129 and 257 plus capacity 7 from the existing
corpus. Close held-out changes the file payload to all 256 byte values but
repeats the same handle lifecycle; it is **not** independent coverage of
new handle/error behavior. These partitions were selected before generation,
not in response to candidate outcomes.

**Measured result: 0/4 routine passes, 0/5 successful candidate compilations.**
Fifteen model requests produced eight directive/inline-assembly rejections,
five unique candidates rejected by FPC, and two duplicates. Constructor
drafts invented helpers such as `PushDS`, `LES` and `STOSW`. Comparator drafts
continued to emit forbidden inline assembly. Read/close drafts omitted
required callback types or used invalid Pascal pointer operations. No
generated candidate reached behavioral comparison or held-out evaluation.
This tests the current output/interface pipeline and does not establish that
the model cannot recover these algorithms.

The run also exposed a repair-feedback defect: compiler logs were retained,
but retries received only the failed command/exit status rather than actual
FPC diagnostics. The runner now forwards captured compiler diagnostics;
regression tests check the next prompt. It also retains malformed raw model
envelopes and uses separate immutable control/per-candidate workspaces.
Those runner improvements are tested, **not** a new measured model success;
no extra requests were made after the pilot exhausted its budget.

All eight saved controls were replay-validated, and hashes confirm that the
four repository bodies and recovery ledger were unchanged. The run stopped
below the 25% yield floor; no larger run, model sweep or promotion followed.
The next bounded question is whether enforcing the declared interfaces and
providing actual compiler diagnostics can produce a compilable non-copy
candidate, not whether more unattended requests can inflate recovery counts.

Evidence is retained in the session artifact
`liero-four-routine-pilot-20261030-v3/result.json`, with raw responses,
original-byte disassemblies, compiler logs and isolated workspaces beneath
each panel entry. Two preparation attempts were blocked before model use:
the first encountered an unrelated unreadable core dump during an overbroad
snapshot; the second used an escaping BYOD symlink rejected by the existing
path validator. Source-only snapshots with a contained executable copy
resolved these preparation errors without weakening the validator.

The control preflight also found that the file-probe image loader attempted
to include newly recorded cross-segment caller/filename regions and
allocation-failure paths inside its COM harness. Its checked-region selection
now explicitly includes only the file fixture's successful-allocation paths.
The underlying whole-program evidence validators are unchanged; external
caller preparation and allocation-failure behavior remain outside this
fixture's contract. The original constructor/refill/close/file controls and
affected probe regression tests pass after that correction.

Reproduce the bounded pilot with a new output directory:

```sh
uv run python tools/liero_four_routine_pilot.py --output <new-empty-directory>
```

Default full-corpus probe behavior remains unchanged. This pilot is finite
host-Pascal/original-byte evidence, not TP7 ABI equivalence, normal startup,
routine-wide source recovery, or model-weight learning.

### Bounded model-generated copy repair

The original-byte probe in
[tools/liero_copy_routine_probe.py](../../../tools/liero_copy_routine_probe.py)
binds the tested instructions and source data to LIERO.EXE SHA-256
`e45653ab0f915238f7394b2846b70288d0cc35a2595debc2a49502078398c7d1`.
It executes both entry paths in a controlled COM image. Training used DI
`$0200` and `$FFFA`; held-out used DI `$0000` and `$000C`. Each entry was tested
at both offsets, comparing copied memory and redzones, AX/CX/SI/DI, preserved
segment/stack state, and CF/ZF/DF.

The checked-in includes originally failed all four training cases only because
AX remained at the source start. A schema-constrained Qwen 2.5 Coder 14B request
produced one unique candidate, which passed all four training cases and all
four held-out cases. Its assembly-derived AX source-end adjustment has now been
integrated into both includes. The final checked-in sources pass both suites
against the original executable; positive controls and candidate reports were
also replay-validated.
The integrated-source reports are retained under
`build/copy-parity/integrated-source-20261030-training/` and
`build/copy-parity/integrated-source-20261030-heldout/`. Recovery audits now
discover these reports, replay both suites, and reject evidence if either
include or the shared runtime no longer matches the saved source hashes.
The measured audit counts two scoped differential routines (four training
and four held-out cases across the pair); both remain `in_progress`.
This does not change the whole-routine original-binary or source-recovery
counts. Four unrelated older constructor/comparator reports remain invalid.
The combined host runtime test still stops at the earlier comparator
`Halt(97)` before reaching the copy tests; the isolated copy probe compiles
and executes the current includes independently of that blocker.
The run used one unique candidate (candidate SHA-256
`69a86524912d6cef214703c298373828661e5f7f088c3104b14b5dc3dd56485c`); its
raw completion SHA-256 is
`77528bc167fecd74298bb219181d2309081a59c2e9cde958a1e4adbbe30da7e2`.
Re-run with `uv run python tools/liero_copy_routine_probe.py --output
<new-empty-directory> --model qwen2.5-coder:14b-instruct`. This requires the
local model endpoint, GNU `as`/`ld`, DOSBox, Free Pascal, and the BYOD
executable.

This is a scoped behavior result, not a routine-wide equivalence claim. The
COM harness controls the initial segment/register state; only the selected
fixtures and defined CF/ZF/DF flags were compared. The includes were corrected,
but their recovery-ledger status remains in progress; this trial does not by
itself justify routine-wide source recovery. It demonstrates structured
drafting plus oracle feedback, not online model-weight training or durable
model improvement as new projects are added.

`FUN_24dd_04dc`, `FUN_24dd_4919`, `FUN_24dd_492c`, `FUN_235c_04f3`,
`FUN_24dd_3e63`, and `FUN_24dd_3e7c` currently have source-recovery and
behavior-verification attestations in the ledger. `FUN_24dd_04dc` is pure
register arithmetic; its exhaustive instruction-level host test is sufficient
for this model, and no original-binary parity claim is made. The shift routines
preserve the returned AX word and full DX:AX result; processor flags are not
modeled. `FUN_24dd_40d6`,
`FUN_24dd_3d68`, and `FUN_24dd_4905` host tests exercise memory effects but do
not establish the full segmented-pointer and processor-register behavior
visible in their assembly; those routines are not counted as recovered or
behavior-verified. `FUN_24dd_492c` is modeled over the runtime's logical
DS-relative memory; its assembly caller reinitializes the clobbered ES/DI
state before relying on those registers.

The string helpers `FUN_24dd_3e95`, `FUN_24dd_3eaf`, and `FUN_24dd_3ed3` copy
length-prefixed byte strings, with the latter two applying a maximum length or
start-position/length slice. Host tests exercise these data effects with linear
pointers. Original-binary probes are still needed to verify 16:16 far-pointer
behavior and register/ABI effects; these routines are source-recovered but not
counted as behavior-verified.

`FUN_24dd_3fb1` writes a two-byte length-prefixed value (`1`, then the supplied
byte). Its guarded host pointer test passes; far-pointer and register/ABI effects
remain unverified against the original executable.

`FUN_24dd_3fc3` writes the low byte of a 16-bit count followed by exactly that
many bytes from the source, including counts above 255. Host tests verify both a
short copy and the 256-byte wrap case. Far-pointer and register/ABI effects
remain unverified against the original executable.

`FUN_24dd_3f86` compares length-prefixed strings through their shorter length.
The host model reads both strings through packed 16:16 pointers, wraps 16-bit
offsets and 20-bit physical addresses, and mirrors the comparison's zero and
carry flags. A hash-bound DOSBox/original-byte versus compiled-Pascal probe
passed nine paired fixtures covering empty/equal strings, both byte orderings,
unequal lengths, embedded zero bytes, and 255-byte strings. It checked only
ZF/CF, far-call stack balance, and non-mutation of each tested 256-byte region.
The mismatch carry direction follows `CMPSB`'s source-minus-destination
comparison; this probe exposed and corrected the earlier reversed Pascal model.
The recovery audit records this as a scoped differential pass, not routine-wide
behavior verification. Other CPU flags, arbitrary aliasing/wrap cases, and
normal game startup remain unverified.

Reproduce the scoped comparison and have the recovery audit validate the saved
report with:

```sh
uv run python tools/liero_compare_routine_probe.py \
  --output targets/liero/build/comparator-parity/FUN_24dd_3f86-9cases
uv run python -m engine.recovery --target liero
```

A separate live-model trial started from a checked-signature skeleton in a
disposable target copy, with this routine marked unreviewed only in that copy.
`qwen2.5-coder:14b-instruct-q4_K_M` preserved the required `Longint` declaration
but emitted invalid host-pointer casts instead of using `RealModeMemory`. The
same candidate hash (`fc3fb62038ef6de4f07d6cac0a48da89875f25bf4571710d2474c6dc788c219d`)
was produced for all three bounded attempts; FPC rejected it at line 48 with
incompatible `Char`/`^Byte` types and a subsequent syntax error. Since no
candidate compiled, the routine comparator was correctly not run. The loop
recorded three rejected attempts and stopped at its cap; it produced no scoped
pass or verification claim. The repository's checked implementation remained
unchanged and continues to pass the nine-case control above. The live-model
attempt is therefore an unsuccessful end-to-end demonstration, not evidence
that generation can yet repair this ABI/runtime mismatch.

A follow-up disposable PoC run (`20261030T155158.932446Z-a52494d7`) used a
corrected contract prompt that prohibited host pointers, documented the
`RealModeMemory` access pattern, mapped ZF/CF to `RegisterZeroFlag` and
`RegisterCarryFlag`, and exposed retry temperature and captured prompt hashes.
All five drafts compiled and reached the original comparator, but produced the
same candidate hash
(`14702a8f10916f1c98ade2fa1c1b900ce0fd928f86cb1d20d96481c25ea8ca3c`).
Each comparator run checked all nine cases and passed only `dest-greater`;
eight cases returned incorrect ZF/CF values, while stack balance and tested
memory preservation passed. The saved first-attempt report replay-validated as
failed with 1/9 cases passing. Attempts 2–5 received the measured mismatches
and previous candidate, but repeated the same output. The live PoC therefore
still fails, and the 0/5 draft hit rate is below the project's 25% floor. Stop
here: do not increase retries, widen the routine set, or package this as an MVP.
The next experiment needs a materially different generation/repair strategy
or model. The checked repository include remained unchanged
(`5131a7796ac1261be2d8b989c6fde382eed43426d9ae83e7502e5e1f758daf19`).

A third isolated live trial (`20261030T171741.903602Z-ee7e260a`) supplied the
assembly-derived branch behavior and all nine original-trace ZF/CF outcomes
directly to `qwen2.5-coder:14b-instruct-q4_K_M` at temperature 0. The first
candidate was compiled and executed by the strict routine comparator, but
passed only 5/9 cases. It failed `equal`, `dest-greater`, `source-shorter`, and
`equal-maximum-length`; stack balance and tested-memory preservation passed in
all nine cases. The generated Pascal set `srcLen := 0` before the repeat loop
in both branches, then exited before assigning flags, so it did not implement
the observed compare behavior. The report replay-validated as failed with 5/9
passes against the candidate snapshot and the manifest-bound executable.

Attempt 2 received the measured mismatches, but returned the exact same
candidate and completion hashes as attempt 1 despite a changed prompt. The
duplicate-candidate guard stopped the run after two attempts. Its summary has
zero scoped passes and `stop_reason: duplicate-candidate`; this is evidence
that feedback delivery and duplicate stopping work, not that the model learned
the routine. The 0/1 candidate hit rate remains below the 25% floor: do not add
retries or widen the target set. A materially different repair method or model
is required. The reviewed include still hashes to
`5131a7796ac1261be2d8b989c6fde382eed43426d9ae83e7502e5e1f758daf19`, and the
main recovery ledger matches the pretrial snapshot.

`FUN_24dd_3f40` searches a length-prefixed byte string for a nonempty
length-prefixed pattern and returns its 1-based payload position, or zero when
no match is possible. Its host model handles packed far pointers, 16-bit offset
wrap, and 20-bit physical-address wrap. Tests cover later matches after a
partial candidate mismatch, absent/empty/oversized patterns, and offset wrap.
Original-executable parity remains unverified.

`FUN_24dd_3f14` appends a length-prefixed source string to a length-prefixed
destination, saturating the destination length at 255 and copying only the
remaining capacity when the sum overflows. Host tests cover ordinary append and
the saturation boundary; far-pointer and register/ABI effects remain unverified.

`FUN_24dd_40ac` formats a 32-byte field as leading zero bytes, a source byte
sequence, and trailing zero bytes based on the high and low bytes of its count
argument. A guarded host test covers a two-byte prefix and three-byte payload;
far-pointer and register/ABI effects remain unverified.

`FUN_24dd_4181` ORs 16 source words into the corresponding destination words.
The host test checks all 16 results and guards both sides; segmented pointer
behavior is not established by this host-only test.

`FUN_24dd_4161` maps a byte coordinate to an in-range bitmap row and rotates
the selected byte by the pixel's bit offset; out-of-range coordinates return
the sign-derived sentinel from the assembly path. Register-state tests cover an
in-range coordinate, a lower-bound miss, and the negative-input fallback.
Processor flags and original-binary behavior remain unverified.

`FUN_24dd_40ec` sets one bit in a real-mode far-pointer bitmap. The host runtime
models the 20-bit physical address space and 16-bit offset wrap, and tests cover
both the bit mask and offset wrap. This does not yet attest CPU flags or compare
the behavior with the original executable.

`FUN_24dd_3b22` initializes a 48-byte little-endian header (`0`, `$D7B0`, then
22 zero words) and appends up to 79 bytes from a length-prefixed source, stopping
at an embedded NUL and writing a terminator. Host tests cover the header, normal
copy, 79-byte cap, and early-NUL behavior through packed far pointers. The
original executable has not been run.

`FUN_24dd_3d36` scans the DOS command-line buffer at `ES:$80`, counts
space-delimited nonempty arguments, and stops when the input count in `DX`
reaches zero or the buffer length is exhausted. `FUN_24dd_3d2f` initializes
`DX` to zero, invokes that scan, and returns the total token count in `AX`.
Host tests cover whitespace, three arguments, an explicit one-token limit, and
an empty command line using the simulated real-mode memory. Original-executable
parity remains unverified.

`FUN_24dd_3d80` multiplies the two 32-bit operands held in `DX:AX` and `BX:CX`,
returning the low 32 result bits in `DX:AX`. The host model checks the split
register result in both the 16-bit and 386-mode branches, including a product
that carries into the high word. Original-executable parity remains unverified.

`LieroRuntime.pas` contains host-side logical mirrors for a small subset of
the original segment-relative globals and a 64 KiB single-segment memory model
used by the stack-copy routines, plus a separate 64 KiB code-segment image for
`FUN_24dd_0642`. These variables do not reside at the original DOS addresses.
DOS interrupts, far-call ABI, hardware I/O, and general
segment:offset pointer behavior are not emulated beyond the specific
`FUN_24dd_3f86` and `FUN_24dd_40ec` memory operations described above.
`RegisterWordESDIPlus2`
represents the value loaded from the implicit `ES:DI+2` operand, and
`RegisterZeroFlag` and `RegisterCarryFlag` preserve selected compare results
for their callers.
The file-control builder uses `RegisterES` and `RegisterDI` as the logical
destination segment and offset; its host pointer is only the backing storage.
The routines listed above remain unverified against LIERO.EXE; the host
Free-Pascal harness checks the stated local behavior, not game parity.

## DAT file coverage

The DAT model exposes 20 documented bytes as typed settings and preserves the
other 135 bytes opaquely. A byte-exact round trip establishes lossless
preservation, not semantic understanding of the opaque portion.

## Autonomous compile-gated iteration

`engine/improve_loop.py` processes a small batch of assembly-backed functions
at a time. For each candidate it preserves the prior source, asks the local
model to draft or retry one Pascal routine, and compiles the full target before
accepting the change. Compiler diagnostics and the previous candidate are
available to the next attempt. A failed candidate is rolled back; the loop
stops at its iteration/attempt bounds or after a configurable number of
iterations add no new compilable routines.

Candidate order is dependency-first. Direct in-target callees are extracted
from assembly; callers are deferred until those callees have hash-current
`source_recovered` attestations. A compile pass alone does not unlock dependent
callers. Mutually recursive functions are treated as one dependency group, and
the loop reports when remaining callers are blocked on unresolved routines.

Routine compile evidence is gathered by changing one routine at a time and
building it in the target's shared Pascal declarations/runtime context. The
final whole-target build is reported separately. A routine counts as
meaningful only when it contains a non-skeleton Pascal body; a compiling
skeleton is not an implementation. The FPC `-Mtp` build checks compatibility,
not execution under DOS. `dat-parity` remains a DAT-format check, and neither
it nor compile success marks a routine as verified against `LIERO.EXE`.

Run `make improve TARGET=liero` to use the loop directly. Bounds and model
options are configurable with `MAX_ITERATIONS`, `SATURATION_WINDOW`,
`FUNCTIONS_PER_ITERATION`, `MAX_ATTEMPTS_PER_FUNCTION`, `MODEL`, and `LLM`.
By default it uses the local Ollama endpoint at `http://localhost:11434` and
the `qwen2.5-coder:14b-instruct-q4_K_M` model; `LSR_LLM_ENDPOINT` and
`LSR_LLM_MODEL` override these defaults.
The summary keeps generated, meaningful, compilable, whole-target-buildable,
and binary-verified counts distinct. Missing compiler/model infrastructure is
reported as a blocker rather than a saturated success.
It also reports `functions_source_recovered` and `evidence_accounted_percent`
from the recovery ledger. Those values require reviewer-attested evidence and
matching source/assembly hashes; they are not inferred from compilation or the
selected format oracle. If the ledger is absent, source-recovery metrics are
reported as unavailable rather than zero.

The loop does not automatically prove that a generated Pascal body matches
assembly-level control flow, call targets, or state effects. A successful
compile or DAT-format check is only an intermediate result. The current Liero
diagnostic pilot used a single candidate iteration; broader runs should wait
until a separate semantic acceptance gate is available.

## Local candidate-setting experiments

Install the optional experiment dependency alongside the existing development
and training extras with
`uv sync --extra dev --extra training --extra experiments`, then run
`uv run --extra dev --extra training --extra experiments python tools/liero_candidate_experiment.py`.
The default sweep compares two installed Ollama models, learned-context versus
base prompts, and temperatures `0.0` and `0.3` across four size-stratified
routines, including `FUN_24dd_0582`. The defaults can be changed with
`--models`, `--prompt-profiles`, `--temperatures`, `--functions`, `--panel-size`,
and `--max-tokens`.

Each trial uses a clean scratch copy and logs its prompt, raw completion,
sanitizer result, candidate source, compiler output, model digest, and input
hashes to a local SQLite MLflow store and local artifacts under `mlruns/`.
The comparison report is written to a unique timestamped directory under
`reports/liero-candidate-experiment/`. The baseline build is reported
separately. A candidate build is attempted only when the sanitizer accepts a
draft that actually changed the routine; otherwise the build status is marked
skipped, not passed. Accepted candidates get one bounded compiler-feedback
retry by default; `--compile-repair-rounds` changes that bound. Candidates are
ranked only by sanitizer acceptance and candidate-specific whole-target
compilation; neither result proves semantic equivalence or permits automatic
promotion into the target source or knowledge base.

## Localized repair PoC result

The bounded localized-repair trial (`20261030T184122.059854Z-50f36e52`) used
`qwen2.5-coder:14b-instruct-q4_K_M` at temperature 0 with at most two attempts.
The full first draft compiled and passed 5/9 comparator fixtures. The localized
retry compiled and passed 3/9. Both saved reports replay-validated; neither
candidate passed the scoped oracle. The retry changed only the contract's
selected 54-line comparison/flag region, preserving the source around it, but
the fixture result regressed rather than improved. Stack balance and tested
memory non-mutation passed for both candidates. The first draft failed
`equal`, `dest-greater`, `source-shorter`, and `equal-maximum-length`; the
localized retry failed `equal`, `dest-less`, `source-shorter`, `embedded-zero`,
`equal-maximum-length`, and `late-mismatch`. The retry prompt contained those
measured mismatches and the previous candidate. Inspection of the retry shows
the loop still tests its decremented length after reading another byte, and
the final flag assignments use that mutated loop counter and overwrite the
mismatch-path flags. This is consistent with the observed failures; it is not
a claim about untested paths.

This demonstrates that counterexample feedback reached a bounded patch and
that the patch boundary was enforced; it does not demonstrate an effective
repair strategy. With 0/2 candidates passing, the observed yield is below the
25% floor. Stop this strategy here rather than increasing retries or expanding
the target slice. No candidate was promoted, and no routine-wide recovery
claim follows. The checked main-worktree include and ledger were unchanged
(`FUN_24dd_3f86.inc` SHA-256
`5131a7796ac1261be2d8b989c6fde382eed43426d9ae83e7502e5e1f758daf19`;
`recovery.json` SHA-256
`10367d3a953442f6275c1c733b96bf4755dc06207dee8bba495549b72a145c09`).
Candidate source hashes were `fa6643b489a2f874a9d35bb2461d9877a11918d01ecd68bf0d5fba7afd0dd298`
and `306e2486c00a31aae9a53d7853c80cb393c0d811cdad900a89db240c638a0b94`.

## Evolutionary-search controls and results

The initial positive-control gate exposed an error in the checked comparator:
the zero-common-prefix path failed to reflect the source-minus-destination
length comparison. The earlier source (`5131a7796ac1261be2d8b989c6fde382eed43426d9ae83e7502e5e1f758daf19`)
passed 9/9 training fixtures but only 56/64 held-out fixtures. The eight
failures were `heldout-01`, `heldout-02`, `heldout-17`, `heldout-18`,
`heldout-33`, `heldout-34`, `heldout-49`, and `heldout-50`; they covered
empty-vs-nonempty strings and preserved stack balance, pointer identity, and
tested memory. The routine's early return was corrected before the search.

The corrected checked source
(`fbdc49e7b97348d15597ae83540a6a160beb3977acc6f9e2c3afde2db06ca863`) passed
both fresh positive controls: 9/9 training cases and 64/64 held-out cases.
The fixture suite IDs and hashes remain
`liero-compare-train-v1` / `a6007c775192c785faf2d6f0753c60d9a330de1860f6d4fbf35f6fb102f4c61b`
and `liero-compare-heldout-v1-seed-20261030` /
`20d9671a6da2f934c1da636b843d0999c2d1242f9b9934eafd71068a1cf6071d`.

The bounded run `run-20261030T1952f` used a fixed seed, up to four generations,
population size eight, 32 unique evaluations per arm, and 64 proposals per
arm. Its 30 saved comparator reports (two controls and 28 candidate
evaluations) passed replay validation. The deterministic arm evaluated 26
unique candidates; its best candidate passed 6/9 training fixtures (15
matching defined flag bits), improving on the best seed's 5/9 but not reaching
the 9/9 gate. The LLM-assisted arm evaluated only its two seed candidates. All
64 model proposals were rejected because the response was not valid JSON, so
no LLM-generated mutation reached the oracle. The raw malformed completions
were not retained, which prevents diagnosing the response-format failure from
this run alone.

Neither arm produced a candidate eligible for held-out evaluation. Candidate
hit rate was 0% for both arms, below the project's 25% floor. No candidate was
promoted and no routine-wide recovery claim follows. Do not widen or repeat
this search unchanged. A subsequent bounded trial should first improve the
LLM proposal interface and preserve rejected completions for diagnosis; use
assembly-derived behavior and human review to guide any new mutation strategy.
The checked main-worktree include and recovery ledger were not changed by the
search (`FUN_24dd_3f86.inc` SHA-256
`fbdc49e7b97348d15597ae83540a6a160beb3977acc6f9e2c3afde2db06ca863`;
`recovery.json` SHA-256
`10367d3a953442f6275c1c733b96bf4755dc06207dee8bba495549b72a145c09`).
These results are scoped to the listed comparator fixtures.

## Concrete stack-object argument handoff

The audit's `object_identity_chains` section binds the entry of
`FUN_1000_a816` (`1000:A816`) and its checked body (`1000:A836` through the
call at `1000:A874`) to the executable hash, exact instruction bytes, exported
instruction boundaries, and all twelve far-call segment relocations. The
entry-prefix check confirms a `206h`-byte local stack reservation and the
filename-check branch: nonzero `AL` reaches `A836`, while zero jumps to the
function epilogue at `A8F3`. With the caller-tail evidence linked, both targets
must land on reviewed instruction boundaries. The allocation call at `A81C`
is linked by its relocated far pointer to `FUN_24dd_0530` (`24DD:0530`).
The caller loads `AX=206h`, calls the helper, then reserves `206h` bytes from
SP. The helper's 24 bytes match the original image and exported instruction
boundaries. Its checked instructions add `200h` to AX, compare against SP and
`DS:[640Eh]`, and return through `RETF` on the normal path without removing
caller arguments. The failure path sets `AX=00CAh` and jumps to `24DD:010F`.
That four-byte transfer stub pops the far-call return IP and CS into CX and BX,
then short-jumps to `24DD:011A`, an instruction boundary inside
`FUN_24dd_0116` (also addressed as `2000:4EEA`). Its checked 22-byte entry
prefix loads the relocated data segment into DS, enables interrupts, stores
the error code at `DS:[6406h]`, and tests `CX | BX`. For the call from
`1000:A81C`, the popped return address is `1000:A821`, so that zero branch is
not taken. The following instructions test `DS:[63E4h]`; its value and branch
outcome are unknown. Its zero-branch target is `24DD:015F`, checked as an
instruction boundary inside the same handler export. The checked zero path
stores the return IP at `DS:[6408h]`, stores
`1000h - DS:[640Ch] - 10h` at `DS:[640Ah]` with 16-bit arithmetic, then loads
`ES:BX` from `DS:[6402h]` and tests `ES | BX`. The pointer value and the
resulting branch are unknown; the zero branch targets `24DD:018B`. That
checked path calls `FUN_24dd_3711` with `DS:78F0h` and `DS:79F0h`, then
processes interrupt vectors using a table at `DS:7AF0h`, handler offsets at
`CS:0239h`, and `INT 21h/AH=25h`. Its next test ORs `DS:[6408h]` with
`DS:[640Ah]` and branches to `24DD:01E9` if zero. The outcome remains unknown
because it follows helper and interrupt calls whose effects are not covered
by this evidence. Code after that branch remains unreviewed. These are static
linkage and control-flow findings, not execution or a promotion of the helper.

The filename call at `A82A` is linked by its relocated far pointer to
`FUN_202c_0843`: `2000:0B03` and `202c:0843` are real-mode aliases for the same
address. Its complete 106-byte body and four internal far-call relocations
match the original executable and exported instruction boundaries. The body
copies the supplied path, invokes four subordinate routines, and returns with
`RETF 4`. Its checked control flow sets `AL` to zero when the final subordinate
call returns nonzero `AX` or the copied path begins with NUL; otherwise it sets
`AL` to one. The subordinate routines' meanings and side effects remain
unverified, so this does not establish file-existence semantics or the
filename helper's runtime behavior. The caller body tracks the symbolic
argument stack:

- The constructor receives object `SS:(BP-0104h)` and filename `CS:A80Ch`.
- The input-open wrapper receives that same object pointer.
- The string reader `24DD:3988` receives the object, destination
  `SS:(BP-0204h)`, and maximum length `FFh`.
- The reader loads its object from `[BP+0Ch]` and returns with `RETF 6`.
  This removes the destination/count arguments but leaves the object's
  four-byte far pointer on the caller's stack.
- The immediately following `24DD:38F0` loads the retained object from
  `[BP+6]` and removes it with `RETF 4`. No new object pointer is pushed
  between these two calls.

The complete reader, line-skip, and status-helper bytes are checked alongside
the caller slice. The status helper `24DD:04F4` returns directly without
writes only on `DS:[6410h] == 0`; its nonzero-status path jumps outside the
reviewed region. The caller's sole direct memory store in this slice is the
two-byte loop counter at `SS:(BP-2)`, not a method-slot write.

This is **conditional argument-identity evidence**, not a proof of continuous
method-slot state. Constructor stack cleanup remains an explicit callee
summary; input-open now links to the same-binary lifecycle evidence below,
including its checked `RETF 4`. Normal returns must preserve BP/SS and live
argument words. External effects and destination writes must not alias the
object or stack. No indirect call or routine is promoted by
this evidence; the audit retains 13 unresolved transfers, 26 source-recovered,
10 behavior-verified, and zero original-binary-verified routines.

The entry-prefix check closes the previous static gap between
`FUN_1000_a816` and the reviewed post-gate body. It does not execute the
allocation helper or the filename helper's subordinate routines, and it does
not cover the shared error continuation or the filename helper's failure-side
effects. No helper is promoted as behavior-verified.

### Checked input-open, close and reopen effects

The setup protocol's optional `input_lifecycle` report checks six additional
byte streams: input-mode entry `24DD:36B7`, common open `24DD:36C4`, close
`24DD:3711`, indexed dispatch `24DD:374D`, input method `24DD:375E`, and close
method `24DD:37D3`. Every instruction is matched against its independently
decoded template, all direct edges reach reviewed instruction boundaries,
and no MZ relocation may overlap these streams. The existing setup evidence
supplies the input method-slot outcomes.

A bounded path interpreter follows the closed/input-mode branches of the
open/close wrappers. It composes setup success/failure and close method
zero/nonzero returns, retaining each path rather than silently dropping
failure states:

| Starting state and operation | Conditional normal-return effects |
| --- | --- |
| Closed (`D7B0`), open for input | Clears buffer words `08h` and `0Ah`. Setup success installs read `24DD:375E` in slot `14h`, null slot `18h`, close `24DD:37D3` in slot `1Ch`, and leaves mode `D7B1`. Setup failure changes mode back to `D7B0`, records the error, and retains the prior method slots. |
| Input (`D7B1`), close | Dispatches slot `1Ch`, then marks the object closed even if the close method returns an error. It does not erase the method pointers. Handles at most 4 bypass the DOS close interrupt; other handles use DOS AH=`3Eh`. |
| Input (`D7B1`), reopen for input | Calls close, preserves the requested input mode across that call, resets buffer words, and calls setup **even after a close error**. Failed setup retains the old pointers but leaves mode closed. |
| Invalid open mode / already-closed close | Returns without calling setup/methods, writing status `66h` / `67h` respectively. |

The indexed dispatcher saves and restores `ES:DI` around its far method call
and records nonzero AX in `DS:[6410h]`. A zero AX does **not** clear an earlier
status. Consequently, successful setup after a failed close can install the
input methods yet still leave a close error for the caller's status check.

The checked input method writes only object words `0Ah` (read count or zero)
and `08h` (zero); the checked close method performs no direct object writes.
Neither writes the method slots. These are conditional static effects:
normal DOS returns must preserve the stated registers and stack, DOS open
errors must return nonzero AX, and all external/buffer/status writes must
remain non-aliasing. Output-mode flush/close, arbitrary replaced methods,
full caller-loop slot continuity, and actual DOS behavior are not proved.
The lifecycle evidence alone does not establish cross-callee method-slot
preservation. The optional caller-loop composition below supplies a scoped,
conditional continuity statement.

### Post-gate caller-loop continuity

The object-identity record's `loop_regions` now extends the checked caller
from `1000:A836` through its return at `1000:A8F4`, ending at `1000:A8F7`.
This includes both reading loops, the reopen, intervening PRNG call, and
final close. It deliberately excludes the function's earlier stack-allocation
and existence-check calls; reaching `A836` with a valid allocated frame
remains an assumption.

`engine/object_loops.py` checks exact bytes and instruction partitions for
the caller tail, constructor tail, PRNG wrapper/core, dispatcher, refill and
optional-method wrappers, and the two callback families used here. It reuses
the existing reviewed dispatcher partition and restricted callback decoder.
All direct local branches/near calls target reviewed boundaries. Every
far-call segment operand has exactly one MZ relocation, with no other
relocations allowed to rewrite the checked streams.

A finite symbolic argument-stack traversal explores both outcomes of each
caller conditional and reaches fixed points at both loop backedges:
`1000:A881 -> A85B` and `1000:A8E1 -> A8B2`. It checks all 14 static call
sites, including both retained-object reader/skip handoffs, and an empty
argument stack at the caller's return. This is not a loop-termination or
input-feasibility proof.

The checked write footprints narrow the remaining alias conditions:

- The caller's direct word stores/increments touch only `BP-0206h`,
  `BP-4`, and `BP-2`, outside the file object at `BP-0104h..BP-5`.
- The first destination, including its length byte, occupies
  `SS:(BP-0204h)..(BP-0105h)` under the stated valid-buffer conditions.
- The second destination is `DS:(66ECh + byte_argument * 15h)`, with a
  maximum 20 data bytes plus its length byte. Across byte arguments 0..255,
  the destination offsets are contained in `66ECh..7BEBh`.
- The intervening PRNG wrapper calls a checked core whose direct writes are
  the two words `DS:[6412h]` and `DS:[6414h]`; it has no object-relative stores.
- Reachable callback entries are `24DD:390E`, `24DD:3923`, and
  `24DD:39AB`. Their only data stores are byte stores to the supplied
  destination, not object-relative method-slot stores.
- The checked constructor tail returns with `RETF 8` and joins the
  previously checked initialization prefix. The checked input method writes
  only buffer-state words, and the dispatcher writes the consumed-buffer
  offset and global error status.

When this evidence is linked to the checked input lifecycle for the same
binary, the audit labels method-slot preservation
`conditional_for_post_gate_caller`. Both opens must succeed, status-check
calls must return on zero status, and the established input methods must be
the methods invoked. In that state, the line-skip routine's guard sees the
null segment in slot `18h`, excluding its optional slot-`18h` call. Final
close marks the object `D7B0`.

This closes the local static call/write chain, **not the runtime alias
question**. Real-mode physical addresses derived from DS and SS can alias
despite distinct segment:offset expressions. The PRNG/status/global-string
storage must not overlap the stack object or live arguments; filename,
DOS-buffer and callback writes must remain valid, nonwrapping and
non-aliasing. Normal DOS/register preservation, immutable code, and valid
buffer/count state remain explicit assumptions. Without linked lifecycle
evidence, the same loop check is labeled `unlinked_callee_summaries` and does
not promote slot continuity. No global indirect call is resolved and no
source or behavioral recovery count increases.

### Original-byte DOS file-I/O observation

`tools/liero_file_probe.py` now runs a narrowly scoped DOSBox COM harness
assembled from `tools/liero_file_probe.S`. It copies only hash-validated,
reviewed routine regions from the user's executable into their original
code-segment offsets. The five checked segment immediates are relocated to
the harness's actual CS. The original executable and extracted files are
never modified, and no executable bytes are committed with the probe.

Run with GNU `as`, GNU `ld`, and DOSBox installed:

```sh
uv run python tools/liero_file_probe.py --output reports/liero-file-probe-run1
```

The output directory must be new. A missing BYOD executable produces an
explicit `skipped` result. Missing tools, stale evidence, emulator failure,
missing/partial snapshots, or unexpected observed values fail the run rather
than producing a successful report. DOSBox is bounded by a 30-second timeout
per fixture and mounts only the fixture directory.

Two deterministic fixtures execute the original constructor, input-open,
string-reader, line-skip, reopen and close code using actual DOS file services:

| Fixture | Observed result |
| --- | --- |
| `ALPHA\r\nBETA\r\n` | Reads `ALPHA`, skips CR/LF, reads `BETA`, reopens and reads `ALPHA` again. Final close changes mode to `D7B0`; status remains zero. |
| 127 `A` bytes followed by `\r\nBETA\r\n` | First read stops at buffer offset 127 of 128. Line skip crosses the refill boundary and consumes LF in the next buffer, leaving offset 1 of 7. The following read returns `BETA`. Reopen reproduces the first line. |

Each fixture retains ten 532-byte binary snapshots. They capture CS/DS/SS,
BP/SP, flags, status, the complete 256-byte stack-local file object, and the
256-byte string destination. Checked observations include the four-byte
object argument retained after the string reader, restored SP after skip,
the internal buffer pointer, mode changes, and unchanged input method slots
through final close. `result.json` includes hashes of the original executable,
assembly source, assembled harness, generated COM, input fixtures, and traces.
The output also retains emulator logs and exact emulator commands.

**Scope:** this is `isolated_original_bytes_dosbox`, not normal `LIERO.EXE`
startup. The harness deliberately establishes its segments and frame; its
observed equal CS/DS/SS does not establish the game's segment layout or
non-aliasing. It does not execute the full caller, establish error-path
coverage, compare reconstructed Pascal, or permit source/original-binary
ledger promotion. It supplies real original-code DOS I/O observations to use
as a bounded reconstruction reference. The recovery counts remain unchanged.

### First original-versus-Pascal constructor contract

`tools/liero_constructor_probe.py`, its small COM harness, and
`tests/probe_liero_constructor.pas` now compare original `24DD:3639` with
the actual reconstructed Pascal include. The candidate runs under host FPC;
it is not a second hand-written reference implementation.

```sh
uv run python engine/verify.py --target liero --oracle constructor-parity
```

The fixed corpus contains 778 cases: all 256 declared short-string lengths
under zero, all-one and patterned initial memory; eight embedded-NUL
positions; and the `INPUT.TXT` constructor inputs from both earlier file-I/O
fixtures. The whole 256-byte name storage, 256-byte object and two 16-byte
guards are compared. This checks unchanged tails as well as initialized
fields, the 79-byte filename cap and its terminating NUL.

The original constructor runs with the object at offset `6910`, input at
`6800`, and CS=DS=SS. The host model receives that actual segment and object
offset for its logical buffer pointer. Only object word `+18`, the method's
relocated code segment, is normalized: original execution must contain the
actual CS, while the Pascal result must contain its logical `24DD`. No
other byte is masked. Original SP must be restored by `RETF 8`; preserved
DS/SS and output object identity are checked for every case.

The first actual run matched all 778 cases. A compiled candidate with a
deliberately shortened filename cap is rejected by the same comparison.
Tests also reject pointer, string, unchanged-memory, ABI, stage-order,
partial-output and saved-provenance mutations.

`engine/recovery.py` discovers conventional build-directory reports and
revalidates their contract, corpus, source hashes and artifact bytes.
`scoped_differential_routines_passed` is separate from recovered source,
host behavior and whole-routine original-binary verification. Results bind
the executable, actual Pascal body/runtime, harnesses, comparator, reviewed
region manifest, input/output bytes and build/emulator tools. No source or
learning promotion occurs.

`constraints.json` records the first small whole-program consequence: the
constructor's checked `+04 = 128` capacity reaches the same-object
input-open entry through the already byte-checked caller handoff. This is
a conditional derived fact, carrying the contract and caller assumptions,
not evidence that input-open is fully recovered or that all game paths
reach it. An incompatible grounded capacity produces a graph conflict.
The address-independent transfer is justified by the checked constant
assignment in the constructor prefix and the bounded filename-write tail,
not by extrapolating finite COM-address samples. Observed COM preconditions
remain separate from the caller's transfer assumptions.

**Remaining limits:** fixed nonaliasing layout and finite cases; no normal
game segment capture, arbitrary-alias coverage, TP7 code-generation match,
full register equivalence or complete input-I/O-family Pascal parity. The 295/26/10/0
inventory/source/behavior/whole-routine-original baseline is unchanged.
Next is the connected file-input family, not a new game implementation.

### Input refill leaf: original `24DD:375E`

The input-open Pascal wrapper still calls an unresolved implementation, so the
next recovered candidate is its leaf read handler, before attempting the
caller. This entry exists in the byte-checked input lifecycle regions but not
in the existing 295-entry assembly/function inventory. Its new Pascal include
is therefore an isolated candidate, not an inventory or ledger promotion.

The handler uses the object's DOS handle at `+00`, capacity at `+04`, and far
buffer pointer at `+0C/+0E`. On a successful read it writes the returned byte
count to `+0A`; on failure it clears `+0A` and returns the DOS error. Both paths
reset position `+08` to zero. A short read overwrites only the returned prefix,
leaving the rest of the buffer intact. The original does not itself write the
global dispatcher error word: probe instrumentation stores returned AX there
solely to capture it.

`tools/liero_read_handler_probe.py` reuses the existing COM harness with an
assembly-time refill-only branch. Constructor/open/setup still run original
bytes. The host Pascal runner starts from the original post-open snapshot and
executes the actual `src/FUN_24dd_375e.inc`, with a resolved buffer pointer and
an explicit read-service adapter. No original pointer or handle is masked.

**Measured:** 96 calls across 12 fixed fixtures pass full 512-byte
object/destination and return-value comparison. Cases include binary bytes
`00`, `0D`, `0A`, `FF`, repeated EOF, lengths around the 128-byte boundary,
capacities 0/1/7/128, and invalid handle `FFFF` returning DOS error 6.
Position and available-count fields start dirty before every call.
A compiled Pascal mutant hardcoding a 127-byte read capacity is rejected.
Saved comparisons are replayed and stale source/artifact bindings rejected.
The earlier constructor and original file-loop tests still pass.

**Limits and next dependency:** the host adapter is not full DOS emulation,
and does not prove arbitrary errors, aliased memory, original TP7 ABI or normal
game segment layout. Open/setup remain original-only; read/skip/reopen/close
wrappers are not yet a differentially verified Pascal family. Recovery counts
remain 295/26/10/0, and the standalone leaf is not added to scoped audit counts.
The close-handler leaf is checked below. Dispatch/open wrapper contracts
remain next; do not jump to callers whose callees remain unresolved.

### Input close leaf: original `24DD:37D3`

The checked original leaf reads the handle from object `+00`, returns zero
without a DOS call for unsigned handles at most 4, and otherwise invokes DOS
AH=`3Eh`. A failed DOS close returns its AX error; success returns zero.
The leaf itself does not clear the object handle, mode, buffer position or
method slots, and does not store the global dispatcher error word. Those
effects belong to callers, not the close leaf.

The actual `src/FUN_24dd_37d3.inc` now implements that conditional behavior
using an explicit host DOS-close adapter. The existing file-handler runner
and COM harness were extended, not replaced with a second probing framework.
The host adapter closes a real file once and tracks its closed state; reserved
handles are never passed to it by the correct candidate.

**Measured:** all eight original-versus-Pascal calls pass: handles 0/1/2/3/4,
the original live input handle, that handle again, and `FFFF`. Results are
0/0/0/0/0/0/6/6. All 512 object/destination bytes are compared without pointer
or handle masking; the harness seeds dirty position/count fields and nonzero
buffer/destination patterns so spurious clears cannot hide in zeroed memory.
Original DS/SS and `RETF 4` stack cleanup are checked. Host-only callback
counts additionally reject invoking the adapter for reserved handles.
A compiled `handle <= 3` guard mutant fails at handle 4.

**Limits:** original constructor/open/setup remain fixtures rather than Pascal
caller parity. The host adapter is not full DOS emulation, and callback counts
are not original interrupt observations. The candidate is absent from the
existing inventory, so no recovery, scoped-audit or training count is raised.
Shared-runner edits require fresh read-leaf evidence; old hashes are not
silently reused. Next is dispatch `24DD:374D`, with checked read/close leaf
contracts and explicit unknown setup/other-method outcomes.

### Dispatcher composition: original `24DD:374D`

The indexed near dispatcher now has a meaningful Pascal body, retaining its
existing parameterless entry. It uses the runtime register mirrors and an
explicit host method resolver rather than pretending that original far
addresses are native host function pointers. The dispatcher saves `ES:DI`,
calls the selected method with the saved object identity, sets the zero flag
from returned AX, records nonzero AX in `GlobalWord6410`, and restores `ES:DI`.
Zero AX leaves any previous error untouched. No resolver is an explicit
runtime error, not a successful no-op.

**Measured:** 24 original-versus-Pascal dispatches pass over empty, binary short
and full-buffer inputs. The first five dispatches compose actual read/close
leaves on both sides: read, close, repeated close, reserved handle close, and
invalid handle read. This exercises successful calls with initial error
`55AA`, error 6, and a subsequent successful call that must preserve error 6.
The host resolver checks captured method segments/offsets and object identity.

For the last three dispatches, probe-only slot `18h` points to a labeled
synthetic far callback. It increments object `+06`, clobbers `ES:DI` and returns
`1234`, zero, then `FFFF`. This verifies single invocation, argument handoff,
pointer restoration and sticky errors under an adversarial callback; it does
not recover the null slot as a real game method. Full 512-byte snapshots and
captured AX/ES/DI/ZF are checked, as is original stack balance. Other registers,
flags and normal-game segment layouts are not certified.

Compiled mutants that clear errors on success or break either restored
pointer word fail. Missing resolver and unknown method pointers fail
explicitly. Existing leaf/constructor/file-loop and reporting tests continue
to pass. The first attempted synthetic location `0A00` overlapped the copied
original helper due to harness padding; the image builder rejected it before
execution. The final callback is at `0400`, below the original helper `04F4`.
Do not relax overlap checks when extending the probe.

This dispatcher is in the existing inventory, unlike the read/close leaf
entries. No ledger attestation or source/training promotion was made and the
standalone dispatch result is not yet counted by automatic scoped audits.
The input subset of setup is checked below. Common open/reopen wrapper
composition remains next; output-mode and unknown method effects remain unresolved.

### Input-mode setup: original `24DD:420C`

The setup routine includes unresolved output-mode branches and a helper that
can seek/truncate files. This batch deliberately recovers only mode `D7B1`,
whose branch opens read-only input or bypasses open for an empty filename.
The actual `src/FUN_24dd_420c.inc` aborts unsupported modes rather than
pretending the complete routine is recovered. It is not in the existing
295-entry inventory and no ledger entry is promoted.

**Measured:** 32 original-versus-Pascal calls pass across existing-file,
empty-name, missing-file and missing-directory fixtures. Each call begins
with dirty handle `BEEF`, position/count `55AA/FFFF`, and `A5` method slots.
The full 512-byte object/destination state and AX are checked. Success installs
read `24DD:375E`, null slot `18h`, and close `24DD:37D3` without changing the
mode or buffer position/count. Failure leaves handle zero and retains dirty
method slots. Original DS/SS preservation and `RETF 4` balance are checked.

Two first-run hypotheses failed and were corrected against original traces:

- Empty names do **not** store the prepared AX value `3D00`: the conditional
  branch skips both DOS open and its handle store, retaining the zero written
  at entry. Method slots are still installed.
- This DOSBox backend returns error **2**, not the hypothesized 3, for
  `NO_DIR/INPUT.TXT`. The host adapter maps the actual missing path to that
  observed backend outcome; it is not a general DOS error specification.

Original open is used only to capture fixture identity; the fixture handle
is closed before setup calls. The host adapter actually opens input read-only
and reuses the captured logical DOS handle, so allocator equivalence is not
claimed. Probe cleanup closes successful opens after capture. Empty names
invoke no host adapter; a probe counter records nonempty open attempts.
Unexpected host I/O errors abort.

Compiled mutants clearing position or converting an open error into success
are rejected, and an output-mode fixture triggers the candidate's explicit
unsupported-mode runtime error 211. No full TP7 ABI, output/setup-helper,
normal-startup or training promotion follows. Next is composing the input-only
common open/reopen wrapper with the checked dispatcher, close and setup
bodies, preserving sticky errors and all unsupported-path gates. That bounded
composition is checked below.

### Input open/reopen/close wrapper composition

The actual input entry `FUN_24dd_36b7`, common open `FUN_24dd_36c4` and close
wrapper `FUN_24dd_3711` now compose the checked dispatcher, input setup and
close leaf bodies. The old draft incorrectly passed the mode as the common
open's sole argument; the original receives a far object argument and the
requested mode in DX. Host signatures now explicitly receive the resolved
object `Pointer`, while `RegisterDX` supplies the logical requested mode and
`RegisterES:DI` mirror the object's original address. All affected forwards
and the output-entry binding were updated together. The output entry now
forwards the object with requested mode `D7B2`; output transitions remain
unsupported and abort explicitly before wrapper side effects.

**Measured:** 24 transitions pass full 512-byte state and global-error
comparison over empty, binary short and full-file fixtures:

| Operation | Global error afterward | Mode afterward |
| --- | --- | --- |
| Reopen live input, starting with error `55AA` | `55AA` | Input |
| Reopen after forced invalid-handle close | `6` | Input |
| Reopen with missing filename | `2` | Closed |
| Open existing file from closed | `2` | Input |
| Close with forced invalid handle | `6` | Closed |
| Close already-closed object | `67` | Closed |
| Open object with invalid mode `1234` | `66` | `1234` |
| Open empty filename from closed | `66` | Input, handle zero |

These are connected transitions, not independent summary mocks. Actual Pascal
setup/close leaves run through the actual dispatcher and a bounded resolver.
Host adapters use real files and reject unknown methods or unexpected I/O
errors. The fixture harness deliberately closes live resources before forcing
invalid handles, and dirties buffer position/count before every operation.
Input open resets those fields; invalid operations and close do not.
Successful setup retains previous global errors, so common open must use the
current return zero flag rather than test the global error word.

Original execution confirms that reopen does not stop after a close error,
and input close always marks the object closed after the dispatched close
returns, even on failure. Compiled candidates breaking either rule or
confusing sticky status with current setup success are rejected. Current and
requested output-mode gates are separately executed and return runtime error
211 on the host. Matching forward declarations and actual include bodies
compile together.

**Limits:** original constructor/open still establishes initial fixture
identity; host logical-handle reuse is not DOS allocation equivalence. Wrapper
register returns, arbitrary far-pointer layouts, output flush/setup, normal
startup and universal equivalence remain unproved. No source/ledger/training
promotion or automatic scoped-count change was made. Next is the connected
string-read/line-skip slice, including the retained four-byte object argument
and CR/LF across the 128-byte refill boundary.

### String-read/line-skip callback leaves

Before composing the still-unrecovered buffer dispatcher `37EC`, the actual
Pascal callback leaves `39AB` and `390E` now have a bounded original-byte
differential probe in the existing runner (`--handler callbacks`). They are
not separate inventory entries and are not yet wired into the unrecovered
wrapper drafts. The probe compiles both actual include bodies.

**Measured scope:** 14 fixed single-buffer fixtures, eight alternating
read/skip calls each (112 total). Checks include full 512-byte states, AX,
relative SI/DI, remaining CX, original near-RET balance and DS/SS.
Input comes from original open/refill. Counts are `0/1/7/255`; fixtures
include CR/LF/1A/NUL/FF, 128-byte boundaries, repeated CR and a terminator
exactly at the count limit. Three compiled incorrect candidates are rejected.

Original execution corrected two initial hypotheses: exhausted count does
not rewind SI, and skip's 1A branch does rewind SI and returns zero, not
`3923`. In contrast, CR at the buffer's last byte returns continuation
`3923`; skip consumes a following LF but leaves any other next byte.
Count zero wraps rather than meaning "copy nothing." Reader delimiters stay
unconsumed, while ordinary LF and NUL are copied.

**Unresolved:** callback composition through `37EC`, `3923`'s second phase,
actual reader/skip wrappers, retained object-argument handoff and cross-refill
CR/LF Pascal parity. The prior original-only cross-refill observation remains
valid but is not evidence that these host leaves compose correctly. No
whole-routine, ledger, source-recovery or training promotion follows.
Next is the connected dispatcher and remaining continuation dependency,
before replacing the reader/skip drafts.

### Input buffer dispatcher and cross-refill continuation

The next dependency group now composes actual Pascal `37EC`, refill bridge
`396C`, read leaf `375E`, callbacks `39AB/390E` and second-phase `3923`.
The original skip-region byte binding already includes the continuation
entry: it consumes one LF, otherwise leaves the next byte unconsumed.

**Measured:** 88 original/Pascal calls over11 fixed fixtures in shared-runner
`--handler buffer` mode. Read/skip operations keep one live input resource,
so buffer positions, tails and file cursor carry between calls. Cases cover
CR at byte127 with LF/non-LF/EOF after refill, multiple refills during skip,
read continuation across refill, short/empty input, repeated EOF,1A and
embedded NUL/LF/FF. Final operations exercise sticky-error bypass and invalid
mode68; a separate fixture forces invalid read handle6.

All512 object/destination bytes, global error, callback AX, relative SI/DI,
CX and ZF agree with original execution and an independent chunk/prefix
checker. Object bytes32..41 are labeled harness-only register capture.
Original DS/SS and near-return balance are checked. Three compiled mutants
and five unsupported host bindings are rejected; tampered comparisons and
partial output cannot replay as success.

The dispatcher must preserve the *current* continuation token through the
actual refill bridge. CR at the last byte changes390E to3923 before refill;
substituting390E would skip the following line. Both EOF and read failure
can return a nonzero callback AX while final ZF is true. Host method resolution
requires375E plus the captured segment and explicit bound buffers; it is not
a general far-call emulator.

The main Pascal include surface now includes these dependencies before37EC;
existing parameterless forwards remain valid. Complete target compilation
passes (unrecovered draft results and unbound runtime adapters still warn).
The adapter is intentionally not wired into guessed normal-startup behavior.
No source/ledger/training promotion or recovery-count increase follows.

### Reader and line-skip wrappers

The wrapper mode now executes the original `3988` reader followed by
`38F0` skip, twice, against the actual dispatcher/refill dependency group.
Two fixtures run four wrapper calls each (eight total), including a CR/LF
split at the 128-byte boundary. All512 object/destination bytes and global
status are compared after each call.

The captured stack is `FDF8` at baseline, `FDF4` immediately after each
reader `RETF 6`, and back to `FDF8` after skip `RETF 4`. The Pascal probe
models the retained object far argument as an explicit logical record and
verifies its offset, segment and lifetime; it does not claim that FPC
reproduces TP7's physical stack ABI.

The optional `+18` method path is exercised through a synthetic far method
returning zero or `1234`. The candidate resolver accepts only the captured
`0400:CS` method and the exact object address; a changed method slot is
rejected. `1234` becomes sticky global status on skip, and later wrappers
preserve it. In this fixed fixture, remaining buffered bytes are used as the
bounded equivalent of the original ZF-clear optional-method path; general
flag equivalence is not claimed. The synthetic method and host resolver are
test seams, not recovered Liero methods.

Replay binds the harness, candidate sources, trace, full state output and
comparison. A compiled reader mutant, malformed output, tampered report and
unsupported method pointer are rejected. This evidence verifies only the
fixed input-mode wrapper sequence and bound host adapters. It does not prove
arbitrary far pointers, general TP7 ABI, all reader/skip contexts, normal
startup, whole-routine equivalence or justify ledger/training promotion.

**Next:** use the measured wrapper path as a constraint for the adjacent
input caller, retaining the existing evidence gates and avoiding any jump to
normal startup or whole-program recovery.

## Remaining work

The function inventory contains 295 Liero routines. Only a small subset has
meaningful Pascal bodies; generated skeletons are not implementations. The
entry point is not a reconstructed game loop, and there is no playable build
or whole-program original-versus-reconstructed-Pascal parity oracle yet.
Progress counts are generated by `tools/report.py` and recorded in
`reports/progress.json`.
