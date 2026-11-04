# Liero source reconstruction status

## Current session checkpoint and next work

### Latest: open-output cleanup and the complete text-error continuation

The installed3711 now supportsD7b1 input andD7b2 output. Output calls slot20
through374d, then slot28 even after a flush failure, and finally writesD7b0
even after a close error. Original savesAL1 across the flush: using the flush
status to stop would be a redesign.374d restoresES:DI, setsZF fromAX and stores
only nonzeroAX into6410.37d3 skips DOS close for handles0..4 and otherwise
returns the actual close result. Original bytes and absence of MZ fixups for
these regions are authenticated, not inferred from assembly listings.

010f now preflights closed objects or checked default open input78f0/output79f0.
Open close must be37d3 at the explicit runtime code segment; output additionally
requires37b3, capacity128,used<=128 and its internal buffer atobject+128 in the
bound data segment. Missing resolver, bad identities/bounds/stack or nonempty
descriptor/callback chains reject. ES:DI is explicitly rebound before each3711.
The installed resolver is a declared host port, not arbitrary TP7 dispatch.

The existing cleanup/error probe now has `--terminating --open-output` and
`--terminating --open-output --text-error`; both support immutable `--replay`.

| Panel | Original/installed matches | Evidence |
| --- | --- | --- |
| Open010f/nonzero04f4 |40/40 | Both entries, used0/1/7/128; actual file success/invalid-handle6, separately injected write5/close6 |
| Complete0037 error continuation |3/3 | One actual invalid-handle6; injected write5/close0 and write5/close6 |

Open endpoints are1037 bytes: prior885-byte globals/objects/vectors/diagnostics
plus152 bytes of write/close observations and attempted output. Actual file
bytes and independent host process termination status are checked. Successful
cleanup preserves203, flush5 then successful close preserves5, and close6
replaces the sticky error. Input handle0 closes without a DOS service.

The text panel runs unchanged original0037 in a separate segment and patches
only its two actual MZ far-call segment operands. It rendersA/B with original
attributes, attemptsCRLF count2, then reaches nonzero04f4 and010f. Cleanup
attempts a second write with count0 and then closes. The actual original far
return is **0155:textCS**, and diagnostics report`0300:0155`; the earlier0157
handoff was an unmeasured, wrong assumption. Failed debug1 is retained.
The installed source writes that logical pair before04f4 under explicit text/
runtime/data bindings; its native host stack is not TP7 ABI.

Full5299-byte endpoints additionally compare4262 bytes of first-write count/
mode/used,4000video and256input. That snapshot is **before diagnostics**, not
the final diagnostic console screen. Real vector restores/diagnostic/termination
are still observed; INT21 deliberately saves/restores the owned observing hook.
Compiled source mutants reject wrong0157 and skipping close after flush error;
eight invalid open bindings reject211. Trace mutations check state and service
fields. No normal-game error reachability is inferred.

Final sealed archives: `files/open-error-final-20261104`,
`text-error-integration-final-20261104`. Both replay; six earlier returning
text panels, scrolling, closed termination and original startup-return archives
also replay without altering historical methods or scope.
1192 connected tests pass,3 existing xfail; Ruff passes; cleanup runner Pylance
diagnostics are empty after explicit tuple-length guards. Full range-checked
Pascal target builds with40 warnings. Frozen liveQwen3 regression uses one
request,56/56training+56/56terminal and identical replay:
`files/open-cleanup-model-regression-20261104`. This repeats known assisted
arithmetic; no weight improvement, text-model recovery or source/example
promotion. Whole-review28/295 and cleanpanel2/3 remain.

Current source SHA256:
- 3711:`2db135f4e87eaad6856afd615adec0bd2e7d7ade39c850b7d0212b9c462a21ac`
- 010f:`86ebd7c2f615fdb2d2d6633be7cfc9284acecb9b8a5c9ff9fe73de7cbb5a982a`
- 0037:`7f73d17c527477221b5ebb23eccb6f667de606c0477040442b39e3a95ea81d94`
- Runtime:`8a9e3b68def792ae8c7be9971c3a6da8e585d03047fff076e4bc1fd63da2bfb6`

The private scoped review binds remaining source/method hashes, measured
results and preserved failures. Actual descriptor/callback provenance and
writable bounds, sound-device polling/progress, redirected378e, recovered
Pascal startup, native ABI and normal-game reachability remain unresolved.
Relative135c:1345 (not24dd:1345) depends on045d/032e and ultimately polling
leaves0000/001a without software timeouts. Ready-port fixtures do not establish
real termination. Do not widen these40/3 cases into full010f/0037 acceptance.
The preexisting runtime Halt97 and seven older startup-tool diagnostics are
not fixed or counted as passed.

### Previous: scrolling, terminating errors and full original startup return

The requested limits work produced three distinct evidence classes:

1. **Installed scrolling service projection:**88/88 full0037 original/Pascal
   console cases use rows23/24, eleven shortstrings and capacities1/2/7/128.
   Row24 CRLF scrolls3840 bytes upward; all80 bottom cells become space/07.
   Cursor stays row24,col0. Complete4000video+256object+256input bytes, status
   and attempted service byte/count logs agree. This is mode3/page0 CR/LF,
   not a generic terminal implementation.
2. **Installed terminating010f scope:**28/28 direct/nonzero04f4 cases use
   errorwords1,5,106,203,255,1234hex,ff00hex and zero/nonzero caller pairs.
   Original POPCX/POPBX consumes the far return; actualMZ DS fixup011b,
   normalization byPSP+10hex,19 vector restorations and actualAH4c exit are
   preserved. Empty descriptor/callback chains and closedD7b0 input/output
   objects are required. Closed3711 sets sticky67. Full58globals,588object/
   vector bytes, restored IDs/targets, diagnostic bytes and declared frame/
   segment/exit request match; host exitcode lowbyte independently checked.
   OriginalINT21 saved/restored target is the disclosed observing hook.
   Real010f normally terminates, never returns. Unknown chains, open objects,
   missing ports and aliasing reject before unsupported source execution.
3. **Original-only full startup return:**unmodified original entry farCALL,
   startup0000..00b0 and RETF execute through actual constructors/opening.
   Only the next main instruction becomes a disclosed farJMP collector,
   reusing its existing MZ segment relocation exactly once. Original saved
   vectors are restored after recording.8192 DS bytes captured; loader/
   PSP/return stack and exact default objects are checked, not whole-window
   Pascal parity. ObservedDS1b12/code167e are this run's relocation, not
   historical constants. Output handle1,object79f0,buffer7a70/capacity128,
   both37b3 slots and37d3 close bind to actual startup segments. Input handle0
   has375e flush, null optional and37d3 close. No normal game main executes.

Source010f SHA256:
`bfb9390f06c331e98192ba7427af4ace33cf90eddb5ec3fe76bae428e4358179`;
04f4:
`d0503043f3e59711d096f6ccdf0dcdf0030c89c138ff1fc33388180cc774e831`.
01f0 is now CS-string output;0218's omitted fall-through now prints both
bytes/four digits;01fe restores its final duplicated remainder after output.
Source hashes and limitations are bound in the private scoped review.

Reproduce with text probe `--entry text --service scroll`, existing cleanup
dispatch probe `--terminating`, or startup clear probe `--full-return`;
each supports `--replay --output <existing>`. Final archives:
`files/text-scroll-final-20261104`, `text-error-exit-final-20261104`,
`text-startup-return-final-20261104`. Historical text source sets remain
separately accepted for their old scope; methods/trace bytes are not rewritten.
Historical cleanup replay checks saved method snapshots and current semantic
premises, not equality to today's larger tool's hash.

1190 connected tests pass,3 existing xfail; Ruff passes; target builds with40
warnings. Pylance's new possibly-unbound scroll-body diagnostic was corrected
by keeping the scroll panel inside the text branch. Existing startup-tool
diagnostics outside the added path are not relabeled clean. LiveQwen3 known
arithmetic regression uses one request and passes56training+56terminal; replay
does not infer or evaluate again. No weight/example/whole-source promotions;
whole-review28/295 and cleanpanel2/3 remain.
Final post-type-narrowing regression and replay are preserved at
`files/text-limits-model-final-20261104`;666 focused tests pass after that
nonsemantic generator correction. Earlier live result remains separate.

**Unresolved:**0037's output object is openD7b2, outside this010f closed-object
contract. Need proven374d output resolution plus3711 flush/37d3 close and
correct original caller-return binding before claiming integrated nonzero text
parity. Actual descriptor/callback chains and normal error reachability are
not established by the older mechanism probes. Original startup-return
observation does not recover the Pascal0000 stub or justify later lifetimes.
Redirected378e, arbitrary BIOS/DOS/device behavior and native ABI stay open.

Failed assumptions remain preserved: error debug1 failed TP-mode procedural
assignment syntax; debug2 timed out because the short COM image failed to pad
the original3711 offset; debug3 passed after padding. Startup debug1 duplicated
an already-existing MZ relocation and missed the collector; debug2 reached it
but incorrectly read PSP end through changedES; debug3 bound the saved loader
PSP correctly and passed. Final experiments freeze the repaired methods; none
of these mechanism repairs is unseen-model recovery or terminal feedback.

### Previous milestone: complete supported text routine

Installed3899,3930,zero-only04f4 and full249c0037 body in the existing target.
0037 include moves after its shared output bindings; interfaces are unchanged.
Original asm residue stays. Source SHA256:

- 0037: `57c669a375ef6b5eb0ae48d98048371c809c76322cb7e0b5254553af948ba708`
- 3899: `1239cfe0eea1501e15b672a66bffebab6b8fd6e233e968c2cb571699cd367e0d`
- 3930: `c2ab6ba597dbdccb83d4c2b0af4aa7e7ad296869078ef8d9d9f8a16592eae0c7`
- 04f4: `22d9fc5b72b4e9e07f5c5f06a0933e01afe906f7c9e35013d0e7f2f14b3d5efe`

Complete original0037..0158 bytes, original cursor/arithmetic, output chain,
zero/error-check bytes and actual MZ relocations014e/0153 authenticated.
Fixture runtime at original24dd offsets; text segmentCS+100 contains original
249c:0000..0158. Only the two actual far-call segment words are relocated.
DS=SS fixture provenance, writable object79f0/internalbuffer7a70, source8200,
globals6410/CRLF6424 and stackdb00..dff3 are owned/disjoint from code/video.
These are explicit relocated fixture bindings, not observed normal startup.

The installed full body copies the shortstring to logicalSS frame, uses0013
for default/changed attributes, renders B800 glyphs, processes zero/low/high
escape states, makes both0000 cursor calls, calls3930 and zero-only04f4,
restores BP and returns logical SPentry+12. Final BIOS column uses raw length
including control bytes, not glyph count. Incomplete escape suffixes do not
print. Valid mode3 rows/columns and nonaliasing bounds are checked.

3899 copies through explicit segmented source/buffer bindings in chunks.
Full buffer flushes even with zero initialcount. It saves remainingAX across
dispatch and continues after errors; checked37b3 resets used, guaranteeing
progress.3930 supplies authenticatedDS6424 CRLF; optional slot invocation
depends on returned ZF and slot26, not stickyerror. Zero-count optional calls
and optional calls after a failed full-buffer flush are original behavior.
04f4 zero returns; nonzero explicitly rejects because010f remains unresolved.

Original/installed/specification checks pass:
75file+78injected3899,27file+28injected3930,
44fulltext/file+44fulltext/realconsole. All4000video,256object/buffer,
256input bytes plus sticky/cursor and every attempted service byte/count
agree. Original DS/SS/BP/SP/ZF/guards checked separately; no full native
stack-scratch/register/ABI parity. File byte totals5646/581/189 respectively.
Console's captured attempted bytes are CRLF percase,88total; the OUTPUT.BIN
file is empty because output goes to actual handle1, not that file.

Real console closes an important gap: DOS CRLF moves cursor to nextrow,col0
after the caller's final BIOS call. File output leaves cursor atrow,col+length.
The console panel startsused0; host adapter supports onlyCR/LF with no scroll.
Original BIOS/BDAmode3 and complete resulting video/cursor are observed, not
inferred from file output. Other console bytes, scrolling/invalid coordinates,
arbitrary device/register effects and normal program reachability are unknown.

Run `tools.liero_text_probe --entry text --service console` or writer/crlf
file/injected panels. Six sealed archives under
`files/text-{writer,writer-injected,crlf,crlf-injected,full-file,full-console}-final-20261104`
replay immutable bytes without DOS/compiler/model execution. Earlier initial
archives have narrower methods and remain historical. Source mutants catch
wrong escape state/cursor/CRLF and early flush-error exit; unsupported aliases,
wraps, missing bindings, modes/capacity and010f reject. No held-out/model
recovery trial or source-ledger promotion occurred in these known-body panels.

567 connected tests pass,3 existing xfail; full target builds,40warnings.
Baseline runtime97 remains unrelated/unresolved, not rerun as a pass.
LiveQwen3 arithmetic regression one request56/56training+56/56terminal and
replay, `files/text-full-model-regression-20261104`; same known assisted
method/corpus, no text-model generation, weight gain or independent support.
Whole-review28/295/cleanpanel2/3 unchanged.

The supported complete returning text path is delivered. All-path/native
text acceptance still needs010f/nonzero04f4 cleanup/error behavior,
redirected378e, generic BIOS/DOS/scroll and normal startup provenance.
Do not conflate complete supported execution with universal recovery.

### Installed396c/397a output dispatch to37b3

Installed exact37b3 output branches in the existing396c/397a procedures,
sharing an explicit method/object/source resolver in396c. Prior input375e
and isolated0400 synthetic optional scopes are unchanged and regression-tested.
Source SHA256:

- 396c: `d3d3bfeed8ac1d4c7092a22b327e5333639198fa4605cd98924372cf490f0861`
- 397a: `79a60edcc9da79288d0ccd993577ec5c398da1726facd2c382e3affc3c9a6ddd`

Original14-byte entries atfile106156/106170 have no actual MZ fixups:
PUSH ES/BX; far CALL through ES:[BX+14hex/18hex]; OR AX; zero skips
MOV DS6410,AX; near RET. They do not restore BX. With37b3 and the scoped
DOS preservation premise, BX=handle, DI=object offset, ES=object segment.
Success leaves prior sticky error unchanged; failure replaces it; ZF=(AX=0).
Other external register/flag effects remain unknown, not silently preserved
as a claimed full native contract.

Extended the existing write probe, not a second framework. Each original
dispatcher invokes unchanged37b3 bytes:8 real DOS file writes,8 NUL,
8 invalidFFFF handle errors and32 separately injected CF/AX mechanisms.
Full4096arena/status/service inputs/reset order and360 file bytes per path
agree with installed Pascal. Original stickyDS6410, ZF, BX/DI, segment
restoration, near returnSP and guards checked. Source segment alternates
CS/CS+100 with equivalent physical source; object/code segment distinction
is explicit in the interface but not an independently varied fixture dimension.
Owned writable DS6410 is outside the object/source/code/active-stack regions.

The host method words use logical37b3, while the copied original code runs at
a fixture offset. The driver validates both slot words after invocation, then
encodes that explicit resolver binding in snapshots. This is not host/native
pointer equality. Null/unknown methods, bad count and mismatched bindings abort.
Trace/host mutants and a compiled sticky-error source mutant are rejected.

Private sealed archives `files/output-dispatch-flush-20261104` and
`files/output-dispatch-optional-20261104` replay without execution; historical
write-leaf-v2 also replays.558 connected tests pass,3 existing xfail, including
input buffer and optional-input compatibility. Full Pascal target builds;
the prior unrelated runtime97 remains unresolved, not reclassified as a pass.
LiveQwen3 regression: one request,56/56training+56/56terminal and replay,
`files/output-dispatch-model-regression-20261104`; same known assisted method
and corpus, no weight gain, model-generated dispatch or source promotion.

Next3899 buffered-copy/flush/progress/error composition, then3930 CRLF.
Published callee constraints narrow those callers but do not resolve them.
Redirected378e,010f/nonzero04f4, native ABI and full0037 reachability remain
unresolved;28/295 and clean panel2/3 are unchanged.

### Installed37b3 device-output service projection

Installed `src/FUN_24dd_37b3.inc` in the existing target. SHA256:
`b9e064bdd6621cdb1a2909c8a5258b04002d3ab278607c355cab461ea5a7db67`.
Human recovery from original32bytes atfile105715, with no actual MZ fixups.
The host interface takes explicit resolved object/buffer pointers and a
DOS-write callback; this changes representation, not the original memory/status
policy. It is not a recovered native TP7 argument/ABI declaration.

Original LDS gets buffer+12, XCHG clears used+8 before AH40, including count0.
CFclear returnsAX0 even if AX reports a successful short write; CFset returns
the error with used still0. Installed source resets before its single callback
and ignores bytesWritten.378e's short-write101 behavior is not substituted.
Owned/nonaliasing object, count-readable buffer and active stack/code are
explicit premises; unrelated DOS register/flag/device effects remain external.

`tools.liero_write_handler_probe` compares original execution and the actual
installed include:8 real DOS file writes,8 NUL cases,8 invalidFFFF handle
errors6, plus32 separately labeled injected CF/AX mechanism cases.
Counts0,1,2,7,31,64,127,128; service sourceDS alternates CS/CS+100 at offsets
8100/7100, equivalent physical source disjoint from object and stack.
Full4096arena, one service call/reset ordering/inputs, AX and360 file bytes
agree. Original restoredDS,ES,SS,BP,returnSP and guards checked independently;
host file/NUL/error adapters do not prove native ABI or all DOS effects.

Private `files/text-write-leaf-v2-20261104` is sealed with source/method/image
snapshots; replay checks immutable archived comparisons without execution.
Earlier same-segment archive is retained, not relabeled as different-segment
evidence. Initial mutation-test expectation was corrected: changing fixture
handle/object-segment identity explicitly rejects binding, not merely a row.
551 connected tests pass,3 existing xfail; full target compiles. Baseline
runtime97 remains a prior unrelated failure, not a new successful program run.
LiveQwen3 same-method arithmetic regression: one request,56/56training+
56/56terminal and replay; archive `files/text-write-model-regression-20261104`.
No model-generated37b3, changed weights, new independent corpus or promotion.

Next396c/397a output dispatch, then3899/3930. Current396c remains input375e
only. Redirected378e, nonzero04f4/010f and full0037/native reachability remain
unresolved.37b3 is an alternate entry, not extra census credit;28/295 unchanged.

### Cursor service projection and remaining text-output dependencies

Installed0000 source with(columnWord,rowWord:Word) and matching forward;
original19bytes plus0037:0077..0083 prove column-first/row-last pushes and
low-byte page0 BIOS AH02 cursor binding. Logical BIOSCursorColumn/Row andSP
are modeled, not actual BIOS/BDA storage or external register/flag effects.
Source SHA256b8cb5b64f182a2f07676c8b3c3033364af25ea7959bb8509f4630ba390bdb547.

Original DOSBox cursor query/BDA position16/16, video BDA mode3/80columns
checked percase; returnSP/BP/guards/unchanged arena separately checked.
Installed logical projection16/16 and65536hostword/high-byte/SP-wrap cases
pass; archive freezes source/runtime/harness/corpus/traces and replay checks.
This is bounded original-service observation plus host cursor projection,
not full ABI/device parity or whole0000/0037 source acceptance.
Privatearchive files/text-cursor-projection-20261104; earlier original-only
observation retained.499connected tests pass,3xfail. Full target and runtime
compile; unrelated baseline3f86 Halt97 persists before new assertions.
Mandatory liveQwen3 arithmetic regression: one request56/56+56/56, prior
known-source structured method/corpora; no newweights/blind-source credit.

Byte-authenticated04f4/3899/3930 dependency contracts now document exact
conditional returns, sourceDS6424, outputmodeD7B2, segment switch/restore,
optional397a callback and nonzero tailJMP010f. No whole routine promotion;
missing error/dispatch scopes remain explicit, original source stubs retained.
396c currently supports onlyinput375e; outputflush would wrongly invokeinput.
Subsequent original-byte/relocation trace proves conditional default-output
linkage: relocatedstartup1971 => logicalDS2971;3639 receivesDS79f0 and empty
CS0263, setsbufferDS7a70/capacity128/openmethodCS420c;36bcrequestsoutputD7B2.
420c emptyname skipsopen/create, useshandle1 andDOS4400 deviceinfoDLbit80.
Device: slots20and24 bothCS37b3; nondevice: slot20CS378e, slot24zero. Eleven
original supportingstreams/relocations checked in tests and3899 contract.
Second0000 CALL0143 column+length/row pushes also authenticated, as areactual
DS79f0 farCALL3930 andnext04f4 using realMZrelocations014e/0153. These static
caller facts are not complete caller execution or invalid BIOS position tests.
DOS segment preservation/deviceinfo outcomes and normal reachability remain
service premises, not measured native-program observations. DS6424 original
bytes0d0a authenticate3930's two-byte CRLF source under provenDS.
Both write entries resetused+8 before DOS40;378e returns101 on shortwrite,
37b3 ignoresreturnedcountsuccess. Next validate37b3 service contract, then
396c/397a dispatch and3899/3930; handle378e's different redirected behavior
separately. Source/global/buffer/stack ownership/nonaliasing and010f remain.
No whole routine promotion; reviewcount28/295 unchanged.
Final post-caller/linkage liveQwen3 one request56/56+56/56, replayed under
files/text-final-model-regression-20261104. Earlier regression archives kept.
Same measured corpus/method is
reproducibility, not additional independent support or changedweights.

### Installed SS arithmetic through actual shortstring initialization

0013 installed source93fdcdfbc3077ba75cf3afad3f865ff5ed2f34d352ef84a691b8bfea5b7cb274
replaces the stub. Original one-word argument atSS:[calleeBP+4], actual caller
PUSH BP: retain existing Integer declaration but interpret its16-bit bits as an
SS offset. No additional hostPointer; ReadStackByte uses provenRegisterSS,
each offset wraps16bit before resolving existing20bitRealModeMemory. Sum of
unsignedcell(-261)<<4 andcell(-260) fits4335, storeslowbyteat(-259),AX=sum,
DX=cell(-260),DI=argument,CFfalse,ZF(sum0),SPentry+4; untouched mirrors/DF
preserved. Active stack/code/data nonaliasing required; native Pascal type/TP7
ABI and full execution unknown. This is human integration of earlier checked
model actions, not a new blind source-generation success. Original asm retained.

Actual249c0037..0060 caller prefix: ENTER10a,0;8cd3/8ec3 setsES=SS,8cdb saves
entryDS inBX; LDS source atBP+6, copies length-prefixed string toSS:[BP-100];
8edb restoresDS, writes7atBP-104 and0atBP-105, PUSH BP andnear005dCALL0013.
Real original frame and installed body compose256/256training+256/256terminal,
all shortstring lengths0..255, full4096arena/register/guards/frame/capture bytes.
Host exhaustive65536byte pairs+6offset/physical-wrap checks pass.
Explicit appendedLEAVE/RETF8 at0060 stops before unknown remainder, not source
implementation of entire0037. Sequential DOS fixture disables interrupts through
capture, reenables before service; capturePUSHF writes0002 at847e. Two earlier
training failures preserved (omittedcapturewrite, then interruptscratch255/256);
no terminal on those methods, no claim about real interrupt-safe behavior.

Installed body included by existing Liero target and runtime tests. Full FPC-Mtp
target compiles; runtime executable's unrelated3f86 Halt97 remains and is
reproduced on exact baseline after removing newinclude/assertion.498connected
tests pass,3xfail. Live Qwen3 after integration: one request56/56training+
56/56terminal in existing hostPointer projection; known-source snapshots and
assistance frozen, no newmodel/weights/whole-source credit.
Contract published inconfig/routine_contracts.json, review/evidence in session
files/integrated-nibble-source-review-20261103.json andcaller-v3/build archives.
Whole-review count28/295 stays unchanged pending applicable whole gates.

Full0037 deferred until0000/3930/04f4 callee contracts resolved. Other0013 calls
0107/011e, text/video/service/global behavior, native type/ABI/reachability remain.
This is an integrated prefix milestone, not whole subsystem/program completion.

### Supported recovery prototype: three earlier scoped passes, clean2/3

The existing runner now supports the same structured interpretation/check/
typed-lowering method for249c:0013 and24dd:455e, plus a bounded `--prototype`
preset and validated scoped export. Both arithmetic routines pass original
training, then first-request model action selection and56/56 host training/
56/56 terminal once. No source body or accepted action tuple supplied to model.
Human original-byte facts, vocabulary, checker, interface and renderer are
disclosed assistance; these are not model-written Pascal or blind recoveries.

249c:0013 exact candidate5acbfe125feebd113eb560323e48966cb95db9c62aa33bbcae46ca33353136e0:
zeroextended SS[arg-261]<<4 plus SS[arg-260], lowbyte atarg-259; nearRET2,
BP/DF preserved, AX/DX/DI/arena checked.455e candidate
04e24ee1660fc0174859b3faf620c746dff71439ffa61d085796d3c64cfb169b:
signed32-bit DX:AX magnitude normalization to exponent/fraction registers;
zero preservesCX, nonzero CH=inputDH, CL preserved; word/byte fast paths
equivalent to32-bit left normalization with160bias. Signed minimum, zero and
boundaries included. Native numeric Pascal real type is not established.
Both exact artifacts have assistant scoped reviews; user/native signoff pending.

Packed caller boundary now authenticated and executed: original1000:92d5..92f2,
initializer40d6 and copier4141, actual MZ relocations92df/92eb.40d6 RETF2
retains SS:(BP-50) source pointer4bytes;92e1 pushes SS:(BP-30) destination plus
packed32.4141 RETF10 consumes all10argument bytes. Host explicitly binds
actual pointer origins rather than incomingSI/DI; original/host full-state
composition12/12 training+12/12 terminal. Pointer versus Longint type identity
not proven just by equivalent far-pointer word layout. Entire929a/prologue/
reachability/arbitrary DS-SS alias/wrap remain obligations.

Clean fixed three-routine preset panel: copier fails both interpretation requests
(7/56,7/56,17/56, repeated destination offsets), no compilation/terminal.
Arithmetic and normalization each succeed56/56+56/56, one request each.
Total four generation requests;2/3 fresh scoped passes, not3/3. Previous copier
pass cannot count as clean success. Repeated seeds are reproducibility, not
new independent evidence. Stop expansion at this bounded prototype milestone.
Initial clean attempt exposed preset inheriting legacy Qwen2.5 default: all six
HTTP calls rejected unsupported thinking before generation; retained separately,
fixed preset defaultQwen3 without changing old CLI default. Near-return metadata
pre-inference455e failure also retained.

Exports `files/prototype-export-{packed,arithmetic,normalization}-20261103`
bind exact candidates, raw proposals, byte/corpus/model/runtime/method hashes,
original/host full records, reviews/unknowns and packed caller evidence. Export
replay validates without generation/terminal reexecution, full original executable/
compiled images excluded. `--prototype` existing complete outputs replay safely;
partial outputs reject rather than resume through held-out outcomes.
Whole source-review ledger remains28/295; source install, gold examples and
weights untouched. Clean3/3 and user review are still open prototype acceptance
gates, not implicit new training or full-Liero acceptance.
Validation494connected tests,3xfail; touched-code Ruff/syntax clean, caller
type diagnostics empty, three scoped exports and explicit clean-copy failure
export replayed. Existing complete-output preset reuse performs no generation
or terminal execution. No new source/training/weight credit from replay/tests.

### Actual packed-copy scoped pass; near SS-arithmetic transfer negative

Explicit frozen Ollama `think:true` and8192token budget on the same Qwen3 model,
supplied byte-binding schema and unchanged action/full-state gates produced
first complete checked packed interpretation on request2.7/56,7/56,4/56 then
56/56,12/56,10/56. Human typed lowering and ABI wrapper pass56/56 full-state
training and56/56 terminal once. Exact source hash
28cc36b11fb4b3bd067e0637f39097bb4415b8f0ec4bfb7b97b76c700916cd43 reviewed as
scoped composition. Actions model-proposed; Pascal/checker/vocabulary/citation
facts/fixture/wrapper human-authored. Not model-written code, blind generalization
or whole native routine. No separate thinking trace returned, so runtime option/
token-budget causal effects are not established.

Actual caller pointer offsets/segments, source param3 type/native Pascal ABI,
normal reachability and arbitrary segment alias/wrap remain unresolved.
No installed body/ledger/gold-label/weight promotion;28/295 remains unchanged.
Scope complete-state recall100%, correctness probability/sensitivity null.
Archive `files/frontier-packed-thinking-v14-20261103/` includes exact source-review.

Next different-behavior leaf249c:0013 original bytes
`5589e58b7e04368a85fcfe30e48bd0368a85fbfe30e4c1e00403c2368885fdfec9c20200`
are near SS-relative byte arithmetic. Argument atBP+4 setsDI; read
SS:[DI-260] thenSS:[DI-261], shift second by4, add, write low byte atDI-259;
LEAVE/nearRET2 restores original frame. Same owned arena snapshot framework
now supports genuine near call,2-byte near return and source logical segment249c.
Host pointer to the three cells is explicitly supplied ABI projection.
Original56/56 training, supplied control pass and shift8 mutant fail.
Live direct-source Qwen3 two requests with think:true emits inline assembly,
correctly rejected before compilation. No terminal/source accepted.
Archive `files/frontier-nibble-transfer-thinking-20261103/`.

Transfer0/1yield stops expansion. This is a scoped hybrid success followed by
negative different-method transfer, NOT an equal-method diverse benchmark.
473connected tests,3xfail; Ruff/Pylance syntax and both archive replays pass.
Broader PoC, cross-project weight gain, second-project MVP and full Liero still
require evidence; their steps are blocked, not marked complete.

### Interpretation-first roadmap execution: memory passes, bindings still blocked

Separate v13 `--supplied-bindings` experiment freezes independently derived
instruction strings in the schema, with no accepted action tuple or Pascal body.
Behavioral alternatives/checks remain unchanged; facts are explicitly human
assistance. Two Qwen3 requests produce7/56,7/56,17/56 memory agreement and repeat
those alternatives, with wrong destination starts. It solves citation format
but does not recover correct memory behavior. No selected/executed candidate
or terminal feedback. This new semantic failure does not invalidate the earlier
v11 scoped56/56 actions, nor does it justify promoting them under old failed
rules. Archive `files/frontier-packed-supplied-bindings-v13-20261103/`.
471connected tests,3xfail. Full roadmap remains incomplete; no further retries.

4141 now uses competing structured hypotheses, original-training memory checks
and typed mechanical lowering in the existing runner. Model interpretation and
human checker/renderer/ABI wrapper are separately attributed. Positive supplied
control demonstrates full-state composition with one interpretation request and
no Pascal request; it is a mechanism test, not live model acceptance.

Live Qwen3:14b (v11) training memory hypotheses:
4/56,7/56,5/56; repair56/56,12/56,56/56. The first56/56 hypothesis agrees with
all six byte-backed action constraints but has incomplete source-start/direction
citations. One v12 immutable evidence-only request repeats the missing bindings.
One installed coder14B escalation:4/56,7/56,7/56 then56/56,10/56,17/56; its
one-shot completion also fails citations. No actions are changed by completion.
Both comparisons2+1 requests, no model-written Pascal; acceptance remains blocked.
The failure is citation completeness, not contradicted memory semantics. Preserve
required4152/4154/4156 source setup and4141/415a transfer bindings; no gate
relaxation or relabeling of earlier failures occurred.

All original-training support is authenticated replay, not independent new
evidence. No candidates execute, no terminal feedback/recovery/examples/weights.
Probability/sensitivity null;56/56 is scoped training-memory recall only.
28/295 reviewed-source count unchanged. At0/1 yield, no diverse frontier batch
or new caller compositions were run. Weight readiness still0 eligible Pascal
pairs across0 projects; second-project MVP and full Liero remain unimplemented.
See [roadmap status](../../../docs/RECOVERY_TODO.md) for explicit prerequisites.

Archives: session `files/frontier-packed-interpretation-v11-20261103/`,
`frontier-packed-binding-v12-20261103/`, `frontier-packed-coder14-v11-20261103/`,
`frontier-packed-coder14-binding-v12-20261103/`.470connected tests,3xfail;
Ruff/Pylance syntax pass, immutable historical replays pass. This is partial
execution, not successful PoC/MVP/full-project delivery.

### Packed-copy residual partition: wrappers no longer block, model logic still does

Existing source runner now supports4141 `--residual`: supplied byte-derived ABI
wrapper, model-only declaration-free MemoryBody(argument,source,destination).
Fixture offset/segment assumptions remain explicit; no native/whole-routine claim.
Same Qwen3:14b,4096tokens/two requests and authenticated original training replay.
First candidate fails FPC on inline `for i: LongInt`; repair repeats identical
source hash94bd1aede203371b659c62f45312ab2843377547820148274856b47ef0f60dd9.
Raw body invents count11 and source skip10, ignoring packed argument. This is
a substantive model reasoning failure as well as invalid Pascal, not a gate that
can be removed. No model candidate executes, no terminal evaluation or promotion.
0/1 yield stops panel expansion;28/295 current reviewed count unchanged.

Correct supplied residual control passes full-state training and wrong-skip
mutant fails.461connected tests,3xfail; Ruff and historical archive replay pass.
Session `files/frontier-packed-copy-residual-v10-20261103/` preserves prompts,
raw outputs, compiler failure, duplicate repair and original training replay.
The first roadmap mechanism is implemented but its recovery exit criterion is
unmet. Transfer/weight efficacy/MVP cannot honestly be declared delivered yet.

### Live measurement after typed-memory guidance (v9)

The new [agents rule](../../../agents.md) requires live model performance
measurement after each coherent improvement, separate from tests/controls.
Opt-in4141 typed guidance supplies PByte indexing, LongInt bounds, packed-byte
extraction and numeric mirror/pointer separation, not a target body. The old
first response exhausted2048tokens; v9 freezes4096tokens, same two requests and
unchanged gates. Legacy defaults unchanged.

| Measured outcome | Baseline | Typed-guidance v9 |
| --- | --- | --- |
| Live requests, same Qwen3:14b digest |2 |2 |
| Complete JSON responses |1/2 |2/2 |
| Generated tokens per request |2048,161 |260,249 |
| Executable model candidates |0 |0 |
| Terminal evaluations |0 |0 |
| Accepted recoveries |0/1 |0/1 |

v9 raw responses contain typed forward copy loops but both wrap them in
`unit/interface/implementation` and omit required state mirrors/flags. They
correctly fail the existing include/service gate before compilation. We did not
strip wrappers or supply missing bodies; static loop presence is not semantic
acceptance. Both v9 stops are normal, not length-limited. No whole-model/weight
improvement or generalization conclusion follows from these two requests.
Input hashes/model digest agree; original56training records are authenticated
replay, not new independent measurement. Terminal untouched, source/ledger/
examples/weights unchanged. Probability/sensitivity/behavioral recall null.
Below25percent yield, stop expansion. Next blocker is complete include-format
synthesis of memory behavior together with required ABI effects.

Session `files/frontier-packed-copy-typed-v9-20261103/` preserves raw proposals,
frozen methods, measured comparison and negative review; baseline archive kept.
459connected tests,3xfail; Ruff and Pylance syntax clean. Signature compatibility
fixed one newly induced kwargs diagnostic without changing request semantics;
unrelated pre-existing Pylance diagnostics remain. Historical replay validates
the frozen trial before that type cleanup.

### Whole295 census: blocked dependencies separated from new model recovery

New [frontier triage](../../../tools/liero_frontier.py) uses original-file
bytes, actual MZ relocations, current source audit/contracts, conservative
i8086 decode and dependency groups. It does not alter source attestations.

| Category | Routines |
| --- | --- |
| Current reviewed-source scopes to reuse |28 |
| Manual bodies requiring review |46 |
| Unresolved callee contracts |130 |
| Control/external effects or unavailable original bytes |82 |
| Implementation-unresolved leaves requiring owned oracles |9 |

These are all295 inventory entries, not proof of exhaustive image code discovery.
FWAIT/FPU obligations and non-file-backed2971 pseudo-entries block rather than
become executable leaves. Unknown/alternate targets remain residue; mutually
recursive routines are grouped. Review reuse is scoped, not universal callee
acceptance. Execution eligibility is false until specific oracle preparation.
Known48e1 is not new discovery credit.

First genuinely unimplemented leaf4141 has exact bytes
`fc8bdc8cda36c5770a36c47f06368b5f048acf32ed03f18acbf3a48edaca0a00`.
High packed byte skips source bytes; low byte copies forward, including overlap
smearing; BX retains packed input, SI advances by skip+count, DI by count,
CF/ZF/PF/SF/OF come from ADD SI,CX. Original415c bytes8eda restore DS
(exported listing reverses MOV direction). Host canonical Word/pointer interface
is explicit human assistance, not recovered original param3 type/native ABI.
Owned DS arena/no-wrap/stack premises are frozen. Original training56/56
complete-state records agree; supplied typed control passes and seven byte/state
mutants fail. Control validation is not model recovery.

Qwen3:14b spent its frozen two-request budget: malformed JSON, then
representation-rejected Pascal. Second response also omits copying entirely,
reads pointer data as segment/offset and omits required CF/ZF. No candidate
compiles or executes; no terminal feedback. 0/1 attempted-routine yield stops
expansion below25percent. No installation, ledger/examples/weights changed;
28/295 current source-reviewed count unchanged. Probability and sensitivity
remain null; candidate recall is null because no model cases were evaluated.

Session archives `files/liero-frontier-v3-20261103/` and
`files/frontier-packed-copy-4141-20261103/` preserve frozen method/input hashes,
original training and raw proposals with negative review. Failed earlier census
and v2 classifications remain, not overwritten.457 connected tests,3xfail;
Ruff/Pylance syntax pass and historical snapshot/census replay pass.
Next measured strategy must address typed memory synthesis; do not sweep the
other leaves with the same failed prompt or count deterministic controls.

### Original near prologue and stack-check success compose with the copy

Extended the existing caller runner with `--prologue`, not another framework.
Original05eb prologue bytes are
`5589e5b806009a3005dd1483ec06`; actual MZ relocation at05f4 targets
load+14dd:0530. Stack-check bytes are
`050002720d2bc47309f7d83b060e647201cbb8ca00e9c7fb`.
Unsigned ADD/SUB/NEG/CMP establishes success only when request+512 has no carry,
is strictly less than check-entrySP, and remainingSP >= DS:[640e].
The three failure branches reach0542, loadAX202 and jump010f. Failure dispatch
is explicit unresolved residue, not a modeled successful return.

A failed first original prologue run revealed a harness error: entry was far,
but original BP+4 expects a near return frame. Original trace copied from an
offset based on returnCS rather than supplied argument (0/12 expected matches).
No terminal evaluation ran. That archive and wrong method snapshot remain;
the error is not attributed to the model or original stack-check behavior.
Original tail095d `c9c20200` confirms LEAVE/nearRET2, separately checked.

Corrected external bridge saves/removes its far return words from SS, near
CALLs05eb, then restores the harness return after slice unwind. Original
prologue/stack-check/caller/move bytes remain unchanged, with both actual MZ
segment relocations. The original prologue establishes BP rather than an
injected frame. Harness-only MOV SP,BP/POP BP/RET2 after062e skips the unresolved
caller remainder; it is disclosed instrumentation, not its recovered epilogue.

For the owned near-entry frame, stack-checkSP=efe6, request6 leavesede0,
minimum cell tests0/e6/ede0, and copy entrySP=efd6. Logical pointer arguments,
full DS arena, declared registers/flags, guards and returnSP agree:

| Corpus | Original success-path contract | Host complete composition |
| --- | --- | --- |
| Training |12/12 |12/12 |
| Terminal, one evaluation |12/12 |12/12 |

This exercises the exact minimum equality boundary. Intermediate stack-check
AX/flags are not separately captured; subsequent caller operations overwrite
them, so acceptance is the enclosing success-path composition. The host enforces
minimum <=ede0 and fails explicitly otherwise; it does not execute the installed
manual0530 draft or accept its error-service behavior.

Reviewed only this success-path composition under owned input/DS/SS/stack
premises. Whole0530 still depends on010f failure dispatch; whole05eb also depends
on its unexecuted remainder/direct callees. Normal-program entry/stack-minimum
initialization, reachability, segment aliasing/wrap and native TP7 ABI remain
unknown. No target source/ledger/training promotion;28/295 count unchanged.
Zero model requests and weight changes. Scope recall is100%, correctness
probability and sensitivity remain unmeasured.

Evidence: successful session `files/move-caller-near-prologue-20261103/` with
method/runtime snapshots, frozen original-byte harness and host program,
both trace suites, `source-review.json`; failed
`files/move-caller-prologue-20261103/` with `negative-review.json`.
The freeze's older generic unknown list still names prologue; this review
supersedes only its scoped success-path obligation.445 connected tests passed,
3 expected failures; Ruff clean and positive/previous caller replay.

Hashes: freeze
`3827a42d5290a1f65bfd74b66593c786dfd2f007f13f9efbf05cee923a3c7b78`;
artifacts
`913738825090a6a6736d3569cc351ffe7e470eaf38dc5ca9d0ec422f172eb992`;
result
`906ed841aa0013804dba1015778579e8547174cb14db74733084d8facf874f63`.
Caller-specific source hash unchanged from the earlier slice; the host frame,
program, corpus and original entry are distinct evidence.

### Actual0629 caller composition: DS-relative arguments replace stale entrySI premise

Authenticated original1000:05f9..062e bytes, not exported CALLF text. The actual
MZ relocation is the segment word at062c (slice byte51), originally14dd.
It targets load+14dd:48e1, i.e. the checked byte mover. Caller setup derives:

- SourceDS:(66d8+3*unsigned byte SS:[BP+4]).
- DestinationDS:(5826+3*unsigned byte DS:[68+argument]).
- Count3, both far-pointer segment words pushed from DS.

The original caller leaves SI=2*lookup, not the source offset. This directly
invalidates arbitrary entrySI-as-source composition; original LDS supplies the
source from pushed arguments. Caller-specific typed composition now derives
offsets from these actual arguments and retains the common DS segment contract.
No host-pointer ordering replaces logical offsets.

`tools/liero_move_caller.py` is a bounded caller probe using existing source-trial
harness, assembler, DOSBox, Pascal/runtime and artifact helpers. An allocated
DOS code block holds original caller at05f9 and callee atblock+14dd:48e1; the
actual MZ segment relocation is applied. No original instructions are replaced.
An external RETF immediately after the slice returns to capture. Injected
entrySI1111/DI2222, frameBP=EFF4, argumentSS:[EFF8] and owned DS data establish
explicit conditional premises, not whole-program reachability.

One mechanical candidate, zero model requests:

| Corpus | Original contract agreement | Complete host composition agreement |
| --- | --- | --- |
| Training |12/12 |12/12 |
| Terminal, once after selection |12/12 |12/12 |

Argument/lookup0..15 and both entry flag settings are covered. Full4096-byte
DS5800..6800 arena, AX/BX/CX/DX/SI/DI/BP, DS/ES/SS, CF/ZF/DF, returnSP and stack
guards match. Original PF/SF/OF are checked separately, not host-native parity.
Source/destination3-byte ranges, low lookup cells, frame/stack and original-code
allocation are explicitly nonaliasing. The caller's ten argument bytes and far
return leave callee entrySP=EFDE; RETF10 plus caller-slice RETF restoresEFF0.

Reviewed exact caller-specific candidate
`17ce5169a13126d67616ed350a8d759dc7be7760f06b07774002fda61e504321`.
Accepted only as the scoped caller composition under these premises. Whole05eb
is deferred because preceding05f1 stack-check callee/prologue and normal-program
reachability are unresolved. Other48e1 callers, separate segments, wrap,
stack/global aliasing and native TP7 ABI remain obligations. Target source and
ledger are not promoted;28/295 reviewed routine count is unchanged. Reuse the
checked caller contract to constrain dependent work, not a claim of full recovery.

Evidence: session `files/move-caller-0629-20261103/`, exact caller/callee harness,
frozen source/corpora, original and Pascal training/terminal traces and
`source-review.json`. Replay passes without execution. The initial freeze saved
a method hash but not a method snapshot/predecessor path; later runner versions
add those. Historical limitation is explicit; no terminal rerun retrofits it.
437 connected tests passed,3 expected failures; Ruff clean. Regressions include
stale-register composition mutant, exact byte mutation, bounded inputs,
full-state mutations, tampered traces and selection-before-terminal controls.

Hashes: freeze
`825c8663a1dd82d676f7f682af477f1e07dfcbc22d45e1ab8b9bd9d5190bd55f`;
artifacts
`547aec306760e7eff2b13eb1f828cbebf12bb80d4df59951fc060d6c897367bd`;
result
`4baf05b568f2ed7d3f0c84fc2d29e0af11e354c6ac35bbaac5e93d5e095e936c`.

Fine-tuning remains separately gated: instruction/typed-copy supervision must
be relevant and reviewed, with family/project-disjoint transfer and retention
frozen before training. These now-known slices are development evidence,
not untouched recovery tests. No weight gain or training promotion is claimed.

### Typed hybrid48e1 composition passes training and terminal; caller scope remains

Added optional `--lowering-from` to the same source-trial runner, not another
framework or model sweep. It authenticates a previously selected checked
interpretation, refuses terminal-exposed predecessors and lowering chains,
then freezes one typed mechanical candidate and zero inference requests.
Only the checked48e1 action contract is supported; other alternatives fail
explicitly. PByte source/destination origins and signed LongInt loop bounds
preserve zero-count, direction, overlap and copy order. No model body is
silently repaired or credited with the human-authored emitted source.

One actual **v8** composed trial reused56 original training records and selected
the sole training-passing candidate before one original terminal evaluation:

| Stage | Complete declared-state agreement | Scope |
| --- | --- | --- |
| Training |56/56,100% required-case recall | Owned4096-byte arena plus declared register/flag/guard/SP state |
| Terminal |56/56,100% required-case recall | Fixed terminal seed, one evaluation, no repair |
| Inference/training |0 model requests,0 weight changes | Mechanical source lowering of retained Qwen3 interpretation |

Reviewed exact candidate hash
`942c4fc9488e788256d09c80508a9a3def8d5a71df81b7dafacd8722959e108f`.
The typed loop transfers destination from source in increasing or decreasing
index order; signed count-1 yields empty loops at count0. It follows supplied
logical backward, not host-address comparison. Under owned no-wrap bounds,
every access is in range and overlapping writes occur in original byte order.
Complete composition retains the existing wrapper's CF/ZF/DF and mirror effects.
Original PF/SF/OF remain original-only, not host/native parity.

The wrapper still assumes entrySI/DI already equal argument offsets and entryDS
equals destination segment. Original LDS/LES load actual argument far pointers
instead; arbitrary callers need not satisfy those assumptions. Separate segments,
wrap, aliasing with stack/globals, native TP7 ABI and normal-program reachability
remain explicit obligations. The exact reviewed composition is preserved in
session evidence, not installed as a generally recovered target routine.
Target ledger/attestations/training examples unchanged;28/295 source-reviewed.
This is a scoped hybrid success, not full routine recovery or blind model-written
Pascal. Probability of whole-routine correctness and sensitivity remain null.

Evidence: session `files/move-typed-lowering-v8-20261103/`, exact frozen body and
complete candidate, source/compiler artifacts, original training/terminal
records, result and `source-review.json`. Current replay passed before later
method changes; historical replay preserves all earlier negative trials.
429 connected tests pass,3 expected failures; Ruff clean.

Hashes: freeze
`de4e8c1ff5a72d5a44be9666dee70edda6d0135b0e2b9a46b64cb26def866e9c`;
artifacts
`0885a7cc2ccaeed132c56d2703aac6af41ac823a661a52dd38013f170f580906`;
result
`1c9014c8f0eeea443f0ce1cafef230576ea1ba52c460c60613c56dfc53b222c7`.

Fine-tuning could improve the failed Pascal synthesis, but the earlier7B
adapter was supervised on unrelated XOR/AND/add/OR byte transforms. This pass
does not measure a weight improvement. Relevant direction/overlap/typed-pointer
supervision and independently frozen transfer/retention checks are needed.
The now-known48e1 slice is development/debugging material, not an untouched
generalization task or automatically promoted verified pair.

### Citation completion passes; checked interpretation still lowers to wrong Pascal

Added bounded `--binding-from` in the existing48e1 interpretation-first runner.
It authenticates the initial archive, rejects evaluated terminal outcomes and
completion chains, selects the first prior action-compatible56/56 memory
hypothesis, and freezes its eight memory actions. One structured evidence-only
request may change branch/setup/transfer citations, not memory actions. Missing
address obligations are disclosed assistance; this is not independent discovery
or a weight-learning result. The old six hypotheses and failed freeze remain
unchanged. Citation gate, full-state oracle and two-source-request budget remain
unchanged. The checker verifies required address presence, not explanatory prose.

One immediate Qwen3:14b **v7** continuation made three requests total:

| Stage | Measured outcome | Qualification |
| --- | --- | --- |
| Evidence completion | Required explicit48f2/48f4,48f6/48fa/48fc,48fd supplied; no conflicts | Reused hypothesis, no new independent memory evidence |
| Memory interpretation |56/56 original training memory matches | Finite owned-arena memory agreement, not full ABI |
| Pascal proposal1 | FPC compile-failed at untyped `source^ := destination^` | Not executed; complete-state recall unmeasured |
| Pascal repair | Same FPC error, distinct source hash | Not executed; complete-state recall unmeasured |

Static inspection of proposal1 finds both PByte cursors initialized from
destination, decrements before copying despite the checked copy-then-step order,
and reversed forward assignment through untyped Pointer parameters. Repair
changes `q := destination` to `q := source`, but retains pre-copy decrements and
the wrong forward assignment. These are static contradictions, not measured
candidate execution results. Neither body was manually patched or installed.

Zero candidate executions, terminal evaluations, accepted source bodies,
promoted examples or weight changes.28/295 source-reviewed count unchanged.
The concrete blocker is now typed Pascal lowering faithful to the retained
interpretation, not inability to propose memory actions or complete citations.
This bounded batch stops; no third source request or terminal-feedback retry.
Do not equate successful interpretation with routine acceptance.

Evidence: session `files/move-binding-completion-v7-20261103/`, original training
replay, evidence/source prompts and raw responses, both compiler logs and
`negative-review.json`. Current replay passed before subsequent method changes;
historical replay remains available.420 connected tests pass,3 expected
failures; Ruff clean. New regressions cover immutable actions, missing citations,
action injection rejection, predecessor integrity, no completion chains and
terminal access only after source selection.

Hashes: freeze
`9b8e1c90842740e83085f4e937a4dfed8e7e9baa20b03acfe4793c4b4288b33c`;
artifacts
`c914562e7283685930eb1664820f5450fa1c51ea7fde840212a621b1be917698`;
result
`c4a7a8ead2900c91dde255d5690207618e486162baba1d8720af4e2ed35d69d9`.

### Interpretation-first48e1: memory hypothesis improves, citation gate blocks code

Added `--interpretation-first` to the existing residual source-trial runner:
two structured interpretation requests maximum, up to three alternatives each,
then at most two Pascal requests only after an interpretation passes. Exact
original bytes are checked at freeze; enumerated constraints bind unsigned
CMP/JNC direction, ADD/DEC setup, DF, and REP MOVSB memory actions. A bounded
owned-arena interpreter checks every hypothesis against authenticated original
training memory. Alternatives, byte conflicts, memory counterexamples, hashes
and raw model responses are retained separately. Complete-state candidate and
single-terminal policies are unchanged. No probability estimator was invented.

One immediately following live Qwen3:14b trial reused56 prior original training
records. It made exactly two requests and produced six hypotheses:

| Request | Hypothesis memory matches | Instruction binding outcome |
| --- | --- | --- |
| Initial |16/56,44/56,16/56 | Wrong memory actions and missing citations |
| Training-feedback repair |56/56,16/56,32/56 | Missing citations in all three |

The first repaired hypothesis chose all eight memory alternatives correctly:
backward when source offset is smaller, no zero-count access, forward index0,
backward indexcount-1, steps+1/-1, copy before advancing and count repetitions.
Its branch evidence was only `24dd:48f2`; setup was `24dd:48f6-24dd:48fb`.
The frozen citation checker requires explicit48f4JNC and48fcSTD (and48faDEC)
as well. It does not parse address ranges. Thus the useful56/56 memory
interpretation remains provisional, not a fully instruction-bound selection.
No gate was relaxed and no additional requests were made. This distinguishes
model memory understanding from citation/transport limitations.

Zero Pascal requests, compiled candidates, terminal checks, accepted routines,
promoted examples or weight changes. Source-reviewed count remains28/295.
Human-designed alternative vocabulary and checker are disclosed assistance,
not unseen blind discovery. Memory recall is not full-state recall, sensitivity
or calibrated probability of whole-routine correctness.

Evidence: session `files/move-interpretation-first-20261103/`, including
`freeze.json`, interpretation prompts/raw responses/history, `result.json`
and `artifacts.json`. Replay with `--historical` after subsequent method changes.
Regression controls prove no code before interpretation selection, training-only
repair, retained competing hypotheses and complete-state composed execution;
controls are not live model recoveries.

Validation:417 connected tests passed,3 expected failures; Ruff clean. Historical
replay validates this trial and the preceding v6 negative archive without model
requests or another original execution.

### Consistent residual prompt: real producer bug fixed, recovery still blocked

The saved7B residual prompt requested a complete include, param_2/param_3 and
all register mirrors before appending an incompatible body-only interface
with source/destination and no Register symbols. Local inference also requested
JSON even though synthetic adapter supervision used raw Pascal. This was a
producer bug, not solely model inability to follow a consistent interface.
`residual_prompt` now stands alone; local Transformers inference asks for raw
Pascal, while structured Ollama transport asks for source JSON. Repair feedback
requests the residual rather than the composed include and does not supply
the wrapper as a previous model body.

An additional exact-byte correction resolves48e1's exported
JNC0x2000:96cd to **24dd:48fd**: opcode7307 at48f4, next48f6 plus signed7.
Final8eda remains MOV DS,DX. The helper applies these corrections to model
listing context without rewriting the original exported assembly.
Binary/relocation identity is still checked by each freeze. These fixes do
not change wrapper behavior, source/verification gates or original observations.

One immediately following **v6** trial used the same installed7B base with
two requests/2048-token budget, the corrected raw-body prompt, unchanged
byte-derived wrapper and authenticated56 original training records.
First proposal still emits markdown, dereferences PByte(SI)/PByte(DI), calls
undefined movsb and never decrements cx; count0 also attempts a copy.
Repair still uses numeric register pointers and moves before copying on both
branches, producing off-by-one accesses. Both rejected before compilation.
No candidate execution/selection, terminal evaluation, installed source,
training/example promotion or weight change. Fixture recall and correctness
probability remain unmeasured, not0%; source count remains28/295.

This is still a developer-known, implementation-unresolved development case,
not blind generalization. The exact prompt and listing bugs are removed,
but a pass cannot be obtained by stripping fences and manually fixing pointer/
loop semantics then crediting the model. Stop this bounded run; do not extend
it with another calibration, model sweep or prompt-only retry.

Evidence: session `files/move-residual-consistent-v6-20261103/`, including both
raw proposed bodies and separate negative `review.json`. Identities:

| Artifact | SHA256 |
| --- | --- |
| freeze.json | `c08cabb707774239a837cd01963769f619bb3b4a896ee33f310ad9f771082ee6` |
| artifacts.json | `0a07a45736b28a796eabc63734dd5d63fd957ee3ffdff6add6e79f7b080b3b7f` |
| result.json | `ce07ae645a9236a056f1babc8766d34de67aba87f479790e810a427e5e580446` |

405 connected tests pass,3 unchanged expected failures; Ruff/editor checks
clean. All eleven source-trial histories and reviewed calibration replay
without generation or execution. v6 current replay:
`uv run python -m tools.liero_source_trial --replay --output <v6-directory>`;
older method snapshots require `--historical`. Earlier results remain failures;
this correction is not a retrospective recovery or additional model training.

### Composed residual recovery and an actual7B QLoRA experiment

Implemented optional `--residual` in the existing source-trial runner.
The model supplies only a nested Pascal memory body; exact-byte48e1 ABI effects
are supplied independently by a wrapper. Canonical declaration, CX/offset/
CF/ZF/DF effects and SP+14 remain checked together with the complete arena.
This is static assistance, not model-inferred ABI. Wrapper scope requires entry
logical SI/DI to equal source/destination argument offsets and entryDS to equal
the destination segment, as supplied by the owned fixture; arbitrary callers
are not established. Tests distinguish invalid services/ABI writes from valid
Pascal hex constants and catch incorrect return cleanup.

The mandatory immediate development trial ran after this one preparatory batch:
Qwen3 emits a procedure declaration despite the body-only interface; its body
also uses the same forward-indexed loop on both branches and Word count-1 at
count0. Repair remains invalid. No candidate execution or terminal evaluation.
Evidence: session `files/move-residual-qwen3-20261103/`.

The user explicitly chose7B QLoRA and permitted compatible weight downloads.
Pinned Apache2.0 `Qwen/Qwen2.5-Coder-7B-Instruct` revision
`c03e6d358207e414f1eca0bb1891e29f1db0e242` was downloaded locally.
The existing trainer now supports explicit NF4/double-quantized experimental
training and an explicit development split. Experimental adapters never get
automatic production activation. The existing adapter loader supports explicit
quantized base/adapter inference with the model chat template and context/output
budget errors, not silent endpoint fallback. The training extra/lock now includes
bitsandbytes. These are optional ML dependencies; ordinary engine use remains
stdlib-only.

`synthetic_residual_dataset` produced32 labeled FPC/x86_64 pairs, each compiled
and checked against all256 byte values under a supplied count256 arena.
24 train pairs cover XOR/AND/addition;8 OR-family development pairs are excluded
from training. Source/template-family identities are recorded;416–437 tokens
fit the1024 sequence budget without truncation. No48e1 body/control/proposal,
unverified C or Liero gold label was used. Modern FPC instruction examples
are explicitly not TP7 original binary recovery.

One actual CUDA job completed on the12GB RTX4080 Laptop GPU: NF4, rank8,
batch1, gradient accumulation4, sequence1024,3epochs,18 optimizer steps.
No OOM training backoff was needed. Synthetic development loss changed
**0.893572 -> 0.038920**. This changes adapter weights, not base weights; it
does not prove behavioral recovery gain. Dataset, methods, driver, model files
and resources were frozen in `files/qlora-coder7-20261103/freeze.json`.
Adapter and manifest are under its `sequence-1024/experimental-synthetic-fpc/`
run directory; `activation_allowed` is false.

Equal-budget explicit7B base and adapter each received two48e1 residual requests
using the same original training observations:

| Model | Development result | Fixture recall |
| --- | --- | --- |
|7B base | Markdown/JSON wrappers, procedure/assembler or numeric pointer emulation | Not measured: no executable accepted proposal |
|7B adapter | Markdown JSON wrappers; inspected bodies ignore source or increment count indefinitely | Not measured: no executable accepted proposal |

No48e1 training execution/selection, terminal evaluation or accepted source.
The model-identity finalizer initially compared local weight identities against
Ollama's default model, a runner bug. Fixed backend-specific checking and
authenticated/finalized the saved rejected selections **without another model
request or original/candidate execution**. Both histories retain the original
method snapshot and an explicit bookkeeping-repair note.

Synthetic development-family behavior was measured separately, one request per
model per eight OR tasks. Base emitted inadmissible representations on8/8;
these unexecuted proposals have no byte-case recall. Adapter emitted8 executable
bodies;7/8 fully match the256 retained byte cases each. One proposed addition
instead of OR1, matching128/256. Aggregate evaluated byte-case agreement is
**1920/2048 =93.75%**; complete-task agreement is7/8. This is useful evidence
of improved output discipline and bounded synthetic behavior, **not unseen
Liero recovery or population correctness probability**. OR development also
selected the adapter checkpoint, so it is not an untouched terminal test.

Retention first hit an inference-cache OOM when holding two7B models at once.
Fixed eviction of this loader's own cached model before switching; no other
process was terminated. Base observations were preserved and only the unstarted
adapter retention phase ran afterward. No completed proposal was retried.
There is no untouched supported routine in the current reviewed trial panel:
40d6/3d68/48e1 all have developer knowledge/prior assessments. No generalization
claim, fabricated holdout, fixture expansion, retraining or automatic activation
follows. Source recovery remains28/295; target source/ledger and gold corpus
were not changed.

Validation:403 connected tests pass,3 expected failures in unchanged target
includes; Ruff/editor checks clean and all ten old/new source-trial archives
plus calibration replay. A separate fixed "OK" loader-switch check confirms
live base->adapter eviction on CUDA, one cache entry and approximately5.6GB
allocated each; this is a mechanism check, not another routine/model assessment.

User-requested per-proposal assessments now report matched/evaluated required
cases and `required_case_recall` on executed complete-state fixtures.
Unexecuted/rejected candidates report not measured, not zero. Whole-routine
`probability_correct` remains unknown; sensitivity is unavailable without a
labeled positive/negative classification corpus. Deterministic, overlapping
fixtures do not justify a statistical population probability or confidence
interval. Training and terminal assessments remain separate.

Session artifacts: `residual-qlora-freeze.json`, `qlora-synthetic-20261103/`,
`qlora-coder7-20261103/`, `move-residual-coder7-base-20261103/`,
`move-residual-coder7-adapter-20261103/`, `qlora-retention-20261103/`.
Read-only source-trial replay uses `--historical` where method snapshots differ.
The bounded experiment is complete: do not begin another calibration or model
sweep. The concrete remaining gap is learning admissible directional memory
behavior on Liero instructions, not merely producing Pascal or lowering loss.

### Explicit three-model local comparison

At the user's request, the same unimplemented48e1 routine was assessed with
all three installed alternatives: DeepSeek-Coder-V2 16B Q4_0, Qwen3 14B Q4_K_M
and Phi-4 14B Q4_K_M. This was an explicitly authorized bounded comparison,
not implicit panel expansion. Session `files/local-model-comparison-20261103.json`
fixed model order, equal2048-token output budgets, one proposal plus one repair
per model, identical byte-backed prompt and the previous56 original training
observations before generation. No cross-model candidate/terminal feedback.
Each model had its own predeclared training selection and terminal policy;
no global winner was selected using terminal results.

| Model | Initial proposal | One repair | Outcome |
| --- | --- | --- | --- |
| DeepSeek-Coder-V2 16B | Repetitive RTF-like text inside source JSON, truncated at2048 tokens; malformed JSON | Copies the supplied obligation JSON into source rather than Pascal | No executable candidate |
| Qwen3 14B | Emits a full Pascal unit, rejected by include-only gate | Emits unit plus assembler, rejected | No executable candidate |
| Phi-4 14B | Invalid Pascal declaration (`Pointer) is`); treats scalar RegisterSS as an array | Identical parsed source | No executable candidate |

Review of Qwen3's first body finds a plausible directional host-pointer loop,
but also loads ES from destination data and omits required mirror effects.
Phi-4's first body lacks any forward memory copy, does not position backward
pointers at the end, and leaves DF set on that branch. These are not solely
overstrict-format failures; none is accepted by manually editing its output.
Qwen3 returned no separate thinking text in this configuration; this is not
a comparison of every reasoning mode or optimal model-specific prompting.
DeepSeek's truncated repetition is not evidence that a longer budget alone
would solve recovery. This small equal-budget assessment establishes no
general ranking of model capability.

Six requests total, zero training candidate executions/selections, zero terminal
evaluations or accepted recoveries. No new original execution: all three
authenticated/reused the same56 training records. Source, ledger, corpus and
weights unchanged. All three archived trials pass read-only integrity replay.
The earlier Qwen2.5 failure remains separate, not a fourth new routine.

Session evidence directories and SHA256 identities:

| Directory under files/ | freeze.json | artifacts.json | result.json |
| --- | --- | --- | --- |
| move-deepseek16b-20261103 | `245c9bd918f4efc662ef81248c764732a9ea583faf2b6ed675034b5500b27a30` | `98233467d69848e16b1023a39a0e3dfd1ac7ea4c145cbbcc7f208a60d2a29735` | `5c275934e90045c30bdb6e5b4fff2d16a3cc475a9f02ea0af9f7a0b527a92f8a` |
| move-qwen3-20261103 | `d9cf617f492023fbf1ca3ff994da147eac056aa3b0bd880c159ea7ff994dd74e` | `76420f921575d96d9e9fa4efde444023ba658ed56c566f2f72b2381600a99c5c` | `d8bd2db753b958280ab1b2677f617a2d9f422d81b81c8b3533a9be1a981c3144` |
| move-phi4-20261103 | `f1a17d5b36e46cbc837a443bd31c1948a68626351d42c936d5e07037d185b5c3` | `ec655f6cb0cdbc1e15de815135a506dffcf0882dbb72f6fb76c7e88067e9d05a` | `fd148c75dd9c768e0de946e32e8e289daad98ec2edcf3d0db9c0f53e521acfe5` |

Replay each with `uv run python -m tools.liero_source_trial --replay --output
<directory>` (add `--historical` if method/runtime later changes).

Fine-tuning remains a plausible next method, not established improvement.
Read-only `uv run python -m engine.model_training --target liero --readiness`
reports0 marked-verified Pascal pairs,81 separately labeled unverified C pairs
and no verified Pascal projects. The current64-pair/two-project threshold is
an operational policy, not a scientific minimum for an adapter experiment.
Reviewed manual routines can be considered for explicitly scoped, revalidated
training labels; they are not automatically gold binary/native examples.
Compiler-generated lawful Pascal/assembly pairs can teach syntax and pointer/
ABI representation, but are synthetic assistance, not Liero recovery evidence.
Keep related routines/projects and all assessed48e1 data out of an untouched
future behavioral test. Evaluate base versus adapter with equal budgets,
binary-backed recovery checks and retention, not token loss alone.
Existing local LoRA code needs compatible local Transformers base weights:
installed Ollama GGUF inference files are not directly trainable by that path.
No training job, base-weight download or automatic adapter activation was started.

### Reusing manual solutions; implementation-unresolved move assessment

The current audit answers which older pieces can be reused: **28 current
source-reviewed bodies**, including **10 accepted under the repository's
modeled-behavior gate**; the other18 retain explicit verification limitations.
Those10 are235c:04f3/135f and24dd:04dc/05fd/0642/350e/3e63/3e7c/4919/492c.
An additional old source review for24dd:3f86 is stale because its Pascal changed.
All29 ledger-marked bodies have host passes, but the stale one does not count
toward28. No full-native binary passes. Reuse current checked contracts where
their premises apply; do not re-solve all manual bodies, promote their scoped
results to arbitrary native callers, or count them as automated unknown recovery.
Source review is not automatic gold-training eligibility.

The next target was the genuinely **unimplemented include** `FUN_24dd_48e1`,
a callee-free direction-sensitive move. The existing runner now supports
repeatable `--routine` selection and `--enforce-outputs`: canonical declaration
checking before compilation, exact-complete-byte-bound output/return obligations,
and up to three named training-state counterexamples (including CX/SI/DI/returnSP),
not just an opaque mismatch count. Every byte mutation of the obligation table
is rejected in tests. Original default CLI panel remains40d6/3d68; historical
replay uses each frozen panel rather than the current expanded fixture table.

This is disclosed assistance: developer read the listing/decompiler while
scoping and wrote a fixture control, withheld from the model. The exact interface
and output obligations were supplied. It tests recovery of an unimplemented
source body, **not blind semantic discovery** or independent generalization.
Original36 bytes at file110113 prove final `8eda` is MOV DS,DX, not the exported
listing's reverse direction. Both offset-directed branches, zero count,
overlap, complete owned4096-byte memory, flags/registers and RETF10/SP+14 are
covered by the independent fixture contract.

One frozen assessment:

```
uv run python -m tools.liero_source_trial --routine FUN_24dd_48e1 \
  --enforce-outputs --output <new-directory>
```

All56 original training observations match the independent full-state fixture
contract. Two requests produce one distinct parsed include; repair duplicates.
The declaration and SP+14 are correct, but it dereferences numeric DOS stack/
segment/register values instead of host pointer parameters and is rejected
before compilation. Separate rejected-source review also finds forward-only
copying on the backward branch, stale final DF and omitted CF/ZF effects.
**0/1 recovered**, no candidate execution/selection or terminal evaluation.
This confirms prompt obligations do not by themselves solve representation/
behavior inference; the exact declaration gate is necessary, not sufficient.

The25% floor stops expansion. No installed include, ledger, corpus or weights
changed. Do not repair this body manually and relabel it model recovery.
Before another live run, demonstrate separately checked derivation/composition
of mechanical ABI effects and model-inferred memory behavior. Any supplied
memory algorithm remains a disclosed control, not an unknown-routine proof.
No new framework, larger panel or model sweep is justified by this failure.

Evidence: session `files/unresolved-move-obligations-20261103/`, including
frozen method/runtime/byte/prompt/model identities, original records, both raw
responses, failed selection and separate negative `review.json`.

| Identity | SHA256 |
| --- | --- |
| freeze.json | `7706e8133205e8b59f64359a5df980960660a3c22041aa2dc7f413a109f77dcc` |
| artifacts.json | `6ac5be55df08540450fc38755186478c91d18e701e0dfa41e3f65f1cbc315e57` |
| result.json | `d5d7b7dd2fd539585c9116d9a819a40fd6724356850837fd7fe3b17a4c1b419e` |
| rejected parsed include | `0dcaa9165d021eaefa1045274813a8a74ff490daab94e7534ed31fb0737ef8f5` |

Read-only replay: `uv run python -m tools.liero_source_trial --replay --output
<move-directory>`. v1/v2/v3 and reviewed calibration archives also replay
historically; no further original/model execution.377 connected tests pass,
three expected failures for unchanged unreviewed/unimplemented target includes;
Ruff and editor/syntax checks pass. Source acceptance stays28/295.

### Known-source representation calibration and assisted retry

The representation reopening gate was tested rather than another unchanged
prompt retry. `tools/liero_source_trial.py --calibrate` freezes two explicitly
developer-supplied Pascal bodies, their adapter contracts, actual runtime/
method/prompt identities and local model digest before generation. One request
per task, no repair: the model adds numeric register effects to a host-pointer
masked-byte update and an ordered two-byte update. These are **known-source
syntax/adapter calibration**, not Liero original-byte checks or unseen recovery.
No new binary fixture, model sweep, training or dependency was needed.

Both generated adapters pass all65536 scalar words under the frozen dirty
32-byte arena/entry-register pattern: full memory and all available register/
flag mirrors, including SP/DI wrap cases. This is exhaustive over that scalar
domain, not over every possible initial memory/register combination.
Complete straight-line review separately confirms the supplied memory
behavior, writable one/two-byte bounds, mirror preservation and numeric
updates. Both use `PByte(target)` rather than numeric DOS addresses. Passing
provided-body adaptation does not prove that the model can infer a complete
routine from instructions or that weights improved.

A separate `review.json` binds each candidate, freeze and artifact manifest.
The runner refuses to reuse calibration based only on a pass label: it checks
all archived artifacts/input snapshots, actual runtime identity, all65536 saved
records, candidate/review hashes, original prompts and model identity.
`--calibration-from <reviewed-directory>` also requires authenticated
`--training-from <prior-run>` and freezes exact example/review identities in
the new run. Reviewed examples are included in full and explicitly labeled
as supplied-body assistance; no target body or target loop sketch is supplied.

One separately frozen **v3** strategy ran on the same40d6/3d68 panel:

| Routine | Outcome | Complete review |
| --- | --- | --- |
|40d6 initializer | First proposal contains forbidden assembler; repair fails compilation | Invents third pointer parameter, violating the required two-argument declaration; also implements the wrong memory algorithm |
|3d68 copy | Compiles/runs; all56 training arena memories match, but complete state matches0/56; repair duplicates source | Correct host-pointer forward-copy memory behavior for the declared owned nonwrapping domain, but omits mirrored CX0/SI/DI updates and models RETF10 as SP+10 instead of SP+14 |

This narrows the blocker: supplied-body host-pointer adaptation is possible,
and the copy's pointer representation no longer crashes, but complete
signature/register/return-contract reconstruction is still unreliable.
The memory-only result is not acceptance, an independent generalization
test, a whole-routine pass or evidence of weight improvement.
Four v3 requests, three distinct raw bodies and one duplicate repair.
No candidate passes training; no terminal evaluation, installation,
attestation, corpus entry or weights change. No new original calls: the
same112 original training calls were authenticated/replayed from v1.
Yield remains0/2 below25%; **frontier expansion stays stopped**.

Session evidence:
`files/pointer-representation-calibration-20261103/` and
`files/whole-source-model-trial-v3-20261103/`.
They retain complete freezes, code/runtime snapshots, prompts/responses,
compiled adapters, outputs, independent review and saved failures.

| Identity | Calibration SHA256 | v3 SHA256 |
| --- | --- | --- |
| freeze.json | `987bb944d90f211b7f6d6e9a223c7b7a7eb572959ca83e6f7b43e09a912d05d7` | `715126726ca8c090886f5a0a609261cc8cc5ac138d5b8859389fdd38aa87a562` |
| artifacts.json | `21d16297bd8e2c08e1143f3d8ee6f349cb03aa1d25c45e0923c7529a7c910734` | `94e4a40f3c8c1977ae7d8bccfe3136ed844f9200876e5dc3d10e6af6a67e7e57` |
| result.json | Bound by artifact manifest | `ca658adf00b6c308293a434a77ff4b25693d7d16ec57e6cb732947c7ca05653c` |
| calibration review.json | `ea819b2a226e2a94fa724303856c8533f494ce2eaaec6d7eb58040b6cff46b8c` | Bound as v3 calibration dependency |

Read-only historical replay:
`uv run python -m tools.liero_source_trial --calibrate --replay --historical --output <calibration-directory>`;
`uv run python -m tools.liero_source_trial --replay --historical --output <v3-directory>`.
All three recovery histories replay without another original/model run.
Later replay hardening also rechecks failed candidates' training output and
the attached calibration/review; it is regression-tested, not another trial.

Validation:189 connected tests pass, two unchanged expected failures for
unreviewed target includes' missing mirrored effects.51 focused tests pass.
No target source/ledger/runtime was changed. Do not repair candidates manually
and reclassify this failed live trial as model recovery. Before any further
generation, the exact declaration, all observable clobbers and far-return
cleanup need enforceable, byte-backed obligations; simple supplied-body
calibration alone has now been shown insufficient. No broader panel, unchanged
retry or gold-label/weight promotion follows from this result.

### Whole-source model batch: zero accepted routines, expansion stopped

The bounded whole-source experiment is now executable via
`uv run python -m tools.liero_source_trial --output <new-directory>`.
It reuses the existing pilot's local proposal/sanitization/model-identity
helpers, MZ evidence loader, DOSBox runner and actual LieroRuntime.
It never installs source, attests recovery, promotes examples or trains weights.

The predeclared two-routine panel is callee-free:

| Routine | Authenticated original | Complete static contract |
| --- | --- | --- |
| `FUN_24dd_40d6` | File108054,22 bytes, no overlapping relocation | CLD; load destination/scalar from far-call stack; store scalar word followed by15 zero words; AX/CX0, DI+32, CF0/ZF1; RETF2 leaves the destination pointer words on the original stack |
| `FUN_24dd_3d68` | File107176,24 bytes, no overlapping relocation | Save entryDS inDX; load source/destination/count; CLD and forward REP MOVSB, including zero count/destructive overlap; restore DS; RETF10 |

Actual final copy bytes `8eda` mean **MOV DS,DX**, not the exported listing's
MOV DX,DS. The prompt corrects this from original bytes; the historical listing
is retained unchanged. Both target includes already contained manually written,
unreviewed bodies and host tests. Neither body nor its decompiler was sent to the
model. That disclosure still prevents claiming an unseen-routine benchmark.

Before any proposal, freeze original binary/region/relocation identities,
model digest, prompts, source/runtime/method snapshots, input hashes, budgets and
stop rules. Each routine has56 training and56 disjoint terminal arena cases.
Every case captures all4096 owned bytes plus32 bytes of original registers,
flags, stack/segment observations and guards. Initializer values include
0/1/7fff/8000/ffff, odd/even destinations and arena boundaries. Copy inputs
include zero and lengths through1024, equal pointers, both overlap directions
and separated ranges. Native PF/SF/OF/segments/stack checks are not host ABI
parity; the host checks available logical register/CF/ZF/DF mirrors and memory.
Model mirrors supply input offsets and callee-entrySP; actual host pointers
resolve parameters, not numeric DOS addresses.

Scope: sequential owned nonwrapping ranges in original [8000,9000), supplied
DS=ES=SS=CS, code/captures below6000 and stack nearEFF0; no asynchronous mutation.
This domain does not establish arbitrary segmented aliases, offset wrap, actual
caller provenance or normal reachability. Full source acceptance would also
require complete path/invariant review, not just finite cases.

Frozen budget per strategy: two proposals/routine (one training-only repair),
2048 generated tokens, temperature0,600s request and30s execution limits;
first complete training pass selected, terminal once, no terminal repair.
Actual local model `qwen2.5-coder:14b-instruct`, digest
`9ec8897f747e246e970bc5cfdda85d22f1123dc2e3d34978a010a75968716849`.
No model sweep, supplied loop sketch or manual candidate repair.

| Strategy | Initializer | Copy | Accepted routines |
| --- | --- | --- | --- |
| v1 raw complete Pascal | Compile fails: undefined raw register names and invalid numeric stack accesses; repair duplicates source | Compiles, crashes with runtime216 on numeric-address dereference; repair duplicates source; static review also rejects count/return handling |0/2 |
| v2 explicit host-pointer representation | Both proposals still attempt numeric register/stack dereference; rejected before compilation | Same representation failure; rejected before compilation |0/2, same two routines |

Eight requests across both strategies produced four distinct parsed bodies;
all four repair requests duplicated their initial bodies. Historical v2 logs
label both rejected proposals `proposal-failed`; subsequent runner hardening
deduplicates parsed representation-rejected bodies too. Do not rewrite those
logs as if the later guard ran earlier. Replayed training is not independent
new evidence or another attempted routine.

Only the two original training suites ran:112 calls total. Both pass the
independently derived static-state contract. v2 authenticates and reuses those
same traces; it does not rerun already measured seeds. No candidate passed
training, so **no terminal original or Pascal evaluation ran**. Every generated
body is ineligible for source acceptance; target includes/ledger/corpus/weights
remain unchanged. Yield0/2 is below25%: stop frontier expansion, not evidence
of permanent unrecoverability or of a stronger model.

Persistent session directories:
`files/whole-source-model-trial-20261103/` and
`files/whole-source-model-trial-v2-20261103/`.
They retain freezes, old source/method snapshots, prompts, raw model responses,
original traces/COM images, compilation/runtime failures and hash manifests.

| Identity | v1 SHA256 | v2 SHA256 |
| --- | --- | --- |
| freeze.json | `25367ad21c69a95c2ce4a00bb8ca2a47b355a1da252ec5475abb5a1024b97328` | `add34f64c72bd239f256c52d63e96adbb576b594cb67b9c570b980a727388a81` |
| artifacts.json | `b5e87ee48c7933b26c097948c482f7678a8512ce2ce036255460672e1439925c` | `7532a22e124cd61f37e9b08627b919eec2e010310e4d03c1b703ce1ae6762960` |
| result.json | `9427c4e187a3c7a50c6912286e7a9090a808eadf12e58925aa7b7581611d5ed4` | `35ab50cee047476fed18b7f7f7d019f49bdd6c6f18510547a3a1a8ecfe4f46cb` |

Both replay via
`uv run python -m tools.liero_source_trial --output <saved-directory> --replay --historical`.
This verifies archived input snapshots/artifacts and rechecks the unchanged
case/trace contract without new execution. Strict replay omits `--historical`
and additionally requires current method/runtime identities; it deliberately
rejects method drift. Later runner changes retain per-request prompts, reject
numeric PByte casts and report the expansion stop explicitly. They have unit
coverage, not a third live model evaluation.

Validation:186 connected tests pass, two expected failures explicitly retain
the old **unreviewed** includes' missing register/flag effects. Those tests
become normal mandatory passes if source is attested; no generated body is
substituted to make them green.48 new fixture/orchestration tests pass, including
supplied controls, full-record mutation rejection, selection-before-terminal,
no terminal repair, duplicate rejection and predecessor replay/leakage gates.
Ruff/Pylance syntax pass. Target proxy builds with35 existing warnings.
Audit remains28/295 reviewed sources,4 partial,35 host passes,0 full-native,
one stale and four invalid historical reports; six older scoped checks replay.
Readiness remains0 marked-verified Pascal pairs versus81 legacy-unverified C.

Concrete blocker/reopening gate: the model has not learned this target's
parameter-to-host-pointer/register boundary. Another unchanged prompt retry
or more binary fixtures does not resolve it. A future bounded calibration
must establish that representation on disclosed known-source tasks first,
then freeze a new recovery assessment; such calibration is not itself unseen
recovery or a weight-improvement claim. Device-dependent frontier work remains
deferred. No source body or training label can bypass the existing review gates.

### Source closure: pending-error take-and-clear04ed

The complete seven-byte callee-free `FUN_24dd_04ed` is now reviewed as source
under the existing logical DS-global/register model, not just as a separate
Pascal projection. Original bytes at file92717 are
`33c087061064cb`, with no overlapping MZ relocation:

1. XOR AX,AX establishes AX0, CF0, ZF1, PF1, SF0, OF0; AF is undefined.
2. XCHG word DS6410,AX returns the previous word and stores0 without changing
   flags. In particular **ZF remains1 even for a nonzero returned error**.
3. RETF consumes only the four-byte far return. No arguments, branches,
   calls, device operations or further paths are hidden in this body.

The previous target source returned/cleared the logical word but left modeled
AX/CF/ZF stale. A focused actual-source test reproduced exit2 before the fix.
The installed include now sets RegisterAX to the old word, clears
GlobalWord6410 and sets CFfalse/ZFtrue, preserving modeled DF/other registers.
No runtime-unit change or generic port/memory framework was needed.

`tests/test_liero_error_exchange_source.py` compiles the actual include plus
LieroRuntime with FPC-Mtp-Cr. All65536 old-word values pass; inputAX is the
complement, CF starts set, DF alternates, and an immediate second call returns0.
The single original execution makes131072 calls and checks all32 surrounding
global bytes, output flags (excluding undefinedAF), BP/SP/DS/SS, preserved
BX/CX/DX/SI/DI and two stack guards. Static inspection also accounts for the
unchanged segment registers/remaining flags. PF/SF/OF and native stack
observations are original-only, not host ABI equivalence.

**Required scope:** the mirror represents the intended writable DS6410 word;
original DS=SS=CS is supplied in the fixture; globals6400..6420, code/captures
below6000 and stackeff0 are owned and disjoint. No asynchronous/concurrent
cell mutation. Original memory-XCHG atomicity is not implemented by two host
assignments; host multithread atomicity, arbitrary original aliasing, actual
caller DS/lifetime and normal reachability remain outside source-model
acceptance. This is a whole straight-line source review plus exhaustive
declared input/output corroboration, **not** finite-trace promotion to full
native ABI or whole-program recovery.

Persistent session evidence:
`files/error-exchange-source-20261103/test_original_vs_actual_error_0/` has
pre-run freeze, original image/harness, actual-source/runtime/method snapshots,
compiler logs and full original/Pascal outputs.

- Actual source SHA256:
  `d6eb12c0c0584230d15ef73574ebeadbdd8027f639e8aefd24e891ed64a25fd2`.
- Freeze SHA256:
  `fdc03d2d6532e2bde271dd3b9ff43699b7601ec09f7141b5e757ad5270c2aa7f`.
- Original output SHA256:
  `b984a01737a68a4f3b805afa06fd3a20368e028cf05989d1200c0b9ecc465067`.
- Actual Pascal output SHA256:
  `57b02200d11e6101047f046a2e32fe213ccd411d6c6bd5b6b3cf27ed1cf7814e`.

The recovery ledger records this one reviewed source body, with full-native
binary status still blocked. No caller or sound callback is promoted, and
neither knowledge corpus nor weights change. This manual repair/known-body
review is not an unseen model recovery or a new training benchmark.
It is a concrete source milestone on the pending-error dependency also read
by the cleanup/termination chain. The real caller202c:088d consumes AX then
tests it itself; its file-operation callees and data provenance remain
unresolved, not solved by this leaf.

Validation:618 connected tests pass,11 historical/original execution tests
excluded (the new exhaustive original run passed separately and was not
repeated). All six prior freezes replay; exact new source/artifact identities
remain intact. Target proxy build passes with35 existing warnings and
unresolved residue retained. Audit now28/295 reviewed sources,4 partial,
35 host passes,0 full-native binary,1 stale; four invalid historical reports
stay invalid. No unchanged original trace is counted as independent evidence.

### Routine-closure checkpoint: sound initialization and actual-source anchor

The existing conditional graph now authenticates the43 original bytes at
module13646 and21 bytes at module024e, with only the caller's actual far
segment relocation at prefix+19. The main caller pushes DS65d2 as a word,
then three byte-derived words from65d4/65d5/65d6, and calls relative135c:0086.
Its ENTER6 frame reads the first argument at SS:BP+12 and writes:

| Port cell | Value under the checked prefix |
| --- | --- |
| DS67d0 | unsigned16(base +6), reset |
| DS67d2 | unsigned16(base +10), data read |
| DS67d4 | unsigned16(base +12), command write/status read |
| DS67d6 | unsigned16(base +14), receive status |

This removes a guessed port constant from the dependency chain. It does
**not** establish the caller's DS/configured base, physical device, successful
reset, callback installation or later cell lifetime. No device-model migration
or new original probe was added. Existing graph17 nodes/38 facts/19 edges has
no conflicts; initialization facts/edges are static, runtime applicability
stays unknown. The six historical freezes still replay unchanged.

To move toward whole routines rather than more projections, the existing
`test_actual_size_helper_all_unsigned_inputs` was executed with persistent
output. It compiles the **actual reviewed target source** `FUN_24dd_04dc.inc`
and `LieroRuntime.pas`, not a separately rendered candidate. All65536 AX
inputs match the original17-byte helper for modeled AX/DX/CF/ZF/DF and
returned packed value. Original-only checks additionally cover BP, SP balance,
DS/SS. This revalidates an already source-recovered arithmetic routine; it is
not a new routine, unseen-model success, full native ABI or normal execution
claim. Its accepted source and review identity remain unchanged.

Evidence in session `files/closure-actual-size-source-20261103/`,
`test_actual_size_helper_all_un0/`:

- Actual source SHA256:
  `6f1bfbe8a87b369de886aa2bdbc8a52c196b6241cac5c0472988cae2ddc1b31e`.
- Pre-run freeze SHA256:
  `98a14be0ce185e32cec8a95bcb2b0dc817a6ccf5cb67b662842034dc15b10b19`.
- Original output SHA256:
  `e4651b1655b1c55c1d087d62680d5819972f6caea7ca07d6cb31b193879ea517`.
- Actual Pascal output SHA256:
  `12c00b01d828deb80b0ba01a199aa932b228102548b4bf3dd30664c8a1bf07b5`.

The new read-only `engine.model_training --target liero --readiness` command
finds **zero marked-verified Pascal pairs,81 legacy-unverified C pairs**.
The27 reviewed source recoveries are not automatically corpus entries.
Current knowledge labels do not bind review/whole-path completeness by
themselves, and the trainer's loss-improvement gate does not measure binary
recovery. No training/export/adapter activation or source promotion occurred.
Persisted assessments: session `files/liero-weight-readiness-20261103.json`,
`files/cleanup-initialization-constraints.json` and
`files/cleanup-initialization-contract-graph.json`.

**Completion gates, not another unconstrained probe sequence:**

1. For the port leaf, establish actual base/DS and read/write/busy protocol;
   preserve potentially nonreturning polling, byte argument and RET2 effects.
   The ready-only PIC projection cannot replace this full contract.
2. Then resolve reset/read and BIOS15/DOS21 effects before stop/finalizer and
   real callback reentry. Only then compose complete error/allocator paths.
   Defer callers with unresolved callees rather than installing guessed bodies.
3. Validate the actual target implementation and its shared helpers, review
   every path/ABI/memory/external obligation against original evidence, and
   bind all identities before updating the source ledger. Finite parity alone
   is insufficient. Prefer an already supported pure leaf if I/O remains
   blocked; do not make peripheral breadth a prerequisite for all source work.
4. For training, independently review prospective full-routine pairs and
   lawful known-source Pascal projects, record developer-known/manual bodies,
   deduplicate routine families, and freeze project-disjoint development and
   terminal tasks. Compare base, retrieval-only and adapted models with equal
   budgets, binary-backed recovery metrics and old-project retention.
   Loss-only or synthetic-control gains must not promote weights.

605 connected tests pass,10 historical cases excluded; the separate actual
source exhaustive test passes. Ruff/Pylance syntax checks pass. Audit remains
27/295 source,4 partial,34 host,0 full-binary,1 stale; four invalid historical
reports remain invalid. No unchanged scoped probe is counted as another
independent recovery or as gold training data.

### Real cleanup dependencies mapped; original port leaf ready path checked

The next callee-first step follows the real relative135c:1345 callback, not
the synthetic RETF callback. `tools/liero_cleanup_port_probe.py` authenticates
nine original byte regions and all overlapping MZ relocations. Signed near
displacements and relocated far operands establish these direct dependencies:

| Caller (relative segment:offset) | Byte-backed callee(s) | Scope |
| --- | --- | --- |
| 135c:1345 | 135c:045d; PUSH CS + near CALL135c:032e | Restores saved callback first; full callback still unknown |
| 135c:045d | Three call sites to135c:0000 | DS67cd selects command d5 or d0/d3; then OUT via DS67de with DS67ee |
| 135c:032e | Conditional135c:131a, then135c:0036 | DS67fa selects optional first call; second requires it to return |
| 135c:0036 | 149c:01c3 (module14b83);135c:001a | Reset path includes BIOS15/AH86 wait and device reads, not evaluated here |
| 135c:131a | 14cb:0094 (module14d44) | CLI/port operations, DOS21/AH25 vector helper, then STI; outcome not evaluated |

These are static call facts, **not normal-program reachability**. The first
leaf135c:0000 has no callees: repeatedly load DX from DS67d4, IN AL,DX, and
test bit7; only when clear does it load the low argument byte from SS:BP+4,
reload the port, OUT, restore BP and near RET2. There is no software timeout.
The receive leaf135c:001a instead waits for bit7 **set**; neither its busy
loop nor actual sound-device transitions are accepted from this review.

The write leaf's26 bytes execute unchanged at COM2000 (position-independent
short branch, no relocations), using the existing assembler/DOSBox runner.
The declared fixture owns emulated PIC mask port21, not Liero's sound device.
With interrupts disabled, it saves the mask, sets and reads back ready00/7f,
calls the original leaf, reads back its OUT result, and restores the original
mask/flags before DOS file services. No IN/OUT instruction is substituted.
Code/records end below67c0, globals67c0..6800 and stackeff0 are disjoint;
DS=SS=CS is supplied, not inferred for the real callback.

**512/512 fixed original/Pascal ready cases pass:** all256 command bytes at
each mask, with high argument bytesa5/5a. Checks include all64 global bytes,
CS/DS/SS, returnedSPeff0/BP2468, AX including preservedAH, DX21, stack guards,
declared flags (including IF0), and actual PIC readback. Undefined AF and
unclaimed flags are not promoted to an ABI guarantee. A deterministic Pascal
ready-only projection matches the three-word result for every case; busy
input is explicitly unsupported by that projection, not silently successful.

This is a fixed mechanism corpus, not training/heldout generalization, a
hardware protocol oracle, or recovered callback source. Zero model calls,
repairs, retries or source/example/weight promotion. A pre-execution assembler
range error in the harness loop was corrected before the original run; it
was not feedback from an original or heldout result.

Evidence:
[result](../build/cleanup-port/pic-ready-v1/result.json),
[freeze](../build/cleanup-port/pic-ready-v1/freeze.json),
[Pascal projection](../build/cleanup-port/pic-ready-v1/probe.pas),
[combined graph](../build/cleanup-port/pic-ready-v1/contract-graph.json).

- Freeze SHA256:
  `a032bd5debb0466876175f3c0ee5dfe30fb321a80f21e7e912bb3132d5e2878e`.
- Pascal source SHA256:
  `460c4d8ba3c93288923e981cf8e742761d8708e8a06421e633f488551cf30ec7`.
- Pascal output SHA256:
  `a6c396de2d5657b70eac808e4c31c47324190d2fe4f677a63e430a7177ed9d1f`.

All six frozen scopes replay. Combined graph16 nodes/36 facts/17 edges has
no conflicts; static direct edges remain observed, the PIC ready result
alone is scoped oracle evidence, and actual device/callback/service outcomes
remain unknown. The audit discovers this scope with `ready_only=true` and
`actual_device_verified=false`; source remains27/295,4 partial,34 host,
0 full-binary,1 stale. Four invalid historical constructor/comparator reports
remain explicitly invalid.574 connected tests pass,10 historical cases
excluded; Ruff/Pylance syntax and target proxy build pass (35 existing
warnings, unresolved residue preserved).

**Next blocking question:** establish the original sound-port initialization
and applicable device behavior before accepting busy transitions or composing
reset/read, wait/vector services and real callback reentry. The current
DOSBox runner disables Sound Blaster emulation; PIC roundtrips cannot supply
that missing protocol. Keep installer DS/lifetime, actual failure reachability
and018b cleanup unresolved. Do not extrapolate the ready projection to them.

### Cleanup dispatch/reentry mechanism checked; real target identified

`tools/liero_cleanup_dispatch_probe.py` authenticates the29 original bytes
016e..018a with no overlapping MZ relocation. It runs that original dispatch
in a controlled64KiB COM and stops018b before real cleanup. Eight fixed cases
use two dirty-memory seeds and four callback-pointer modes: null, same-CS,
nonzero-segment/zero-offset, and a second far alias of the same owned target.
The synthetic target records its entry and executes RETF without installing
another callback. It is explicitly not a recovered real callback.

All8 original cases and the deterministic Pascal dispatch-state projection
pass. Each endpoint checks all58 global bytes, CS/DS/SS/SP, and the callback's
actual return words. Results establish, under the fixture premises:

- Null requires both pointer words zero; offset0 with a nonzero segment
  invokes the owned synthetic target rather than silently skipping.
- DS6402/6404/6410 are cleared **before** the transfer. Other captured globals
  remain dirty and unchanged. Null dispatch does not clear6410.
- PUSH CS/016e/ES/BX and original RETF leave returnIP016e and callerCS at
  callback entry with SPefec. Synthetic RETF returns to016e with SPeff0.
- Reentry reads the now-empty slot and selects018b; guard words above the
  entry stack remain1357/2468. The callback's DS-relative recorder supports
  all three far aliases without assuming callbackCS equals dataCS.

This is one frozen mechanism corpus, **not training/heldout generalization**.
Zero model calls/repairs; no callback-body or whole-handler acceptance.
The snapshot recorder is instrumentation that clobbers scratch registers;
only declared state/memory/stack fields are compared, not full ABI.
Code/records/owned callback remain below6000; globals63d8..6412 and stackeff0
are disjoint. Real callback mutation/reinstallation/nonreturn and arbitrary
DS/stack behavior remain unknown.

Source/method/harness/COM/trace/Pascal replay passes, including rehashed tamper
rejection and false-real-callback-promotion rejection.
Evidence:
[result](../build/cleanup-dispatch/mechanism-v1/result.json),
[freeze](../build/cleanup-dispatch/mechanism-v1/freeze.json),
[Pascal projection](../build/cleanup-dispatch/mechanism-v1/probe.pas) and
[combined graph](../build/cleanup-dispatch/mechanism-v1/contract-graph.json).

- Freeze SHA256:
  `bece4a83f86b41df9915ad0e4e1c7d1f1f1163fefc9d8b9e2d6963bae336325c`.
- Pascal source SHA256:
  `28a4b35f61a5dc9e03b6dfb07058803a6ef45ec302a514e4641f1849704d756f`.
- Pascal output SHA256:
  `31aec1fe6798b998f86d8c0f5af48e51e2dc866bc79fdff1ec1970944efe1324`.

The existing graph/audit label the8-case result as a synthetic callback
mechanism, explicitly `actual_callback_recovered=false`. Exact original
write-site review additionally establishes a **concrete next target**:
module138c8's prefix saves6402/6404 into67f6/67f8 and installs relative
135c:1345 (ordinary segment:offset notation), using an actual segment relocation.
Module14905, the same target, begins by restoring67f6/67f8 into6402/6404,
before two unresolved calls. No complete writer inventory, entryDS provenance,
installation lifetime, reentry behavior or callback acceptance is inferred.
The earlier real64000 caller snapshots already have null6402/6404/6410 at
both captured endpoints; this replayed fact does not prove a future failure
will encounter a null slot.

All five frozen scopes replay; combined graph7 nodes/21 facts/6 edges has no
conflicts.545 connected tests pass,10 historical original/frozen cases excluded;
actual target proxy build passes with35 existing warnings and original residue.
No source/ledger/example/weight promotion:27/295 source remains.
The refreshed recovery audit also retains four invalid historical
constructor/comparator reports (stale evidence or an unrecognized old
contract), plus one stale source recovery; this milestone does not repair
or count them as current acceptance evidence.

Requested web research identified upstream REA and Craft Anything; primary
source review and pinned links are in
[the recovery method](../../../docs/RECOVERY_METHOD.md#requested-rea--craft-anything-comparison).
Useful evidence/unknown/feedback patterns reinforce our existing design.
Their feature-recreation workflows are not our recovery objective; neither
was installed or evaluated against Liero, and no code/binaries were uploaded.

**Next exact dependency:** review the real135c:1345 callback's direct callees
before accepting its restore/cleanup/reentry contract, and establish actual
installer DS/lifetime. Null018b cleanup still calls unresolved routines and
services. Do not promote synthetic RETF behavior to those targets.

Earlier checkpoints retain their own historical next-work gates below.

### Error-address translation checked before cleanup

The next error-path dependency is now a scoped original/Pascal comparison.
`tools/liero_error_address_probe.py` authenticates all84 original bytes at
011a..016d and the single actual MZ relocation at011b. Execution stops at016e,
before LES BX,[6402], cleanup dispatch or any subsequent service. The entry
errorAX is203; this experiment does **not** execute an actual allocator failure
or010f's caller-stack pops.

Byte-derived behavior and Pascal review:

- Nonzero CX/BX scans the descriptor segment chain rooted in DS63e4.
  Descriptor +8 is an exclusive offset limit, +16 its base paragraph,
  +20 the next segment. These are descriptive field names, not recovered types.
- Zero descriptor base, base above caller segment, paragraph difference>=4096,
  offset addition carry, and computed offset>=limit all reject that descriptor.
  SUB/JA/NEG and unsigned CMP/JB semantics matter at equality boundaries.
- First match selects computed offset and descriptor segment; a null chain
  retains the caller offset/segment. The selected segment is normalized by
  subtracting savedPSP and16 modulo65536.
- An initially zero CX/BX pair bypasses both traversal and normalization.
  Error203 goes to DS6406, translated offset/segment to DS6408/640a.
  The Pascal model implements precisely these conditional result effects,
  not a native pointer traversal or complete error handler.

One deterministic candidate passes **61/61 training and37/37 terminal cases**.
One terminal evaluation, zero model calls, repairs or retries. Corpora were
fixed before execution and have disjoint caller-offset/topology tuples.
Inputs exercise zero/one/two-node chains, first/second match and fallback,
zero/above/equal base,4095/4096 paragraph boundaries, strict size equality
and addition carry. This is a known-slice mechanism, not unseen-routine
generalization, an automatic recovery-yield success or weight improvement.
Finite cases do not promote the entire routine.

The controlled COM fixture owns descriptors in [8000,8200), with at most
two acyclic segment nodes CS+0800/0810. Code/capture stays below6000;
globals[63d8,6412), descriptor window and stackeff0 are disjoint in a checked
64KiB allocation. Only the original source-DS relocation word is mapped to
COM CS at runtime; original STI remains. SavedPSP is supplied as CS-16.
No actual63e4 provenance or arbitrary chain validity is inferred. Every case
checks all512 descriptor bytes unchanged and all58 global bytes against
exactly the three permitted word stores. DS, SP and IF are checked; other
register/flag outputs remain outside the parity claim. Sixteen-case internal
batches keep586-byte records below globals. Descriptor contents are supplied
fixtures, not observations of the real-program error handler.

Evidence:
[result](../build/error-address/owned-descriptors-v1/result.json),
[freeze](../build/error-address/owned-descriptors-v1/freeze.json),
[Pascal model](../build/error-address/owned-descriptors-v1/candidate.inc) and
[combined graph](../build/error-address/owned-descriptors-v1/contract-graph.json).
Exact source/corpus/method/COM/trace/output replay passes without another
execution; rehashed descriptor/output/source/image/method mutations, missing
hashes, path escape and false source promotion are rejected.

- Candidate SHA256:
  `c0d48ff0279bf2aa176e3430177c30173e06024988acad6eaa3ff7bcdff8fb06`.
- Freeze SHA256:
  `9c03e57c784c3e6ba9a984ad663cd72e30a750a2a775f445508c8b52d01dece6`.
- Pascal training/terminal SHA256:
  `a6c513eb7f2d12e6575278a1c9d1f1b868f40d9f29a79b44723c69fd52bb7daf` /
  `7f20829ecc9e469777f839d0ae4353ccebfd374a169fac76bdba6a5e99f0f502`.

The existing conditional graph/audit now discover this98-case translation
scope separately. Actual descriptor provenance, arbitrary topology and cleanup
callbacks/services remain unknown; whole010f/0116/028a acceptance is blocked.
All earlier allocator freezes still replay.521 connected regressions pass,
10 historical original/frozen cases excluded; Ruff/Pylance syntax checks pass.
The actual target still compiles into isolated writable output with35 existing
warnings and original unresolved residue. Source/ledger/example/weights remain
unchanged:27/295 source,4 partial,34 host,0 full-binary,1 stale.

**Next blocking question:** the contract of016e..018a's DS6402 cleanup callback
dispatch/reentry and its actual target provenance, followed callee-first by
the invoked cleanup routines. Do not equate this address-translation pass with
failure-path termination, callback safety or later caller-buffer lifetime.

Earlier checkpoints retain their own historical next-work gates below.

### Actual64000-byte caller context measured, not merely supplied

The next dependency now has a measured original-program call point.
`tools/liero_allocator_entry_probe.py` executes original startup and main
through the actual `e50e` relocated far call to `028a`, stopping after its
original `e513/e516` result stores and before the next allocation. It does
not replace the allocator, supply heap pointers, clear globals, mock services
or install another callback. One frozen original execution and one execution
of the **unchanged previously checked Pascal source** pass; zero model calls,
repairs, retries or heldout evaluations. This observed input is not a new
training/terminal corpus or evidence of model generalization.

The endpoint records establish, in this instrumented DOSBox context:

Far-pointer pairs below are written offset:segment, matching the AX/DX and
captured global-word order, not the usual disassembler segment:offset notation.

- Actual load segment01a1; DS1b12 and SS22c8.
- Entry far-return IP/CS `e513:01a1`, request64000 on the real stack.
- Empty head/frontier `0000:32c7`, limit `0000:9fff`, default callback
  `00d6:167e`; these were read at entry, not inferred from startup alone.
- Original result and `6684/6686` store `0000:32c7`; frontier/head advance
  to `0000:4267`, carry clear, BP preserved, SPffc8->ffce.
- Allocation physical interval `[207984,271984)` is64000 bytes, begins at
  the guaranteed original allocation's heap boundary, and stays below PSP:2.
- All6010 bytes of DS[63d8,7b52) agree with the predicted seven word stores
  (frontier/head, result pointer and saved request); every other captured
  global byte stays unchanged. Actual Pascal produces the same eight-word
  result/state projection on the observed absolute segment values.

Instrumentation is explicit: MZ entry redirects to appended bootstrap;
028a's three-byte prologue becomes a same-CS gateway, which preserves
registers/flags and executes the displaced PUSH BP/MOV BP,SP before028d.
Only the selected returnIP/mainCS is captured; other028a calls pass through.
The actual e50e CALL, its real far-return contents and both original stores
remain intact. At e51a, three NOPs replace the next PUSH and the following
CALL becomes a far JMP, reusing its **unchanged original segment relocation**.
No new relocation or altered service instruction is introduced. MZ allocation
size remains unchanged; payload is below the last4096 guaranteed stack bytes.
Bootstrap/dispatch/snapshot scratch is10/6/14 bytes respectively. Observed
stack bounds, DS provenance and payload/global/heap separation are checked.
Collector DOS writes occur only after both snapshots. Guest termination is
instrumented, not the original program's cleanup path.

Evidence:
[result](../build/allocator-entry/actual-64000-v1/result.json),
[freeze](../build/allocator-entry/actual-64000-v1/freeze.json),
[patch inventory](../build/allocator-entry/actual-64000-v1/patches.json) and
[combined graph](../build/allocator-entry/actual-64000-v1/contract-graph.json).
Source/method/image/trace/Pascal replay passes without another execution.

- Freeze SHA256:
  `a0b59b9d85311fe9dc39cec47295c891a079830e9be924d139ac8e6b6c91c8e2`.
- Original trace SHA256:
  `61b8ad008686375fed7907834a98eaf2a2e3adf530a063da6026668fc4c3e0b6`.
- Pascal source SHA256, identical to the earlier empty-list candidate:
  `807c2b7b0088ccd5a082668e1a1101be505cf421cdd397100ba753aeac591af6`.
- Pascal output SHA256:
  `18f004b94deecd23ea2d0a7969dcceb84a5e36a2a3f0b6ffc57bbe7961ad4f7d`.

The existing graph now records the applicable **observed** empty-list context
and allocation origin at e51a separately from universal caller applicability.
Later pointer lifetime/aliasing stays unknown; this does not unlock94c5,
certify all64000 buffer bytes, resolve arbitrary lists/nondefault callbacks,
or accept an entire routine/ABI. The audit discovers this one real-context
comparison separately from the112/120-case synthetic allocator fixtures.
All three freezes replay;494 connected tests pass,10 historical original/frozen
cases excluded. No target source, ledger, examples or model weights changed.
Audit stays27/295 source,4 partial,34 host,0 full-binary,1 stale.
Isolated target FPC proxy compilation passes with35 existing warnings;
Ruff formatting/lint and Pylance syntax checks pass.

**Callee-first error-path review also corrected an assumption:** original
010f bytes `59 5b eb 07` pop returnIP into CX and returnCS into BX and jump
to **011a**, not0116. Therefore0116's XOR CX/CX and XOR BX/BX are bypassed.
At011a, the actual MZ relocation and `8e da` establish MOV DX,relocated1971;
MOV DS,DX, not the exported listing's reversed MOV DX,DS. The prefix enables
interrupts, stores entryAX (028a supplies203) at DS6406, and tests CX/BX.
The same byte review confirms0130 `8e c0` is MOV ES,AX, not MOV AX,ES.
Both listing directions are corrected; the routine remains unreviewed.
This is static byte/relocation evidence, not execution of an allocation
failure. The graph records it separately. The following63e4-dependent ES
traversal, cleanup callbacks and external-service/nonreturn contract remain
the next error-path dependency; success does not resolve them.

Earlier checkpoints retain their own historical next-work gates below.

### Continued allocator recovery: bounded nonempty-list projection passes

The next dependency was investigated rather than treated as a reason to stop.
`tools/liero_allocator_list_probe.py` now reuses the existing COM assembler,
DOSBox runner, original allocator/helper bytes and default callback. Exact
short-branch decoding establishes 0371->03d2, 0377->0364, 0379->0381,
037f->0364 and 038c->03c1; exported listing addresses were not substituted
for instruction facts. Node words are next offset/segment at +0/+2 and
size offset/paragraphs at +4/+6. First-fit traversal remembers the predecessor
link cell; exact fit unlinks, while splitting writes the remainder header
after the rounded allocation. These are byte-derived semantics with
descriptive names, not recovered historical spelling.

The declared fixture owns [8000,8200), contains one or two acyclic nodes
at 8000/8100 plus offset0 or8, with eight-byte-aligned sizes8..128.
DS=SS=CS, stackeff0, code/records below6000, disjoint globals and frontier9000,
64KiB COM allocation, nonwrapping relative segments and the default callback
are required. The fixture does not establish those premises at a real caller.
Every accessed/split header fits in the owned window. Records are584 bytes:
result/state16, protected-global snapshot56, heap512. The comparison checks
all256 heap words plus result, head, frontier, saved request and carry;
original global residue and callback/limit cells are also checked.

One deterministic candidate passed **72/72 training and48/48 terminal cases**.
The suites use disjoint request values; one candidate, zero model calls/repairs,
one terminal evaluation. This is a developer-known-slice mechanism, not
automatic recovery yield or learned generalization. Original runs are
internally batched16 at a time: a single72-case capture would overlap global
data, so memory budgeting is enforced before assembly, not fixed after seeing
terminal results. Partial traces fail closed. Runtime errors, mismatches and
premise drift stop without retry; terminal drift is checked after execution too.

Evidence:
[frozen report](../build/allocator-list/owned-two-node-v1/result.json),
[freeze](../build/allocator-list/owned-two-node-v1/freeze.json),
[Pascal model](../build/allocator-list/owned-two-node-v1/candidate.inc) and
[combined conditional graph](../build/allocator-list/owned-two-node-v1/contract-graph.json).
Ignored build artifacts retain each batch's cases, original COM image,
assembly, complete trace, method snapshots, compiler/runtime logs and outputs.
Source/method/case/image/full-heap replay passes without another evaluation.
Tamper tests also reject rehashed changes to saved COM, Pascal, heap output
and method snapshots, missing required hashes and escaping paths.

- Candidate SHA256:
  `9a070fb56971267bdf2866706e08f0e576595a2846235361ae4f7d40ae62fbd1`.
- Freeze SHA256:
  `7f72d1cfcd46c8e0cea437ebffc27cd52b5ad9b2952e87a676a591a089bfefe2`.
- Pascal training/terminal SHA256:
  `139418af60a65ad6f5df454fd2be0573e2c018a5f99a706b8b9ff910ad738c6f` /
  `eab5cfe1939212bbf1be78b1a06dc18f5968c9db07ea914d5ff7b674cba3c6ba`.

The existing audit discovers this120-case scoped check separately. The existing
allocator graph additionally incorporates the owned-list conditional fact and
actual028a call edge, leaving arbitrary topology, callbacks and caller
applicability unknown. This does not resolve the full remaining-paths piece
or propagate a successful allocation into caller globals. Earlier empty-list
source/method freeze still replays unchanged; no shared frozen method was edited.
451 connected tests pass,10 historical original/frozen cases excluded.
Focused Ruff checks pass; isolated target FPC proxy compilation passes with35
existing warnings and unchanged assembly residue. Source counts remain27/295,
4 partial,34 host,0 full-binary,1 stale; no source/ledger/example/weight promotion.

**Next blocking question:** which allocator list/callback premises actually
hold at028a entry, and can original writes/handler targets and lifetimes
justify them? The bounded one/two-node result does not license arbitrary
dynamic ES:DI writes. Preserve nondefault-callback effects/retry, arbitrary
topology/aliasing,010f error-transfer and full ABI obligations. No further
terminal evaluation of this selected candidate is allowed.

The earlier empty-list tranche below retains its historical next-work context;
its nonempty-list gate is now partially discharged only for the fixture above.

### Research-roadmap tranche: deterministic allocator projection passes

The changed strategy now deduces the known empty-list/default-callback slice
instead of requesting another full procedure from the model. The exact
203 allocator, 17 helper and 5 callback bytes are recognized by
`engine.instruction_facts.allocator_empty_list_contract`, after validating
the original binary identity and actual MZ relocation exclusions.
The obligations retain zero-request no-write behavior, actual saved request,
eight-byte rounding, paragraph/offset arithmetic, segment-first limits,
old-pointer return, frontier/head updates and failure DX/CF residue.
Unknown list/callback/entry-state/ABI paths remain explicit.

One frozen deterministic candidate compiled with FPC `-Mtp -Cr` and matched
the complete original projection on **64/64 training and 48/48 terminal
validation cases**. Both original runs completed; one terminal evaluation,
zero model requests, zero repairs. Source/hash-bound replay passes without
re-executing DOS or Pascal. This is a developer-known slice and historical
corpus, not unseen-routine generalization or an automatic model recovery.
The earlier generated candidate's runtime201 failure is preserved unchanged.

Evidence: [deduction result](../build/allocator-deduction/deductive-v1/result.json),
[scope review](../build/allocator-deduction/deductive-v1/review.json),
[obligations](../build/allocator-deduction/deductive-v1/obligations.json) and
[puzzle outcome](../build/allocator-deduction/deductive-v1/puzzle.json).
These local build artifacts are ignored by git; the measured outcome and
identities are preserved here:

- Candidate SHA256:
  `807c2b7b0088ccd5a082668e1a1101be505cf421cdd397100ba753aeac591af6`.
- Freeze SHA256:
  `0864d055a3d962c249c811be63a2063e9b447612eb1901230fac2f8b300cad8c`.
- Original training/terminal trace SHA256:
  `18337a54e73c94b846fafb78799a47f86e08eb2462809432e51fbff80be059fa` /
  `526cc953bb0fee0438905f0105d4554279b33f5cc7ae91d0f8c67a2b8aad3527`.
- Pascal training/terminal output SHA256:
  `a48c5e3815ec926408044e846b2aebed791a10ece7bf156609edd620c13671e6` /
  `790dffc6c6b34e9a54d8b259c9c10a827c269841c65e422622234a3ebe7c9967`.

The existing puzzle scheduler now checks/revalidates this piece, removes
only its empty-list-result prerequisite, and retains two blocked frontier
pieces. The fact graph binds the actual 028a:0290 call to the conditional
0353 result but leaves caller applicability **unknown**; it does not propagate
a successful allocation into 6684/6686. Caller failure also transfers to
unreviewed010f, an additional error-path/far-call ABI obligation.
Scoped instruction context reaches the caller prompt separately from the
full unresolved allocator contract.

No candidate was installed into `src/FUN_24dd_0353.inc`; the existing
no-argument skeleton does not establish a safe register-return/partial-path
integration. No recovery attestation, example or weights changed.
Audit remains27/295 source,4 partial,34 host,0 full-binary,1 stale.
The audit additionally discovers this112-case scoped report, not a whole
routine pass.424 connected tests pass,10 historical original/frozen cases
excluded rather than rerun. Focused Ruff checks/format pass. Actual target
source compiles with its existing residue and35 warnings into a writable
session output directory; the first attempt could not overwrite the protected
legacy build/liero.o. No permissions or legacy objects were changed.

**Supporting runtime research:** inspected
[DCC's Pascal collector](https://github.com/nemerle/dcc/blob/qt5/tools/makedsig/TPL_PatternCollector.cpp),
[signature files](https://github.com/nemerle/dcc/tree/qt5/sigs) and
[wildcard logic](https://github.com/nemerle/dcc/blob/qt5/src/fixwild.cpp).
The collector explicitly handles TP4/TP5, warns that system-unit names are
not reliably linked to routines, and the tree contains t3/t4/t5 signatures,
not a validated TP7 set. Matching uses a short wildcard-normalized prefix,
not complete semantics or actual-MZ-relocation validation.
Repository source is GPL-2.0; this is not independent permission to reuse
compiler libraries or signature-derived third-party material. The configured
path exposes FPC, not `tpc`; no claim is made about arbitrary private media.
The bounded0000/00d6/028a/0353/04dc comparison was deferred before matching
because no applicable lawful TP7 reference was established. This is **not**
five negative signature matches. No matcher, library database or compiler
download was added; recovery did not wait for them.

**Next gate:**0353 nonempty-list layout/ownership and nondefault-callback
effects/retry contracts, callee-first. The current empty-list runner does
not certify node accesses through dynamic ES:DI. Establish a declared,
bounded nonempty-list context and callback target contracts before expanding
that frontier. Actual first-allocation DS/list/limit/handler lifetime and
010f still block028a acceptance. Do not retry terminal validation, count
known-body rendering as automatic yield, train weights, or resume per-vector
startup milestones. See the [research-informed method](../../../docs/RECOVERY_METHOD.md#external-prior-art-and-deterministic-first-recovery).

### 2026-11-02: corrected-schema allocator candidate reaches training and fails

The corrected declaration schema produced one complete0353 Pascal proposal
with local `qwen2.5-coder:14b-instruct-q4_K_M`. The exact generated include
compiled with FPC-Mtp-Cr and executed against the frozen64-case training
suite; no repairs or retries. Original allocator/helper/default callback
execution completed all64 controlled cases. Candidate execution failed
runtime201 at case60 (request65535/startOffset8). The candidate attempts
to assign65543 to a Word. Its partial output contains60 complete records:
eight zero-request matches,52 mismatches. **This is not a training pass
or a 64-case success-rate estimate.** Cases60..63 have no complete candidate
record. The heldout gate remained closed: neither original nor candidate
heldout suite executed.

Review against authenticated original bytes rejects the proposal:

- Original0357 stores the request inDS7b3c; candidate writes constanta5a5.
- Original035a calls resolved rounding04dc; candidate adds raw request bytes.
- Original03dd..03e9 compares segment then offset; candidate ignores the
  segment limit and rejects even equal offsets with spare paragraphs.
- Original03f1..0409 advances frontier/head and returns the old pointer;
  candidate leaves the frontier unchanged and computes a different result.
- Original default failure leaves computedDX and returnsAX0/CF1; candidate
  failure returns initialized or partially computed fields instead.

First counterexample (case8): input request1/start0:0800/limit0:0800.
Original result0:0800/CF1, saved request1; Pascal result0:0000/failed,
saved requesta5a5. Case10 has ample capacity (limit0:1800): original succeeds
with result0:0800/new frontier8:0800, candidate incorrectly fails.
The eight matching zero-request cases do not recover the routine.

Source is **not installed or promoted**;0353 remains unreviewed and the
audit remains27/295 source,4 partial,34 host,0 full-binary,1 stale.
No model improvement, example promotion, unseen-routine generalization or
normal-program allocator acceptance. Added an injected runtime201 regression
to ensure partial output is preserved but cannot enter heldout or become a
scored pass.15 focused allocator tests pass; the original-only control is
excluded rather than rerun. Earlier880 connected regressions remain historical.

Frozen session evidence: `files/allocator-corrected-schema-20261102/`
contains candidate/raw response, prompt/schema/method snapshots, original
and Pascal training outputs, compile/runtime logs, result and `review.json`.
CandidateSHA2a0a7c04c1f87fa805f271e2b2605e5ad8edb5d9e2020a074e9e7c8564905b33;
freezeSHAcff0b2b5a8c16e2760c48310e2ed42436d2df44799ae207c5e88568d8ca37be5.
Inspection of saved output is diagnosis of that same failed execution,
not independent evidence or a new candidate run.

Stop expansion at0/1 candidate yield. The next strategy must address
rounding/frontier/limit/saved-request constraints using training evidence,
with a new explicit freeze; do not retry heldout, repair this frozen
candidate in place or return to individual startup interrupt milestones.
Nonempty-list and nondefault-callback paths remain unresolved.

### 2026-11-02: batched startup checks and bounded allocator experiment

**This supersedes individual-query next steps below.** The existing
startup observer now offers `--vector-batch`: one original instrumented
run checks all19 queries and saves, stopping0064 before handler installation.
Only CLD/CS:LODSB is displaced unchanged; original AH35/INT21, pointer
stores and ADD/LOOP remain in place. Before/after snapshots check selected
IVT entries, PSP:2 and DS[63d8,7b52). All76 saved bytes match pre-loop IVT,
other5934 bytes unchanged; exitCX0/SI024c/DI7b3c and tracked DS/SS/SP
checked. Exact12238 bytes. No individual-service preservation, universal
ABI, transient/other-memory/code/table/live-return integrity or
allocator-entry lifetime follows from endpoint equality.

Batch traceSHA81e64c00e4f3c466464262a253517e56fcf666c958365ec3603f95ae89ce102c;
imageSHAc28a6fab1767b83860c65dd38bdc9c7420829b734e08bb9b715849b7343a8cd1;
freezeSHA388d8b481575c6a5ae3dad75bc8f6e7802fc5fde88d69ce27cc5e3d0be5a1dc4.
Existing0353 contract/prompt receives scoped batch evidence and routing.

The existing pilot adds `--allocator-trial`, isolating0353 zero request,
empty-free-list frontier growth and default-callback failure. It executes
the original203 allocator bytes, actual17-byte rounding helper04dc and
authenticated default callback00d6 in a controlled COM layout. DS=SS=CS,
64KiB allocation checked, SP=eff0; code, globals, records and heap guards
are disjoint. Callback bytes occupy disclosed PSP command-tail scratch
d6..da. The Pascal interface projects AX/DX/CF, saved request and frontier/
head; segment values are explicitly CS-relative. Unrelated globals and
128 heap guard bytes are original-only checks, not whole-memory Pascal parity.
No later startup service assumptions are necessary for this controlled test.
Real allocator-entry heap/list/callback provenance/lifetime remains unresolved.

Frozen budget: one proposal, zero semantic repairs,64 training cases,
at most one48-case heldout. Selection uses training only; drift checks
precede each suite. Partial passes cannot automatically install source,
promote examples or attest the entire allocator. Developer-supplied topology
and a manually known preflight body are disclosed; not blind generalization.

The known four-case preflight passes original versus actual Pascal.
Its first failure corrected a bad assumption: failure returnsAX0/CF1
with computedDX intact, notDX0. This is a control, never a model recovery.
The live model returned only `{"source":"pascal"}`; declaration rejection
prevented compilation and all binary/heldout evaluation. A separately
frozen declaration-constrained format attempt, linked to the prior failure,
hit HTTP400 because the backend requires both regex anchors. No generation
or heldout occurred. The schema was corrected and accepted in a one-token
compatibility diagnostic; no further recovery attempt was made. Both
failed freezes remain intact, including their earlier rule snapshots.

Review verdict: **no acceptable generated Pascal; no routine promotion**.
Nonempty-list traversal/exact-fit/split, nondefault callback/retry, full ABI
and normal-program state remain explicit obligations. Next work must fix
proposal quality and exercise this bounded allocator experiment, not return
to per-interrupt milestones.880 connected regressions pass (8 original/
frozen tests excluded); audit unchanged27/295 source,4 partial,34 host,
0 full-binary,1 stale. No weight-learning or real-project improvement claim.

Session evidence: `files/startup-vector-batch-original-20261102/`,
`allocator-empty-frozen-20261102/`, `allocator-empty-format-frozen-20261102/`;
controlled preflights and `allocator-refocus-final-20261102/` are separate.

### 2026-11-02: third AH35/AL1b observed, stop before third save

The existing observer adds `--third`, mutually exclusive with `--second`
and `--bridge`. First two original calls and displaced pointer saves set
up the third call; only its pre/post endpoints are measured. Original
AH35/INT21 and ADD/LOOP remain in place. Same-CS prefix/stores and
flags-restoring dispatch are disclosed; not an unmodified normal run.
Independent assembly decoding checked CX17 selection and IVT1B capture.

One frozen case passed once: third ES:BX=F000:1060 matches pre-call
IVT1B. DS/SI/DI/CX/SS/SP, PSP:2 and IVT0/2/1b/21 are unchanged.
All6010 protected bytesDS[63d8,7b52) are unchanged, including both saved
slots (eight bytes); clear/heap/class/callback baselines checked.
Exact12110-byte trace stops third005a before stores/remaining16 queries.
This proves neither universal service ABI nor transient/other-memory,
code/table/live-return integrity, handler stack/bytes, Pascal parity,
allocator lifetime/success, source acceptance or model improvement.

Corrected preflight:553 tests pass. Initial preflight552 pass/one failure
caught an unintended older-second dispatch change; it was restored before
original evaluation, and both preflights remain preserved. Final703
connected regressions pass, six frozen cases excluded. Source audit
unchanged27/295,4 partial,34 host,0 full original-binary,1 stale.
The existing allocator drafting context carries the scoped fact and hashes.
No Pascal/ledger/promotion/model changes.

Frozen session evidence: `files/liero-dos35-third-original-20261102/`,
case `test_instrumented_third_servic0/third/`.
TraceSHA f9bc1f261a6ca58b9b22efac4fc98469d63dc97a6f6c7b4c9436e06a01bd0260;
imageSHA 82094fb7611cb97e9c4d187ee7fc49b5f71546ffeb4c8dd53a6dc95096928cc9;
freezeSHA 9d42269c5f4bf9261e851e28152aa1b3d5db073d2664ac9296ba0f58b3d34870.
Next bounded gate: third pointer-save/fourth-input bridge, expect
AL21/CX16/SI023d/DI7afc, stop before fourth MOV AH35/INT21.

### 2026-11-02: second pointer save reaches third input, before AL1b service

The existing observer now accepts **`--bridge --second`** for the second
returned-state/third-input bridge. This previously rejected combination is
an intentional new mode; first service, first bridge and second service
modes keep their meanings. No new framework or wider evaluation budget.
One distinct frozen case uses the first two calls as setup, snapshots the
second returned state at005a, saves that pointer and snapshots the third
input before0056. Neither third MOV AH35 nor third INT21 executes.

Authenticated original stores005a..005e execute unchanged in a same-CS
gateway on both iterations; original ADD005f/LOOP0062 remain in place.
The existing displaced CLD/CS:LODSB loads the next table byte1b. Query
dispatch comparesCX17, return dispatchCX18; PUSHF/POPF restore flags on
every path. Independent GNU objdump decoding before evaluation confirms
the second-return snapshot, shared store path and third-input exit.
Bootstrap4/snapshot14/dispatch2 scratch bytes remain within checked
allocation and disjoint from tracked code/data/payload; handler stack,
live-return contents and unobserved/transient memory remain unproved.

| Observed transition | Result |
| --- | --- |
| Second returned ES:BX | 0070:0008, matching recorded IVT2 |
| Second slot DS7af4..7af7 | `08 00 70 00` (offset then segment), not dereferenced |
| First slot DS7af0..7af3 | `60 10 00 f0`, intact |
| Protected DS[63d8,7b52) | 6010 bytes checked: four predicted second-slot bytes, other6006 unchanged |
| Third input AX / CX / SI / DI | 351b /17 /023c /7af8, DF0 |
| DS / SS / SP | 1b12 /22c8 /ffec, unchanged |
| PSP:2 / IVT0 / IVT2 / IVT21 | Unchanged |

ADD7af4+4 sets CF/PF/AF/ZF/SF/OF0; CLD clearsDF. Remaining flags and
recorded registers are checked. Synthetic fixtures allow returnedAXabcd
and incomingDF1: the service need not preserve AX or DF. Next LODSB
replacesAL with1b; only the next original MOV would establishAH35.
Before snapshot is post-second-service, not its input; this case is not
another second-service pre/post verification or independent evidence for
the entire loop. Universal service, Pascal/source and allocator gates stay
unchanged. No third-service effects, whole-loop or later lifetime claim.

Before evaluation488 startup/probe tests passed, followed by113 focused
bridge/boundary/failure checks. One frozen original bridge case passed
once, with no retry. Final **638 connected regressions pass**, with all
five frozen observations excluded. Earlier trace replay is integrity
validation only. Ruff/format/Pylance syntax checks pass. Existing engine
allocator context carries explicitly startup-only facts and hashes.
Audit stays27/295 source,4 partial,34 host,0 full original-binary,1 stale;
no Pascal, ledger, example promotion, model request or learning claim.

Session `files/liero-second-bridge-original-20261102/` preserves
`test_instrumented_second_vecto0/second-bridge/` with frozen methods,
trace/image, patches, symbols, build/worker logs and results. Preflight
reports: `liero-second-bridge-preflight-20261102/` and
`liero-second-bridge-freeze-preflight-20261102/`; final regressions:
`liero-second-bridge-final-20261102/`.

- Trace SHA256: `fc19e4b56cadfb9db8a79f4cfe0ccbaee79898a6705c84a6a8c6f8e763599e5d`
- Instrumented SHA256: `3a481a4f31924fd8e4b64265590a126b7aef4f35b3cc0c8ba1cf01ffd1795969`
- Freeze SHA256: `dfb91db2990a20fa2fab0825a0c77ff30a1fb96094a8c80af78c3ff3ac6d9a72`

Next exact gate: thirdAH35/AL1b pre/post effects with both saved slots
intact, stop before its stores. AL0/AL2 finite observations do not establish
AL1b or the remaining17 services, installation or allocator-entry lifetime.

### 2026-11-02: second AH35/AL2 return measured with first saved slot intact

Extended the **existing** startup observer with `--second`, implying
original-only service mode. One distinct frozen case executes the first
AH35/AL0 call and its pointer save to establish the second-call context.
Snapshots enclose **only the second AH35/AL2 call**: before its unchanged
MOV AH,35 at0056 and after unchanged INT21 at0058 returns005a. Stops before
the second pointer stores and all remaining17 queries.

The original loop/table and actual MZ relocation exclusions remain bound
by the existing contract. First pointer stores and CLD/CS:LODSB execute
unchanged in same-CS gateways; original ADD/LOOP and AH35/INT21 bytes
remain intact. Both CX dispatches restore flags via PUSHF/CMP/POPF.
Independent GNU objdump decoding **before evaluation** confirms the
first-return store path, second-return output path, snapshot restoration
and IVT2 reads at physical8..11. Bootstrap uses4 scratch stack bytes,
snapshot14, dispatch2; tracked data/code/payload bounds remain disjoint.
Handler-internal stack and live-return contents remain unobserved.

Record layout adds IVT2 offset/segment to each existing17-word snapshot:
initial3 words + two19-word snapshots + two6010-byte windows =
**12102 bytes**. Older12094-byte first-service/bridge traces are rejected
as second-service evidence, not silently reinterpreted.

| Observed state | Value / result |
| --- | --- |
| Second input before MOV AH,35 | AX3502, CX18, SI023b, DI7af4, DF0 |
| First saved pointer DS7af0..7af3 | `60 10 00 f0`, unchanged |
| Pre-call IVT2 / returned ES:BX | **0070:0008 /0070:0008** |
| Required DS / SS / SP | 1b12 /22c8 /ffec, unchanged |
| Required CX / SI / DI | 18 /023b /7af4, unchanged |
| PSP:2 / IVT0 / IVT2 / IVT21 | Unchanged; IVT21 F000:14a0 |
| Protected DS[63d8,7b52) | All **6010 bytes** unchanged, including first slot |

BeforeAL2 is required; beforeAH35 happens to be observed but is **not**
assumed preserved from the first service. The original MOV AH,35
establishesAX3502 at the actual interrupt. Synthetic checks explicitly
permit another beforeAH and changed returnedAX/DX/BP/FLAGS: this is not
an invented DOS residue ABI or a DF-preservation promise.
The first saved pointer must match recorded IVT0, with the remaining
cleared range zero and initialized heap/callback/class cells checked.
ResultES:BX must match **pre-call IVT2**, not IVT0; neither pointer is
dereferenced or proved callable.

Before evaluation **435 startup/probe tests passed**, including injected
worker failure/no retry, distinct-vector fixtures, invalid-but-unchanged
memory, first-slot boundaries, result/register/IVT mutants and exact shape.
The single new original case passed once. Final **585 connected regressions
pass**, with all four frozen heap/service/bridge/second-service observations
excluded. Existing clear-case execution tests are replays, not independent
new acceptance. Ruff/format/Pylance syntax checks pass; all10 runner and15
comparator call sites are signature-compatible. The existing allocator
prompt now includes these explicitly **startup-only** finite facts/hashes.

This case repeats the first call as setup; it does not independently
measure that call's pre/post effects. Its second-call endpoint agreement
does not prove transient/other-memory writes, original code/table integrity,
handler bytes/stack, live-return contents, unmodified normal execution,
all19 calls or allocator-entry lifetime. No second pointer save, vector
installation, Pascal parity, successful allocation, source/ledger/example
promotion, model request or learning claim. Universal service-contract
gate remainsfalse; audit stays27/295 source,4 partial,34 host,
0 full original-binary and1 prior stale.

Frozen session evidence: `files/liero-dos35-second-original-20261102/`
contains `test_instrumented_second_servi0/second/` with freeze, method
snapshots, trace, image, patch inventory, symbols and worker/build logs.
Preflight reports are in `liero-dos35-second-preflight-20261102/`;
final connected reports are in `liero-dos35-second-final-20261102/`.

- Trace SHA256: `33c058b002c24241791a66ea7a11494bcd4edd638567e288774cc422a636f23e`
- Instrumented SHA256: `582884fd54673d90f2b3f095df7cb24e6d9793263ed13b1542470100a64c74c1`
- Freeze SHA256: `0708c49bbbb13aa03402635a3400b82219d260cb3638ff6283d0888da309d8ab`

Next exact gate: carry the measured second-return premises through its
pointer save atDS7af4..7af7 and next input AL1b/CX17/SI023c/DI7af8,
stopping before the third service. Reuse this observer/checked loop,
do not infer AL1b or later-service effects from AL0/AL2 observations.

### 2026-11-02: first vector pointer save and next-query bridge measured

The existing startup observer now supports `--bridge`, implying original-only
service mode. One **distinct frozen case** executes the first AH35/AL0 call,
snapshots its returned state, executes the first pointer save and next-iteration
bridge, then snapshots the next input **before the second MOV AH,35/INT21**.
This is not a retry of the previous service experiment: its two endpoints and
acceptance question differ. The first call repeats in this context; it is not
counted as independent whole-loop or universal service evidence.

All original loop/table bytes and actual MZ relocation exclusions remain
authenticated. Original005a..005e `MOV [DI],BX; MOV [DI+2],ES` move unchanged
to the same-CS gateway (five-byte site becomes JMP plus two NOPs).
Original005f `ADD DI,4` and0062 `LOOP0053` remain in place. The existing
displaced `CLD; CS:LODSB` executes on both iterations. A disclosed
PUSHF/CMP CX,19/POPF dispatch restores flags before either path. Independent
GNU objdump decoding checked both original bytes and generated gateway
**before evaluation**, including jumps back to0056 and005f. Four-byte
bootstrap and14-byte maximum snapshot scratch remain disjoint from the
checked code/data/allocation boundaries. The dispatch's two scratch bytes
do not overlap the live far-return words, whose contents are not captured.

| Observed transition | Result |
| --- | --- |
| First returned ES:BX | F000:1060 |
| DS7af0..7af3 | Bytes `60 10 00 f0`: offset then segment, not a dereference |
| Full protected DS[63d8,7b52) | 6010 bytes checked: four predicted slot bytes, other6006 unchanged |
| Next AX / CX / SI / DI | 3502 /18 /023b /7af4 |
| DS / SS / SP | 1b12 /22c8 /ffec, unchanged |
| PSP:2 / IVT0 / IVT21 | Unchanged |
| FLAGS / next DF | Observed7202 /0; ADD-defined flags and CLD checked explicitly |

Original ADD7af0+4 sets CF/PF/AF/ZF/SF/OF all0 (low bytef4 has odd
parity), LOOP changes CX without changing flags, CLD clearsDF. Synthetic
tests explicitly allow incoming serviceDF=1: preservation is not assumed.
MOV/LODSB/LOOP do not change the remaining flags; the collector restores
its own scratch changes. ReturnedAX3500 was observed, not universally
required; the next original MOV AH,35 would establish3502 regardless of
the first result's AH. Only the next vector ID2 is accepted here, not
its service effects.

Exact12094-byte trace, one execution, no retry. Before evaluation378
startup/probe regressions passed, followed by93 focused bridge/boundary/
failure checks. Final **528 connected regressions pass**, with all three
frozen heap/service/bridge observations excluded. The new bridge execution
passed separately once. Existing clear-case execution tests are replays,
not new independent recovery evidence. Lint/format/syntax checks pass.
The allocator prompt carries these explicitly **startup-only**, finite
outputs through the existing contract renderer; no scheduler or source
acceptance gate changes.

The before endpoint is **after** the first service: this case validates its
heap/clear/register baseline but does not measure pre/post preservation
across that service. Endpoint snapshots do not establish transient writes,
unobserved memory/code/table integrity or live-return contents. No second
query, whole loop, vector installation, allocator-entry lifetime, Pascal
parity, normal-program or learned-improvement claim. Audit remains
27/295 source,4 partial,34 host,0 full original-binary,1 stale.

Frozen session evidence: `files/liero-vector-bridge-original-20261102/`
contains `test_instrumented_first_vector0/bridge/` (methods, freeze, trace,
image, patch inventory, symbols and worker/build logs). Preflight evidence
is in `liero-vector-bridge-preflight-20261102/` and
`liero-vector-bridge-frozen-preflight-20261102/`; final connected reports
are in `liero-vector-bridge-final-20261102/`.

- Trace SHA256: `69fdcc0105e4e6f66d9624494b5af5b0d9020b884dada8ded8407f48d3a4b60d`
- Instrumented SHA256: `05394b48edee391bc31160a6ed54c97325467c181aea79b7275aab19c9f55493`
- Freeze SHA256: `d0fd39c66925ee69bf169bad78f7c6d587c866381435c801cbaa57dfeb125de0`

Next exact blocker: **second AH35/AL2 service effects** with the established
first slot intact. Freeze a separate bounded pre/post case in this context
and stop before its pointer save. Do not extrapolate AL0 service results
to AL2, all19 queries, vector installation or allocator entry.

### 2026-11-02: first original AH35/AL0 call measured, stop005a

Extended the existing startup probe with `--service` (original-only heap
mode implied). One frozen DOSBox execution passed; no retry or later-loop
execution. Original `MOV AH,35h; INT21` at0056..0059 remains in place.
The three original bytes `CLD; CS:LODSB` move unchanged to a same-CS
gateway; pre/post collectors snapshot registers, FLAGS, PSP:2, IVT0,
IVT21 and **DS[63d8,7b52)** before their own DOS output calls.
Both snapshots are contiguous in an exact **12094-byte** record.
Original instructions stop005a, before the first returned-pointer save.

| Observed state | Before / after |
| --- | --- |
| Installed IVT21 | F000:14a0, unchanged |
| Current IVT0 / returned ES:BX | F000:1060 / F000:1060 |
| DS / SI / DI / CX | 1b12 /023a /7af0 /19, unchanged |
| SS / SP | 22c8 /ffec, unchanged |
| PSP:2 | 9fff, unchanged |
| Protected memory | All **6010 bytes** unchanged; pre-state heap/clear/class checked |

The pre-snapshot follows LODSB but precedes MOV AH,35: its AX is **9f00**
(PSP-end high byte plus vector0), not3500. The untouched MOV establishes
3500 at the actual INT. BX/ES change to the result; other recorded
registers and flags are reported, not silently assumed to be preserved.
IVT21's measured address is **not a review of its handler bytes**.

This is finite, disclosed instrumented endpoint evidence, not a universal
DOS ABI, transient-write absence, handler-internal stack/return-content,
other-memory/code/table integrity, normal-program or whole-loop proof.
The remaining18 queries, pointer stores and later vector installation
have not executed in this new case. No Pascal parity, successful allocator
call, later heap lifetime, source recovery or learning claim follows.
The general service-contract gate remains **false**.

Bootstrap uses four scratch stack bytes; each snapshot uses14 at maximum
(including PUSH CS), within the original guaranteed allocation and disjoint
from captured data/code and appended payload. Independent GNU objdump
confirms scratch restoration, relocated prefix and jump back to0056.
**Historical disclosure erratum:** frozen patches.json inherited the old
ten-byte bootstrap description. Preserve that file/freeze unchanged; the
actual frozen service bootstrap is four bytes. Current reporting corrects
this metadata only. No original execution was repeated after the change.

Before evaluation,39 synthetic/patch checks passed. An initial fixture
incorrectly expected a low FLAGS carry-bit change to violate the premises;
changed the mutant to TF instead (CF is not a service-input requirement).
The pre-AX check was corrected from0 to PSP-end high byte before the run.
Final **492 connected regressions pass**, with the prior frozen heap and
new service executions both excluded; the separate single service test
passed once. Includes invalid-but-unchanged baseline and injected worker
failure/no-retry checks. This is not a whole-repository test count.
The existing allocator engine prompt now carries the scoped observation
and limitations; no scheduler eligibility or acceptance gate is relaxed.
Audit stays27/295 source,4 partial,34 host,0 full original-binary,1 stale.

Immutable evidence in session `files/liero-dos35-original-20261102/`:
`test_instrumented_first_servic0/service/` holds freeze, original trace,
instrumented image, methods, symbols, build/worker logs and patch inventory.
`liero-dos35-final-20261102/` holds final regression reports.

- Trace SHA256: `1c1f3c568ff9fc2de58719a939c4147371e698dead681cfaf5be835df891478b`
- Instrumented SHA256: `58456e6d5d72bf195a58cd3afc9374f057a136117c528afd06a62f8180c18f42`
- Freeze SHA256: `c854f03bcf64485fbec47a1147c4ef2a0ac6dc5c70e11b69c242682b7add6b07`

Next bounded question: under this measured first-call context, do original
005a..0063 save only the returned pointer at7af0..7af3 and establish the
next vector2 request without disturbing the tracked heap/stack state?
Reuse this probe, freeze a distinct case and stop at that next external
boundary. Do not extrapolate AL0 service evidence to AL2 or all19 calls,
vector installation, allocator entry or whole-startup acceptance.

### 2026-11-02: first post-heap boundary is DOS vector query at0058

Authenticated all27 original bytes0049..0063 and19 vector-table bytes
CS0239..024b, with actual MZ relocation exclusions. No new vector-service
execution was performed; existing original probes are regression replays.
Before0058 the prefix performs no global writes:
DI=7af0, CX=19, CS:LODSB advancesSI to023a, CLD setsDF0, AX=3500.
**INT21** invokes the handler at physicalIVT[0084,0088); **AL0 requests
vector0**, not execution of vector0. ActualIVT21 target/handler bytes,
DOS/internal stack use, return and protected-memory effects remain unproved.
This is the first external boundary after the measured heap checkpoint.

[RBIL AH35 documentation](https://fd.lod.bz/rbil/interrup/dos_kernel/2135.html)
confirms AH35/AL vector number -> current handlerES:BX. It supplies **no
proof of this installed handler's preservation/effects**. The original loop
requires DS/SI/DI/CX and SS/SP/return bindings to survive; code/table and
heap/PSP/callback state must not be changed by the service or external
mutation. AX is reloaded and CLD executes each iteration at0053, so DF
preservation across service calls is not required for this loop.

Conditional on those premises,19 queries use vector IDs
`00 02 1b 21 23 24 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 75`.
ReturnedBX/ES words are stored, **not dereferenced**, at4-byte slots
DS7af0..7b38, occupying **[7af0,7b3c)**. This ends exactly before the
allocator saved-request word7b3c; it does not overlap heap/callback cells,
reviewed code or active return stack under checked startup provenance.
The six-byte real-mode INT frame is within the guaranteed allocation and
disjoint from these cells; additional handler stack use remains unknown.
LOOP0062 targets0053; conditional loop exit is0064. No post-service state
or subsequent vector-installation calls are accepted.

Extended the existing startup contract with an exact boundary report and
published the same blocker/conditional footprint in the existing allocator
prompt.54 new tests bind original bytes, all loop/table mutants and actual
relocation overlaps. A relocation-test fixture initially omitted the offset
component when choosing a relocation to replace; fixed it and retained the
failure separately. **436 connected tests pass,1 deliberately deselected**:
the previous frozen heap execution is not rerun. Existing trace/artifact
replay is evidence reuse, not a new experiment. No Pascal/ledger promotion,
model request or new source recovery; audit stays27/295,4 partial,34 host,
0 full original-binary passes and1 prior stale recovery.

Session `files/liero-startup-vector-final-20261102/` holds current byte-bound
reports/method snapshots; `files/liero-startup-vector-review-20261102/`
holds original slices/independent decoding, reference, prompt and audit.
Next exact check: establish an explicitly scoped installedINT21/AH35
return/register/protected-memory contract before carrying heap facts past
0058. Reuse the current instrumented boundary probe; do not infer service
preservation from its name, or turn initial capacity into allocator success.

### 2026-11-02: instrumented original heap/PSP state observed before0049

Extended the **existing** startup contract/probe with an explicit `--heap`
mode. It preserves original entry, clear, CPU leaf, heap initializer,
relocations and file-backed initial data; unlike the old clear experiment,
it does **not** dirty the DS window. Only the original header entry/size/
extra-allocation fields and a three-byte jump at0049 change. Appended
bootstrap/collector code remains disjoint from measured data/code/stack.
Total minimum/maximum allocation is preserved by reducing extra paragraphs
as file-backed paragraphs grow. This still changes the loaded image and
is **not an unmodified normal run**.

One frozen original-only DOSBox case passed. The collector records PSP:2
**before its first DOS interrupt** and stops original execution before0049,
so no later original interrupt/call is included. Exact trace shape is8210
bytes:8192-byte DS window plus nine recorded words. Validation checks all
5932 cleared bytes,14 initialized/state words and the CPU-class byte
(**5961 memory bytes**, not the entire captured window).

| Observed state | Value |
| --- | --- |
| Module load segment / PSP | 01a1h /0191h |
| Original CS / DS / SS / SP | 167eh /1b12h /22c8h /ffech |
| ES after original heap setup | 0191h, the saved PSP |
| Heap start / PSP allocation end | 32c7h /9fffh |
| Spare initial heap capacity | **447360 bytes** |
| Free-list and cursor/sentinel | Both0:32c7h |
| Limit pointer | 0:9fffh |
| Callback installed | 167eh:00d6 |
| CPU class observed | 2 in this DOSBox configuration only |

These are environment-scoped observations, not guessed constants to
hardcode into recovered source. They corroborate the scoped startup
projection and demonstrate extra capacity in this instrumented run,
while the MZ **minimum** still guarantees zero spare heap. Capacity is
**not allocator success**, proof of64000-byte buffer provenance, Pascal
parity, full ABI, CPU-family coverage, or later heap/callback lifetime.
No allocator call was executed by this new heap experiment.

The existing0353 contract/prompt now includes measured values with trace,
instrumented-binary and pre-execution freeze identities plus explicit
limitations. Static byte-mutant, initial-data, exact-shape, state/record
mutation and injected-environment-failure tests preserve fail-closed,
no-retry behavior. Prior clear/Pascal mode remains unchanged in behavior.
**383 connected tests pass** across two disjoint selectors:145 probe tests
(including the single new heap case) plus238 remaining connected tests.
The latter were rerun after fixing a missing JSON comma in the observation
configuration; the failure is retained, not counted as an original failure.
Ruff/format/Python syntax/whitespace checks pass.

Session `files/liero-heap-observe-final-20261102/` preserves the frozen run,
patch inventory, original-only trace and method snapshots;
`files/liero-heap-observe-connected-final-20261102/current/` contains final
connected reports. Review/hashes/prompt/audit are in
`files/liero-heap-observe-review-20261102/`. No Pascal/source acceptance,
model request or training promotion. Audit unchanged27/295 source,4 partial,
34 host passes,0 full original-binary passes and1 prior stale recovery.

Next bounded prerequisite: trace original startup **from0049 toward the
first allocator use**, identifying the first unresolved external/direct
callee that can affect DS, PSP, heap or callback lifetime. Stop there and
resolve its contract before extending the observation. Do not equate this
initial-state measurement with preservation through the remaining startup
or parent5e66. No larger model trial or guessed allocator body.

### 2026-11-02: CPU leaf return/segment projection closes one startup gate

Reviewed **all37 original bytes** of00b1 at file91633, actual MZ relocation
exclusions and the nearCALL000e ->00b1. Independent original-byte objdump
confirms both conditional branches target00d2, the byte store toDS6420,
then nearRET00d5. All three path shapes terminate there; each PUSHF/PUSH BX
pairs with POP BX/POPF/POP CX before either branch. No loops, calls,
segment writes or other non-stack writes occur. Under explicit ordinary
real-mode, **TF=0/no-fault/no-trap/no-asynchronous-mutation** premises and
the existing checked stack/store bounds, DX/SI/DI/BP/DS/ES/SS are preserved.
CPU entrySP=FFEA, minimumFFE8, returnSP=FFEC at0011. Its temporary stack
word and DS6420 are writable and disjoint from code, live return stack
and reviewed heap cells. Thus the original return/segment/write-footprint
projection no longer depends on guessing a CPU class.

The class itself remains hardware-dependent: first FLAGS readback high
nibbleFh stores0; otherwise second readback0 stores1, else stores2.
This is a complete static path review, **not execution of three CPU
families**, host FLAGS emulation, Pascal parity or new routine recovery.
The historical Pascal body writes only2; it remains unchanged/unreviewed.
No protected-mode, single-step, interrupt-handler or full FLAGS ABI claim
is made. No original execution cases or model requests were added.

Extended the **existing** startup contract with `startup_cpu_contract`,
retaining the old clear-only interface and frozen prior methods. New
tests reject mutations of every leaf byte, changed call target, overlapping
loader relocation and an aliasing store into the live return stack.
The engine now has a scoped00b1 contract; allocator startup evidence uses
its checked projection instead of the previous unresolved00b1 premise.
It remains a startup prerequisite, not a fictional direct allocator call.
The three existing load-base heap checks now compose that projection and
verify that its sole global store cannot alter the heap cells.

**280 connected tests pass**; focused Ruff/format and Pylance syntax checks
pass. Audit remains27/295 source recoveries,4 partial,34 host passes,
0 full original-binary passes and1 prior stale recovery. Reports, current
source/method hashes and original leaf/independent decoding are in session
`files/liero-cpu-startup-final-20261102/` and
`files/liero-cpu-startup-review-20261102/`; the initial missing-projection
failure is preserved separately. No Pascal or acceptance ledger changed.

Next bounded check: reuse the existing disclosed instrumented-MZ probe to
observe startup state **before0049**, including saved PSP/PSP:2 and heap
cursor/limit/callback cells. Preserve original call/clear/CPU/heap bytes,
stop before subsequent DOS interrupts/calls, and do not treat instrumented
observations as an unmodified normal run or allocator success. Actual
capacity and later state/callback lifetime remain blockers; minimum
allocation still guarantees zero spare heap. No guessed malloc, caller
rewrite, graph rebuild, model sweep or source promotion is justified.

### 2026-11-02: conditional heap initialization and default callback identified

Authenticated startup0011..0048 against all56 original bytes, with no
overlapping actual MZ relocation. Reused the existing successful-MZ-loader/
startup-clear contract, rather than inventing heap fixtures. Original0003
bytes8eda are **MOV DS,DX**, not the reversed exported MOV DX,DS; corrected
that listing line. The1971h immediate is relocated by the loader, so the
logical2971h display is not an observed DOS segment.

The intervening nearCALL000e targets00b1, a37-byte CPU/FLAGS-sensitive leaf.
Its return/segment contract is **not established by this milestone**.
Conditioned on its return preserving DS/SS/SP and relevant state:
startup computes `H=SS+((SP+13h)>>4)` using16-bit ADD/SHR and initial63d8=0.
It stores H into63de/63e0/63e2/63ec/63f0/63f8. Initial63d8/63ee/63f2/63f6
are file-backed zero words with no overlapping relocations; thus free-list
0:H equals cursor/sentinel0:H initially, rather than an invented list node.
Existing clear6426..7b52 covers saved-request7b3c. These cells lie in the
guaranteed writable allocation, disjoint from the reviewed code and active
stack, **at this scoped startup point**, not necessarily at allocator entry.
Saved entryES supplies PSP:2 ->63f4 only under the ordinary valid DOS PSP
premise; the actual allocation end has not been observed.

Stores003f/0045 install **startupCS:00d6** at63fe/6400. All five original
callback bytes are `33c0ca0200`: XOR AX,AX; RETF2. Under a valid disjoint
nonwrapping far-return stack this returns AX0,CF0,ZF1, pops IP/CS and one
argument word (SP advances6), preserves BX/CX/DX/SI/DI/BP, DS/ES/SS/DF
and does not access the heap.
This callee-free instruction review is not Pascal parity, a new recovered
routine, or proof that this handler remains installed at later0402/040e.
No new Pascal body or routine acceptance was introduced.

Crucially, the MZ **minimum**201312-byte module allocation ends exactly at H:
it guarantees **zero spare heap bytes**, not capacity for the64000-byte
buffer request. DOS may allocate more; do not substitute the minimum for
actual PSP:2, infer allocation failure in a real run, or assume success.
Checked arithmetic at three disclosed load bases is not three original
executions. No new execution cases or model requests occurred.

[Existing allocator tests](../../../tests/test_liero_allocator_contract.py)
now bind these bytes, initial data, relocations, bounds, callback and
minimum-capacity result to the scoped engine contract/prompt. The initial
missing-contract regression is preserved separately. **240 connected tests
pass**, including exhaustive actual-source size-helper comparison and prior
startup/sign/random/drawing/engine regressions. Ruff/format checks pass.
Audit stays27/295 source recoveries,4 partial,34 host passes,0 full original-
binary passes and1 pre-existing stale recovery.

Session `files/liero-heap-init-final-20261102/` preserves final test results,
method/source snapshots and reports; `files/liero-heap-init-review-20261102/`
holds original startup/callback slices and the unchanged audit. Next bounded
prerequisite is00b1's CPU/FLAGS-sensitive return/segment contract. Then
revisit startup state preservation and actual PSP capacity before any
allocator execution. Later interrupts/calls, callback replacement, dynamic
heap stores and parent5e66 DS/buffer lifetime remain explicit obligations.
No guessed allocator, new framework, graph rebuild or long model run.

### 2026-11-02: allocator size prerequisite corroborated; heap/handler gate remains

Followed028a ->0353 ->04dc in callee-first order. The size helper04dc was
**already source_recovered**; no new body or attestation was needed.
Authenticated its complete17 original bytes at file92700 with no overlapping
actual MZ relocation. ADD AX,7 supplies carry to RCR DX,1; three SHR operations
and AND AX,8 yield `rounded=8*ceil(unsignedRequest/8)`,
`AX=rounded mod16`, `DX=rounded div16`. This pair represents **DX*16+AX
bytes**, not the ordinary unsigned32 value of packed DX:AX. The existing
Longint function packs register bits, not the physical byte count.
Request64000 yields AX0/DX4000 paragraphs;65535 yields AX0/DX4096,
representing65536 bytes. Final CF0,ZF iff AX0; DF is unchanged.

[Focused regression](../../../tests/test_liero_allocator_contract.py) compares
**all65536 unsigned inputs** against original execution, actual historical
Pascal and independent rounding arithmetic. AX/DX, modeled CF/ZF/DF and
packed function return agree. Original-only BP/SP/DS/SS observations are not
host ABI equivalence. Source/config/method hashes freeze before execution;
the existing unchecked16-bit FPC `-Mtp` contract is retained: **no range-checked
`-Cr` claim**. Inputs start CF1 and alternate DF. This is corroboration of
an accepted known body, not new-routine recovery or unseen model success.

Authenticated all203 original0353 bytes at file92307, no overlapping MZ
relocation. Its nearCALL035a targets04dc. Independent original-byte decoding
exposed **three reversed segment MOVs in the exported listing**:

| Address | Original bytes | Correct instruction |
| --- | --- | --- |
| 24dd:0362 | 8ec1 | MOV ES,CX |
| 24dd:03ac | 8ec2 | MOV ES,DX |
| 24dd:03ef | 8ec3 | MOV ES,BX |

Corrected only these listing directions and bound them with byte/text tests;
the initial failure and earlier listing snapshots remain preserved.
In particular0360 MOV CX,DS followed by0362 establishes **ES=entryDS**
locally, not a read of arbitrary incoming ES. Before it, the nonzero path
stores the original request at DS7b3c. At0368 it dereferences the far-list
cell DS63f6. This is the first unproved heap dependency, requiring provenance,
writable/nonaliasing saved-request state, valid list nodes and topology.
Cursor/sentinel DS63ee/63f0 and limit DS63f2/63f4 also lack established
initialization/bounds. Dynamic ES:DI writes cannot be accepted from this
local segment assignment alone. Zero request branches directly to03ce,
XOR AX,AX/CWD/RET, with no heap access under a valid near-return stack.

Indirect far calls0402/040e use DS63fe/6400. The growth path pushes0;
exhaustion pushes the saved request. Actual callback targets, stack cleanup,
DS/register effects, heap changes, outcomes and retry termination remain
unproved. The028a wrapper also has a failure JMP010f requiring its own
contract; its parameterless skeleton is not proof of request/return ABI.
No heap fixture or allocator execution with invented state was introduced.

Published scoped04dc facts and **blocked**0353/028a contracts through the
existing configuration and one-hop prompt mechanism. A real allocator prompt
includes the rounding projection, corrected segment provenance and explicit
heap/handler limitations. Both allocator sources and caller0895 stay
unreviewed; no Pascal source, ledger acceptance, model request, training or
knowledge promotion changed. **285 focused tests pass**, new-test Ruff/
format/Python syntax and whitespace checks pass. Audit remains
**27/295 source recoveries(9.15%),4 partial,34 host passes,0 full
original-binary passes**. Existing broader runtime failures are unchanged.

Session evidence: `files/liero-allocator-before-20261102/` preserves initial
listing-regression failure and original/source helper pass;
`files/liero-allocator-final-20261102/` contains final exhaustive traces,
source freezes and static contract report;
`files/liero-allocator-review-20261102/` contains original slices, corrected
method snapshots, engine prompt and unchanged-audit report.

Next bounded prerequisite: establish original initialization/provenance of
DS63f6, cursor/limit cells and the saved-request cell, then identify the
DS63fe callback contract from its actual writes/relocations. Reuse the
existing startup evidence; stop at unresolved initializer/callback dependencies.
Do not assume heap-list validity, successful allocation, DS continuity or
buffer lifetime merely because rounding is checked. The0895 buffer/seed,
loop/overflow and full ABI obligations remain; no larger model run is justified.

### 2026-11-02: caller input provenance reaches the engine without unblocking recovery

Completed the next bounded0895 input-provenance assessment. Two authenticated
incoming far-call slices belong to unresolved **FUN_1000_5e66**:

| Setup slice | Original file offset | Far call | Destination |
| --- | --- | --- | --- |
| 1000:7e3c,70 bytes | 38316 | 1000:7e7d | ES:DI loaded from DS:6684 |
| 1000:8411,74 bytes | 39809 | 1000:8456 | Same cell, then ADD DI,00a0h |

Both original calls encode offset0895 and relative segment0ec2, with actual
MZ segment-word relocations at slice68/72. These are two checked direct
sites, not proof that no indirect/aliased callers exist. The supplied start
coordinates are wrapped16 object X/Y minus DS67b0/67b4 or67b2/67b6;
target X/Y are parent frame BP-6+7 and BP-8+4. The slices push the far
pointer directly, not a proven linear host address. The second view adds160
to the **offset alone modulo65536**, without segment normalization.
Argument bindings require valid disjoint frame/stack/code and input cells;
changed SS/SP or aliasing stores invalidate them.

Startup's15 original bytes at1000:e50b (file64635) push unsignedFA00h=64000,
far-call24dd:028a with an actual MZ relocation, then store AX/DX at
**post-call** DS6684/6686. Requested size is not proof of successful
allocation, returned pointer normalization, preserved DS or pointer lifetime.
The exact21-byte028a wrapper near-calls0353; both allocator routines remain
unreviewed. Stop at this concrete producer dependency and unresolved parent
DS/pointer effects rather than assume a successful allocation. No path from
seed writers to this caller, actual DS value or initial seed was established.

The drawing leaf's maximum coordinate displacement is50397. For the two
views, a sufficient common nonwrapping base offset is **<=14978**, with
valid writable/nonaliasing physical bounds through base+50557 (50558 bytes).
That footprint would fit a valid64000-byte allocation, but the request alone
does not establish one. Exhaustive arithmetic over all65536 possible offsets
identifies exactly14979 satisfying both nonwrapping conditions. An explicit
excluded arithmetic example starts at offset15000: left view ends65397,
whereas the right view's linear end65557 wraps to original offset21.
This is static arithmetic, **not an executed caller or new Pascal parity**.
Actual offsets remain unknown; high-offset alternatives are not silently
normalized or folded into the checked linear projection.

Published these supported conditional facts in existing
[routine contracts](../config/routine_contracts.json). The engine previously
injected only a routine's own contract and decompiler-derived sibling
signatures. [Drafting](../../../engine/draft.py) now carries **one hop** of
explicit `callee_contracts` into the caller prompt, including declaration,
scope, arguments, memory model, semantics and limitations. The shared
[loader/renderer](../../../engine/routine_contract.py) rejects malformed,
missing, duplicate or self references; it does not recursively expand cycles.
Relations are reviewed input, not automatically inferred from decompiler
text. Changed callee premises reach the next prompt without a cache.
Neither loading nor displaying a partial contract resolves a dependency,
permits execution or promotes source.

The actual engine prompt now includes checked random-scaling and drawing
constraints without needing a C seed. Actual scheduler regression still
reports4654/0dc8 as unresolved prerequisites and **does not select0895**.
No guessed caller/body, new model request, learning claim or knowledge/source
promotion. **283 focused tests pass** (278 engine/source/evidence tests plus
5 drafting-settings tests); Python/Pylance syntax and focused lint pass.
Drafting retains its10 pre-existing Ruff diagnostics, unchanged against HEAD;
pre-existing whole-file formatting differences were not mass-reformatted.
Source audit remains **27/295 recovered(9.15%),4 partial,34 host passes,
0 full original-binary passes**. Replayed source oracles are not independent
new evidence.

Session evidence: `files/liero-caller-provenance-checked-20261102/` preserves
the source-bound static report and scoped source regressions.
`files/liero-caller-engine-context-checked-20261102/` contains the real
prompt and scheduler report (zero model requests, caller_selected=false).
An initial scheduler-test import typo was corrected; the first failed run is
separate from final validation. Earlier method/trial freezes remain historical.

Next bounded prerequisite: establish allocator028a through its direct callee
0353 in callee-first order, or record the first unresolved heap/handler
dependency that prevents its allocation/DS/ABI contract. Do not recover the
11677-byte parent by assuming those contracts. Parent DS continuity, pointer
lifetime/nonaliasing, seed mapping, caller loop/overflow and full ABI remain
explicit obligations before0895 source acceptance. Keep the existing25%
expansion floor; this is reusable engine context plus static provenance, not
automatic new-routine yield.

### 2026-11-02: random-state bug fixed and conditional caller constraints checked

Returned to connected source recovery, reviewing callee **FUN_24dd_46b1**
before its scaling wrapper **FUN_24dd_4654**, not extending syntax search.
The54-byte near leaf at original file109553 and29-byte wrapper at109460
match original bytes; no actual MZ relocation overlaps either slice or the
following CS:46e7 constant8405h. The wrapper's CALL displacement005a targets
46b1. Complete straight-line review establishes the scoped recurrence
`nextState = (state * $08088405 + 1) mod 2^32`.
State is low/high words at DS:6412/6414; unsigned low*8405 gives DX:AX,
wrapped shifts/byte adds contribute low*0808 and high*8405 to the high word,
then ADD AX,1/ADC DX,0 completes the increment. It has no callees/branches.

The historical manual Pascal incorrectly incremented the **old seed low
word**, not the low multiplication product. Its initial range-checked run
failed with runtime201; compiling the archived old source without range checks
exposed **1681/1753 state/return mismatches**. Seed1 should yield08088406,
not old08080002. Corrected the actual source's low-product increment and
explicit16-bit carry wrap, including seed26B05733 producing full32-bit zero.
This is debugging a known manual body, not new model-generated recovery.

After callee nearRET, original wrapper reads unsigned bound at SS:SP+4.
Two unsigned MULs and ADD/ADC compute
`floor(nextState * bound / 2^32)`, then MOV AX,DX/RETF2. Bound0 returns0 but
still advances state; positive bound returns0..bound-1. Existing Pascal
scaling arithmetic is unchanged. Its signed Integer result preserves16 bits,
not an unsigned interpretation for results>=32768. Its modeled RegisterAX
remains the generator low word, not original wrapper's final AX; full
register/flag/return ABI is explicitly outside this projection.

[Actual-source regression](../../../tests/test_liero_random_source.py)
passes **1754 scoped original/actual-Pascal cases**:292 direct generator and
1462 scaling calls, with corner/mixed seeds, bounds0/1/2/5/65535, carry and
full32-bit rollover. Source/harness/config/assembly hashes freeze before
execution; actual sources compile/run under FPC `-Mtp -Cr`.
Python independently predicts recurrence/high product. Original and Pascal
state/return and adjacent guard words agree. A separately allocated writable
64K DS is disjoint from retained COM CS/SS/code/corpus; source DosMemory and
CodeMemory mirror that fixture. Original-only BP/SP/DF/DS/SS/ES observations
are **not host ABI equivalence or normal-program reachability**.
The broader runtime's deliberately synthetic A55A multiplier fixture now
expects lowEA49 rather than1235 (highCDB9/scaled803 unchanged). An isolated
actual-source `-Mtp -Cr` fixture compiles and passes those assertions; this
is not original8405 parity. Earlier unrelated broad-runtime failures remain.

Published scoped generator/scaler facts in existing
[routine contracts](../config/routine_contracts.json), with conditional
constraints propagated through the actual0895 call sites. Original PUSH5,
OR AX,AX/JNZ, conditional PUSH2 and ADD AX,0053/PUSH AX establish first
result0..4 and conditional color83/84. Exact ADD encoding is055300, not the
equivalent83c053 spelling; the initial new assertion failure was corrected
against original bytes. Drawing arguments push columnBP-2,rowBP-4,color,
then the original segment/offset. No caller implementation is installed:
actual DS/seed initialization, buffer allocation/far-offset nonwrap premises
and wrapped arithmetic/loop termination remain unresolved.

Both random routines are **partially_recoverable**, not source_recovered.
Audit: **27/295 source recoveries(9.15%),4 partial,34 host passes,0 full
original-binary passes**. **238 focused tests pass**, Ruff/format/syntax/
whitespace checks pass, and the full actual target compiles with existing
warnings. No model request, training/example promotion or new long run.

Persistent session evidence:
- `files/liero-random-before-20261102/`: source-bound runtime201 failure.
- `files/liero-random-old-semantic-control-20261102/`: archived old-source
  unguarded comparison and1681/1753 mismatches; not repaired or overwritten.
- `files/liero-random-fixed-20261102/`: earlier1753-case passing source run.
- `files/liero-random-reviewed-20261102/`:1754-case passing random run;
  surrounding focused suite initially failed the new caller encoding assertion.
- `files/liero-random-final-20261102/test_actual_random_source_and_0/`:
  final1754-case freeze/source snapshots/original and Pascal outputs/result.
- `files/liero-random-build-20261102/build.log`: full actual target build.
- `files/liero_random_synthetic_fixture.pas` and the build directory's
  `synthetic-build.log`/`synthetic-runtime.log`: isolated synthetic-fixture check.

Next bounded question: establish actual0895 DS/seed provenance and its
BP+6/+8 destination pointer/offset/allocation premises using original callers
and shared initialization. Stop at a concrete unresolved producer/callee;
do not infer those premises from isolated tests or implement0895 with guessed
globals. Checked recurrence/scaling narrows its behavior but does not resolve
the caller or lift the25% expansion floor.

### 2026-11-02: type-safe drawing mechanism passes a fresh bounded trial

Extended the existing pilot's closed-sketch machinery with a drawing schema,
renderer and exact-source execution gate. The full62 original bytes must match;
all62 single-byte mutations are rejected. Only the two supplied equivalent guard
styles are renderable. Conflicting stride/bounds/order/zero-color hypotheses,
missing/extra fields and arbitrary Pascal text are rejected, not repaired.
The renderer supplies `Longint(row)` widening, `Byte(color)` and the existing
RealModeMemory store. The execution gate requires exact renderer output, not a
regex claim that arbitrary Pascal is safe. Proven input bounds remain necessary.
Both styles compile under FPC `-Mtp -Cr` and match independent projection
expectations. No target Pascal or ledger status was changed.

Fresh trial frozen before generation: one local qwen2.5-coder14b structured
request, temperature0/2048-token cap, no repair/fallback, original hash/actual
relocation check, method/schema/corpus/harness/model digests, supplied topology,
fixed arena bounds, training/withheld indices and stop rules. The pre-run
developer control matched the existing53-case original trace. The sole model
proposal passed the closed gate and rendered **identically to that control**;
its source-bound compilation/output were reused rather than rerunning identical
oracle work. Training **46/46 (3015392 bytes)** and terminal withheld-from-feedback
assessment **7/7 (458864 bytes)** agree. The excluded far-offset-wrap case still
disagrees, as expected; it is not included in the pass.

This removes the demonstrated type/memory-output mechanism blocker, but is
**not** an independent recovery or measured model improvement. All semantics,
casts and topology were developer-supplied; the developer/control had already
seen the whole development corpus, including the withheld subset. The model
selected equivalent syntax. No unseen holdout claim, adapter training, knowledge
promotion, source acceptance or expansion-yield gain. Earlier0/2 raw-source
failures, safety-stop deviation and overnight trial remain unchanged.

Evidence: session `files/liero-draw-typed-trial-20261102/` contains the freeze,
method snapshots, one raw response/proposal, selected include, control build/
output, hashes and terminal result. The driver is session
`files/run_draw_typed_trial.py`. Response-to-rendering/source and archived
original/Pascal bytes replayed successfully. The pilot method hash is now
`9761d15648dc5875fae92cb43f98d1c45eea58ccaaf601144addddc3cc1edd88`;
older frozen method snapshots retain their earlier identities.

**399 focused tests pass**, Ruff/syntax/whitespace checks pass, and the actual
target compiles with existing warnings. Audit remains **27/295 source recoveries
(9.15%),2 partial,32 host passes,0 full original-binary passes**.

Next source milestone: resolve random-state dependency4654 callee-first and
the actual0895 drawing-buffer/offset premises before implementing that caller.
Do not extend syntax trials or start another overnight run merely because this
known-slice mechanism passes.

### 2026-11-02: scoped drawing review and a stopped engine comparison

Reviewed **FUN_1ec2_0dc8**, a callee-free62-byte leaf at original file69976.
All bytes and five exits were checked; no actual MZ relocation overlaps it.
BP+6/+8 supply the destination offset/segment, BP+10 the low color byte,
BP+12 signed row and BP+14 signed column. Nonzero color and coordinates0..157
write one byte at `segment*16 + ((offset + row*320 + column) mod65536)`.
All exits join LEAVE/RETF10 at slice58. `OR [BP+10],0` is a same-value stack
write, not just a read. No calls, DS/global accesses or direction-dependent
instructions occur.

The existing historical manual Pascal models a **linear base**, not a packed
far pointer. Under proven writable, nonaliasing bounds, a sufficient memory
projection premise is offset<=15138 and physical base+50397<1MiB.
Actual source/helper pass **53 nonwrapping cases**, checking **3474256 arena
bytes**, including three complete158x158 grids (**74892 writes**), signed
bounds, colors0/1/127/128/255 and16 guard bytes. DOS allocation is separate
from the retained COM code/data/stack. Original-only BP/SP/DF/DS/SS observations
pass but are not host ABI equivalence.

An excluded counterexample deliberately demonstrates the missing behavior:
offset15139,row157,column157 writes original offset0, whereas linear Pascal
writes65536. The body remains **partially_recoverable**, not source_recovered;
its signature/algorithm were not rewritten to guess the caller's pointer
representation. Caller0895 still needs buffer provenance, random dependency
4654 and its own loop/arithmetic review. Source recoveries remain **27/295
(9.15%)**, now **2 partial**, **32 host passes**, **0 full original-binary
ledger passes**.

Published the scoped facts through existing `config/routine_contracts.json`,
not a new graph/probe framework. This exposed and fixed the existing contract
declaration matcher rejecting semicolon-separated Pascal parameter groups;
positive and malformed-declaration regressions cover it.

Then ran the existing drafting engine twice on the same known slice with local
`qwen2.5-coder:14b-instruct-q4_K_M`: signature-only versus checked-contract
context, identical ASM/C/declaration, isolated empty knowledge/no adapter,
temperature0 and768-token cap. No historical body in either prompt, no
candidate repairs/retries. Both outputs sanitize:

| Arm | Compilation | Scoped execution |
| --- | --- | --- |
| Signature-only | Pass | Not run: casts modeled DOS address to invalid host pointer |
| Checked contract | Fail: Char assigned to Byte array | Not run |

The assisted output uses the intended RealModeMemory space, but **0/2**
candidates qualify for scoped evaluation. **No measured verification gain**,
no held-out evaluation, source installation, training promotion or weight
learning. Expansion stops below the25% floor. Pre-execution inspection stopped
the baseline for safety; this was not a preregistered scoring gate, so the
planned runtime comparison is explicitly incomplete, not a paired parity result.

Evidence: session `files/liero-draw-reviewed-20261102/test_actual_draw_source_and_or0/`
contains original/actual-source freezes and traces;
`files/liero-draw-engine-paired-20261102/` contains the pre-request freeze,
both prompts/raw responses/candidates, compiler logs and terminal `result.json`.
Its ledger snapshot predates the later arithmetic typo correction in validation
notes; preserve it as historical. **194 focused tests pass**, full target
compiles with existing warnings. Earlier unrelated broad-runtime failures and
all frozen overnight results remain unchanged.

Next: before another engine experiment, freeze a modeled-memory execution gate
and a bounded type-safe store representation using existing sketch machinery;
do not repair these terminal candidates or claim generalization from this
manually known slice. For connected source recovery, resolve4654 callee-first
and establish0895's buffer/offset premises before attempting the caller.

### 2026-11-02: connected sign-step constraints; independent fallback accepted

The direct caller **FUN_1ec2_0895** (296 bytes, file68645) has two original
near calls at **08BBh/08C5h** to reviewed **086Bh**. The existing sign test
authenticates the exact first54 original bytes and excludes prefix relocations:
`c80e00008b46108946fe8b460e8946fc8b460c2b46108946f88b460a2b460e8946f6ff76f855e8adff8946f4ff76f655e8a3ff8946f2`.

Under valid writable nonaliasing SS-frame/code/argument premises, the solved
contract establishes **BP-12 = sign16(wrap16([BP+12]-[BP+16]))** and
**BP-14 = sign16(wrap16([BP+10]-[BP+14]))**. Each result is FFFFh/0/1.
The intervening PUSH BP supplies the unread first argument—not an output
pointer. This is supported constraint propagation, not a recovered caller.

The caller also has four actual relocated far calls to **FUN_24dd_4654**,
at slice offsets150/167/255/272, and two PUSH CS/near calls to
**FUN_1ec2_0dc8** at182/287. Those direct callees remain unreviewed.
Random-state/drawing effects, valid destination buffers, wrapped signed
absolute -32768 and loop termination remain unresolved. The caller stub is
unchanged; no guessed service behavior or source acceptance was introduced.

The planned fallback independently reviews **FUN_1ec2_09bd** at original
file**68941**, all42 bytes/no relocation overlap, actual body and existing
SignWord helper. The bytes match086b but this entry's mapping and signed
paths were checked independently. The parameterized existing test compares
**all65536 signed-word returns** at this entry, including original-only
BP/SP/alternatingDF/DS/SS observations. No host/DOS ABI or normal-program
reachability claim is made. Complete static/source review—not tests alone
or sibling identity—supports an explicit source_recovered entry.

Current audit: **27 valid reviewed source recoveries/295 (9.15%)**, **1 partial**,
**31 host passes**, **0 full original-binary ledger passes**. **136 focused
tests pass** and full target compiles. No model request, training-example
promotion or new framework; earlier broad-runtime failures remain unrelated.
Session `files/liero-sign-connected-20261102/` retains caller constraints,
blockers and both independent source/trace freezes. Ledger hash in the caller
assessment is the historical pre-sibling-acceptance snapshot.

Next: resolve/review drawing dependency **FUN_1ec2_0dc8**, callee-first, then
the random-state dependency before revisiting0895. Do not equate establishing
the two sign results with completing the caller.

### 2026-11-02: complete signed-word source review adds one recovered entry

**FUN_1ec2_086b** is now explicitly **source_recovered**, based on complete
original-byte/control-flow/source review plus exhaustive signed-word return
checks. This is a review of an existing manually reconstructed body, not
automatic/model recovery or original textual-source identification.

Original file offset **68603**, all **42 bytes**:
`c8020000837e06007d07c746feffffeb12837e06007e07c746fe0100eb0531c08946fe8b46fec9c20400`.
No actual MZ relocation overlaps the routine. ENTER2 sets a valid stack frame;
BP+6 is the signed-word input, BP+4 is never read. JGE/JLE partition the entire
input domain into negative, zero and positive. The corresponding stores
FFFFh/0/1 join the same local-result load, LEAVE and near RET4. Branch offsets
8/15/21/28 target 17/35/30/35 respectively. There are no callees, global
loads/stores or external services. All paths and frame-only effects are
accounted for under valid writable, nonaliasing stack/argument/code premises.

The actual `src/FUN_1ec2_086b.inc` delegates to the inspected
`LieroRuntime.SignWord` helper. Its signed Integer comparisons match the
three original branches; the test verifies the TP-mode Integer is 16 bits.
Renamed arguments to `unusedWord`/`value` in body and forward declaration
and replaced the stale oracle label. Return values are FFFFh for negative,
0 for zero and 1 for positive.

`tests/test_liero_sign_source.py` freezes method/actual-source/helper hashes
before execution. **All 65536 signed-word bit patterns** match the original
COM routine and independent expected returns. The ignored argument varies
as input XOR AAAAh; independence is established by static nonuse, not sampling.
Entry DF alternates; the original preserves it, BP=1234h, SP=FFFEh and DS/SS
in the fixture. Those original-only observations are not host ABI equivalence.
No unmodified-program reachability or all-machine-state parity is claimed.
The full original-binary ledger status stays blocked, separately from the
supported source-level review.

Current audit: **26 valid source recoveries /295 (8.81%)**, **1 partial**,
**30 host-test passes**, **0 full original-binary ledger passes**.
The other sign leaves and all callers are unchanged/unreviewed. **134 focused
tests pass**, and the full target compiles; the unrelated broad-runtime
failures reported below remain. No training promotion, model request, new
recovery framework or retrospective transfer-rate claim.

Persistent session artifact:
`files/liero-sign-source-review-20261102/test_actual_signed_word_leaf_a0/`
contains pre-run freeze, source/helper/method snapshots, raw routine,
original/Pascal outputs, logs and artifact hashes.
Next: one evidenced caller or independent original-byte review of a matching
sign sibling. Do not copy acceptance to a neighbor without checking it.

### 2026-11-02: actual target copy body checked; one partial source review

The copy deliverable is now the actual Pascal body/helper, not just a
standalone generated projection. Reviewed `src/FUN_1ec2_0000.inc` and
`src/LieroRuntime.pas:72`: the wrapper truncates count by shifting two bits;
the helper performs sequential four-byte loads/stores and advances both
pointers. Source/destination ordering matches original stack arguments.
Descriptive parameter names and a scoped oracle comment replace the old
unqualified names/"Oracle: none"; the forward declaration matches.

The existing `tests/test_liero_dword_copy_contract.py` now additionally snapshots
and compiles the actual target include/helper with `fpc -Mtp -Cr`. Across the
same **774 original-byte cases**, all **421056 arena bytes** agree. These
are source-bound replays, not independent new original inputs. The developer
projection remains a separate control. Actual source/helper hashes are frozen
before their compilation and preserved with outputs.

Ledger state is **partially_recoverable**, not source_recovered. The record
binds assembly/source/helper identities and the five review evidence categories.
The accepted source count remains **25/295 (8.47%)**; partial count becomes
**1**, host passes **29**, full original-binary passes **0**. Inherited DF=0,
disjoint valid nonwrapping ranges and stack/code separation remain explicit
preconditions. Entry DF=1, actual caller allocations and full flags/register/
far-return ABI are not implemented or attested.

The previously selected blocking predecessor is **11677 bytes** with unresolved
helper calls. It and the caller stay deferred/unreviewed rather than forcing
whole-chain recovery or creating more tooling.

Session `files/liero-actual-copy-source-20261102/test_original_bytes_vs_develop0/copy/target-source/`
retains the source-bound freeze, snapshots, trace comparison and compile logs.
**133 focused source/caller/ledger tests pass** and the full Liero target
compiles. The broad Pascal runtime suite stops before this leaf at unrelated
`Halt(97)`, or a pre-existing range error at `src/FUN_24dd_4161.inc:62` under
`-Cr`; no full-suite pass is claimed. Its temporary test additions were removed.

Next: one independent callee-free Pascal body, or a small direct dependency of
the deferred chain, validated through existing helpers/tests. No new probe
framework or learned/generalized recovery claim.

### 2026-11-02: actual dword-copy caller has unresolved premises

`tools/liero_dword_copy_caller.py` authenticates the original slice
`1000:94C5..94DC` in **FUN_1000_929a** at file **44085**, bytes
`e89ec9c43e84660657c43ed76506576850c39a0000c20e`.
The far call at **94D7** (file **44103**) has an actual MZ segment relocation
at **44106**, targeting relative `0EC2:0000` / mapped `1EC2:0000`.
The listing's displayed target is not the instruction oracle.

This caller pushes source far pointer from **DS:6684h**, destination from
**DS:65D7h**, then unsigned count **C350h = 50000**. These DS origins refer
to the state **after** the immediate preceding near call at **94C5** to
**FUN_1000_5e66**, not an assumed source/runtime DS. That predecessor and
the caller remain **unreviewed**. No post-call DF=0/DS/SS:SP/global-pointer
contract is established; resolve the predecessor's dependencies first.

The copy contract conditionally requires 50000 readable/writable bytes
(12500 dwords), initial buffer offsets <=**15536** to avoid offset wrap,
and physical nonaliasing with each other, stack and code. LES does not prove
any of those allocation properties. Ten pushed argument bytes, four far-return
bytes and saved BP/DS require **18** bytes below preargument SP; RETF10 would
restore that SP if the stack preconditions hold. These are static obligations,
not observed caller execution or full ABI parity.

**Blocked-on-caller-premises** is the result. The previous leaf corpus reaches
only count 257 / 256 copied bytes, so it cannot be cited as a measurement of
this 50000-byte call. No oracle expansion was attempted to hide the provenance
gap. No caller eligibility, normal-program reachability, new recovery or
source/ledger/example promotion is claimed.

Session `files/liero-dword-copy-caller-20261102/` retains the blocked report,
original byte/callee/ledger identities and method snapshots. **85 focused
caller/leaf tests** pass, including 33 new byte/relocation/operand/blocker
checks; historical frozen copy/pilot/rule identities remain unchanged.

Next: resolve or explicitly block **FUN_1000_5e66**, taking its direct callees
first. Revisit this caller only after the required contracts are supported.

### 2026-11-02: new scoped dword-copy contract, not unseen transfer

The next bounded slice is callee-free **FUN_1ec2_0000**, historically manual
but still **unreviewed** in the ledger. Its manual source was not read/used.
`tools/liero_dword_copy_contract.py` binds the actual file-offset **66448**
bytes `5589e51ec5760cc47e088b4e06c1e90266f3a51fc9ca0a00`, with no overlapping
MZ relocation. This adds a separate developer-authored contract, not a change
to the frozen two-shape vocabulary or a learned recovery.

The complete instruction shape establishes source pointer at frame BP+12,
destination BP+8, unsigned count BP+6 (entry SP+10/+6/+4 respectively).
SHR CX,2 followed by `66 F3 A5` copies **floor(count/4) dwords**.
No CLD occurs: **entry DF=0** is a required premise for forward copying.
Zero/sub-four counts write nothing; count remainders are left untouched.
POP DS/LEAVE/RETF10 balance the scoped stack. Valid disjoint, nonwrapping
buffers/stack/code, nonwrapping return cleanup and 80386-or-later support
remain explicit obligations. No overlapping-pointer or DF=1 claim is made.

Before original/Pascal execution the run freezes counts **0..257** and dirty
seeds **A5h/5Ah/FFh**, 774 total cases. Each arena has 256 source bytes,
16 guard bytes, 256 destination bytes and 16 trailing guard bytes. All
**544 bytes per case / 421056 total** agree between original-byte COM
execution, independently checked memory and the newly developer-authored
host-Pascal projection. The fixture explicitly supplies CLD and disjoint
buffer bounds; it does not prove those conditions for ordinary callers.
Preargument/postreturn SP **FFFEh** and preserved DS are original-only checks,
not Pascal ABI translation. No model request, heldout, source installation,
ledger status/acceptance-count change or example promotion.

Session `files/liero-dword-copy-contract-20261102/` retains the pre-run freeze,
method snapshots, original bytes, cases/traces/Pascal output and artifact
hashes. **492 focused tests** pass, including all 24 single-byte mutants,
zero/remainder/boundary/guard mutations, bad-output/corpus rejection and
explicit no-retry failure recording. Replays are not independent new cases.
Frozen pilot/rule identities and previous failures remain unchanged.

Next at that checkpoint (assessment completed above, premises blocked): connect exactly one original direct caller to DF=0 and pointer/count/
stack bounds using existing evidence. Unsupported premises remain unknown;
the new contract does not retroactively make the frozen eligibility census
or original-program reachability pass.

### 2026-11-02: instrumented caller-layout original/Pascal memory pass

The next bounded comparison is complete: three pre-frozen dirty seeds
**A5h/5Ah/FFh** each check the full **8192-byte** DS window against the generated
Pascal memory projection and a separately checked startup ES store.
**24576 bytes total**, all pass. This remains known-slice instrumented
original execution, not normal unmodified startup or full Pascal ABI parity.

`tools/liero_startup_clear_probe.py` preserves original entry bytes, the
14-byte startup prefix through the near CALL, all 18 clear bytes and the
original relocation table in a disposable MZ image. It discloses every
modified original byte:

- Header file-size, extra-memory and initial CS:IP fields redirect entry to
  a dirty-memory bootstrap and preserve original allocation totals.
- Appended payload starts at module offset **137216**, after the complete
  measured DS window `[128784,136976)` and before the active stack.
- Bootstrap saves/restores flags, AX/CX/DI/ES and SP, dirties the window, then
  far-jumps to the original entry. Original startup DS provenance and calls
  therefore execute, rather than copying the old COM DS=CS layout.
- The three bytes at startup +14 (file **91470**) become a near jump to the
  collector, reached only after original near RET. Later original startup
  calls are intentionally not executed.

Actual DOSBox observations in these three cases:

| Observation | Value |
| --- | --- |
| Load base / entry PSP segment | `01A1h` / `0191h` |
| CS after clear | `167Eh` |
| DS and ES after clear | `1B12h` |
| SS before/after original path | `22C8h` |
| SP before original entry / after clear | `FFF0h` / `FFECh` |

These are **original-only** register/stack observations. Pascal implements
memory effects, not original flags/segments/return ABI. The static mapping's
`1000h` base is illustrative and differs from this observed load base.

Startup writes entry ES at DS:640Ch, outside the clear but inside the guarded
window. The check accounts for this explicitly: **5932 zero bytes**, **2258
unchanged guard bytes**, **two independently validated ES-store bytes** per
case. The Pascal projection must leave those two bytes dirty; only then is
the checked startup ES word composed into its output for full-window equality.
The other **8190 bytes** are compared directly, without pointer masking.

Session `files/liero-startup-clear-parity-20261102/` retains the pre-execution
freeze, method snapshots, exact patch inventories, traces, generated Pascal,
compiler/runtime logs and all result hashes. Exactly one original/Pascal
execution per seed in this run; test replays do not add independent evidence.
**440 focused tests** pass, including bad-memory/register/guard/output-shape
mutants, allocation/code preservation and explicit failure/no-retry behavior.
No source/ledger/example promotion, new routine recovery or model request.
The original BYOD and frozen overnight methods remain unchanged.

Next at that checkpoint (contract development completed above): identify one bounded unresolved callee contract using existing evidence.
The unchanged two-shape vocabulary still has no new eligible transfer; new
rule development must be disclosed and frozen separately before transfer.

### 2026-11-02: exact MZ-loader/startup/492c contract

The bounded `next-global-contract` milestone is now established for the **initial
DOS-loader path**, using `tools/liero_startup_clear_contract.py`. This is a
developer-authored static contract, not learned recovery or an unmodified
normal-program execution observation.

Actual first MZ instruction at file offset **64535** is `9a0000dd14`, a far
call to relative segment `14DDh`, offset zero. Its segment word at **64538**
is relocated by the MZ table. At illustrative mapping base `1000h`, this
is `24DD:0000`. No unresolved routine runs before this startup call.
Startup at **91456** begins `ba71198eda8c060c6433ede81e49`: relocated
DS=`2971h` (operand relocation **91457**), save ES at DS:640Ch, clear BP,
then near-call 492Ch from +0Bh. Instructions are taken from original bytes,
not the listing's erroneous MOV direction or displayed call segments.

The MZ header declares **129856 image bytes**, **4466 minimum extra
paragraphs**, SS=`2127h` relative to load base and SP=`FFF0h`. A successful
ordinary loader therefore guarantees **201312 module bytes**, excluding PSP.

| Module-relative interval | Purpose |
| --- | --- |
| `[58535,58540)` | Initial far-call bytes |
| `[85456,85470)` | Supported startup prefix |
| `[104188,104206)` | Complete 18-byte clear routine |
| `[129820,129822)` | Startup save of entry ES |
| `[129846,135778)` | 2966 cleared words / 5932 bytes |
| `[201304,201312)` | Active stack writes through PUSH DS |

All relevant writable intervals are in the guaranteed allocation and disjoint
from each other and the code. Far CALL consumes four stack bytes, near CALL
two, PUSH DS another two; POP ES balances the DS push. The checked final C3
returns to startup IP=**000Eh**, restoring SP to **FFECh**. This scoped return
contract does **not** broaden generic prefix decoding: its C3 residue remains.
Actual runtime load base is not measured; `1000h` is the existing logical
mapping, and supported nonwrapping bases are derived rather than guessed.

Assumptions remain explicit: standard successful MZ allocation/relocation,
writable conventional RAM, original initial entry and no asynchronous/external
memory mutation. Full flags/register/host-Pascal parity, later startup callees
and return to main are outside this contract. No source/ledger/example
promotion or recovery-count change.

**398 focused tests** pass (48 new contract checks plus the previous 350),
including byte mutants, relocation overlap/duplication, allocation/stack
aliasing and method/report identity. Session
`files/liero-startup-clear-contract-20261102/` preserves the report and method
snapshots; binary SHA remains
`e45653ab0f915238f7394b2846b70288d0cc35a2595debc2a49502078398c7d1`.
Frozen pilot/rules and incomplete overnight evidence were not edited.

Next at that checkpoint (completed above): freeze one bounded memory comparison under this loader/caller layout,
separating instrumented original execution from Pascal effects and unmodified
normal-program observations. The earlier conditional DS=CS projection already
passed and must not be recounted as the new layout experiment.

### 2026-11-02: incomplete overnight closure and transfer frontier

The supervised continuation **also stopped**, at **03:30 UTC**: Python worker
SIGSEGV (`-11`) for candidate 0, batch 1990. Unlike the first process failure,
this produced explicit supervisor failure and process-exit state. The worker's
faulthandler log is truncated, with no comparison directory/result; the exact
native crash cause remains unknown. No overnight process is active.

A diagnostic budget was frozen at **four workers maximum**, the same candidate
source and batch-1990 512-case input descriptor, 180 seconds per worker and no
heldout/model request. Three probes under original managed Python **3.12.13**
and one under installed system Python **3.14.10** all compiled/executed/replayed
successfully. Thus the failure was not reproduced in that budget; neither an
input-dependent semantic bug nor a fixed runtime cause is established. These
replays remain diagnostics and do not refund the original unknown attempt.

The reconciler authenticated the original frozen pilot, supervisor snapshot,
input/source/report identities and both contiguous training histories:

| Completed stress evidence | Candidate-case comparisons |
| --- | ---: |
| Original run, batches 0..1105, both loop forms | 1,132,544 |
| Continuation, batches 1106..1989, both loop forms | 905,216 |
| **Total replayed** | **2,037,760** |

Every completed comparison passed. These are **1,018,880 distinct stress input
payloads**, not 2,037,760 independent inputs or routine recoveries. Controls,
baseline training and diagnostic replay are not added to that stress count.
The native-failed batch-1990 attempt remains unknown. Final closure is
**`closed-incomplete`**, **`selection_allowed=false`**, with **zero heldout
evaluations**, source acceptances or promotions. We did not change the frozen
stop rule or force the shortest-source selection just to finish a run.

The same fixed complete-byte recognizers were then assessed against **294
exported `FUN_*.s` routine entries** (separate `entry.s` excluded; this is not
the 295-entry ledger denominator). Only existing **4905 fill** and **3b22
shortstring** matched: **zero new supported entries**. No model request or
new original-execution transfer trial was made, and no new decoder/grammar
rule was invented to turn that eligibility result into success.

Six mapping/relocation blockers were explicit:

- `FUN_1000_01a1`: MZ relocation overlaps exported-entry boundary.
- `FUN_24dd_0000`, `FUN_24dd_0116`, `FUN_24dd_3639`: relocated operands outside
  the fixed leaf probe's supported scope.
- `FUN_2971_65df`, `FUN_2971_67f6`: exported ranges outside the file-backed image.

Other entries lie outside the frozen complete-byte vocabulary. These blockers
are not inferred semantic contracts or a claim that those routines can never
be recovered. The first two assessor runs exposed boundary/non-file-backed
conditions; their failed freezes and explicit errors remain preserved.

Session artifacts:

- `liero-crash-diagnostics-20261102/`: diagnostic freeze, four worker logs and
  original/Pascal results; no heldout.
- `liero-overnight-closure-final-20261102/`: complete report hashes, reconciler
  snapshot, native-failed attempt reference and closed-incomplete result.
- `liero-frozen-sketch-transfer-final-20261102/`: export/rule/method freeze,
  per-entry eligibility and explicit unsupported reasons.

Reconciliation and eligibility are available in the existing narrow supervisor:

```sh
uv run python tools/liero_overnight_resume.py --prior OLD_RUN \
  --reconcile-continuation CONTINUATION --output NEW_CLOSURE
uv run python tools/liero_overnight_resume.py --prior OLD_RUN \
  --assess-transfer --output NEW_ELIGIBILITY
```

Validation: **350 focused tests** pass, plus Ruff/format/syntax/whitespace
checks. Original frozen pilot/rule/scheduler files were not edited by this
closure. No ledger review was renewed, source installed or example promoted.

**Next at that checkpoint (superseded by the contract above):** establish one new scoped contract from bytes/callers, or work on
the unresolved 492c caller/return/aliasing evidence. Freeze any resulting rule
change separately before transfer. Do not retry unknown outcomes/holdouts,
restart unchanged overnight loop testing or call rule-development results
unseen transfer. This is a fixed-method frontier, not whole-project saturation.

### 2026-11-01: partial memory projection and evidence reconciliation

The shared byte rules can now render a disposable Pascal **memory-effect
projection** for bounded constant entry-DS word stores. This is useful partial
source work, not exact historical structure or a recovered whole routine.
The renderer uses shared write facts, not the existing manual 492c body.

- For `FUN_24dd_492c`, generated Pascal matches the original DOSBox trace on
  all **8192 observed bytes per seed**, with seeds A5h, 5Ah and FFh.
  Each checks 5932 cleared bytes and 2260 preserved guard bytes. These are the
  already used original contexts, now compared with generated Pascal; they are
  not three new independent routine experiments.
- The data window remains the conditional entry-DS range `[6000h,8000h)`.
  Original SP before/after remains a separate original-only observation.
  Host FPC `-Mtp -Cr` checks compilation/range safety, not TP7 ABI parity.
- The 17-byte decoded prefix retains original suffix `C3` at offset 17.
  The Pascal procedure implements only memory writes; registers, flags,
  segment-stack and return behavior are not translated. Whole-routine
  execution and training promotion are explicitly blocked in its metadata.
- The static report, original bytes/listing, rule snapshot, Pascal source,
  renderer hash, write-support offsets and exact residue are revalidated.
  Modified source/metadata or changed dependencies cannot replay as current.
  No target include, recovery attestation or training example was changed.

Validation: **237 focused regression tests passed** across instruction facts,
pilot, repeated-frontier scheduling, constructor, close and read probes; changed Python files pass Ruff,
formatting and syntax checks. The three distinct archived Pascal/original
measurements replay with matching artifact hashes. Resolve pytest `current`
symlinks before counting directories; aliases are not additional measurements.

Reproduce in a **new** experiment directory:

```sh
uv run python tools/liero_four_routine_pilot.py \
  --output targets/liero/build/partial-memory-492c \
  --prefix-transfer-routine FUN_24dd_492c \
  --prefix-data-window 0x6000 0x8000 --partial-memory-source
```

Exit 1 is intentional because the prefix still has unsupported residue.
`partial-memory.inc` is a slice-harness include, not an implementation of
`FUN_24dd_492c`; the original assembly remains separate. Replay via
`validate_partial_memory_source(root, output)` in the existing pilot module.

The live audit still has 295 entries, 25 valid source recoveries (8.47%),
two scoped routine entries sharing coupled copy evidence, four invalid scoped
reports and one stale source review. The new projection does not change those
counts. The named discrepancies were reproduced, not silently repaired:

| Historical report/review | Current rejection |
| --- | --- |
| constructor `3c8598a25dba4789a9549fdf46062090` | stale constructor source/evidence |
| constructor `a342abda4f7c4aa2a9b70377451c73f3` | unrecognized constructor differential contract |
| constructor `f4815af1d734415a9b49172bcde0b622` | stale constructor source/evidence |
| comparator `FUN_24dd_3f86-9cases` | stale source/evidence under the current validator |
| comparator source review | Pascal source changed since review |

Caller inspection found an important listing discrepancy. Original startup
bytes at file offset 91456 begin `BA 71 19 8E DA`; actual MZ relocation is at
routine offset 1. They set DX to relocated logical 2971h and execute
**MOV DS,DX**, not the listing's `MOV DX,DS`. Bytes `E8 1E 49` at startup
offset 0Bh call near offset 492Ch. This narrows the entry/return topology,
but does not establish an original-program writable/nonaliasing allocation
or full ABI. The test's DS=CS context must not be substituted for startup DS.
Binary SHA256 remains
`e45653ab0f915238f7394b2846b70288d0cc35a2595debc2a49502078398c7d1`;
startup bytes SHA256 is
`8f3b8cff731f85dd57115b4029d98391ee253b359118e4fba05d25cc72f33a87`.

### Controlled new leaves and measured low-yield stop

The initial dispatch/oracle blocker was resolved without modifying target bodies.
The existing pilot now has independently executable leaf-memory probes for
4905 (20 original bytes) and 3b22 (59 original bytes). Both are callee-free;
their complete original bytes are checked against the BYOD image, with no
relocated operands accepted by this probe. A far-call COM harness compares
the entire 544-byte source/guarded-object arena and records original DS/SS/SP.

Positive controls are **manually supplied reference implementations**, not
model passes. They pass 514 training cases for 4905 and 512 for 3b22. Training
uses dirty seeds 00h/FFh; held-out definitions use A5h, plus embedded NUL cases
for 3b22. Those corpora are byte-disjoint, but finite and related: they are not
an independent held-out-project benchmark. Controls and model sources remain
separate; no existing manual target include is read into model prompts.

| Frozen strategy | Actual model outcome | Stop |
| --- | --- | --- |
| Original bytes/disassembly and declared host interfaces | **0/2** scoped passes: 3b22 emitted invalid labels, a compiling placeholder and a duplicate; 4905 repeatedly emitted forbidden inline assembly | 0% yield; stop expansion |
| Added byte-derived fill/initialization constraints, same leaves and model | **0/2**: 3b22 produced runtime 103/201 failures and wrong guarded memory; 4905 produced unsupported `for var` syntax and then the identical source | Budget/duplicate exhaustion; 0% yield; stop expansion |

The constrained strategy is changed-method debugging on the failed panel, not
unseen-routine generalization. A shared exact byte-fill shape reader derives
argument slots, CLD/REP STOSB effects and encoded far-return cleanup from bytes.
Varied stack-slot fixtures and opcode/direction/layout/return mutants test it.
Its caller bounds remain obligations; the generic prefix decoder still does
not accept RET or translate the unresolved 492c suffix. For 3b22, existing
shared prefix writes are provided as constraints; the string suffix remains
a hypothesis until execution checks it.

The first constrained candidate compiled but failed host execution. The
initial runner incorrectly aborted instead of recording that training rejection.
This was fixed with explicit runtime diagnostics and a 30-second execution
limit. The interrupted request was replayed, not requested anew; 3b22's
original four-request cap remained four across continuation. 4905 stopped
after its second, duplicate request. Failed method/rule/scheduler snapshots,
raw outputs, compiler/runtime failures and training counterexamples remain
archived; no historical failure was relabeled as success.

**No candidate in either live strategy reached held-out evaluation.** Holdouts
remain unused and were not fed back. The scripted test that intentionally fails
only on held-out data is a mechanism test, not another live-model experiment.
No source attestation, target installation, training promotion or verified
neighbor/caller resolution follows from these failed proposals.

The bounded frontier helper now distinguishes request-budget exhaustion and
terminal held-out outcomes from evidence-relative saturation. The measured
historical helper initially labeled exhausted attempts as frontier saturation;
that classification was corrected and regression-tested, without editing the
saved runs. Top-level measured stop is **low yield**, not whole-puzzle
saturation. Empty or unknown model-request outcomes cannot be silently refunded
on resume; resumption also rejects any prior held-out evaluation.

Reproduce only as a separately recorded run, not an unchanged retry for progress:

```sh
uv run python tools/liero_four_routine_pilot.py --leaf-trials \
  --leaf-byte-constraints --model qwen2.5-coder:14b-instruct \
  --output targets/liero/build/frozen-leaf-trial
```

The local model digest, byte/probe/scheduler/tool identities, manual topology,
corpus hashes, maximum four requests, source deduplication and training-only
selection are frozen before requests. A first training-passing unique candidate
would receive exactly one terminal held-out evaluation, with no feedback retry.
Failed runs exit 1. `validate_leaf_probe(root, output)` rederives completed
control/training comparisons; changed method/evidence makes a current replay
stale. Historical replay must use its trusted frozen method identities.

### Restricted 4905 fill synthesis: known-slice mechanism pass

The next bounded changed-strategy run replaces model executable text with a
closed five-field JSON fill sketch in the existing pilot. Shared code renders
`for`/`while` Pascal using declared `LongInt` indices and signed count endpoints.
Zero count executes no writes, with or without an explicit guard. Exact original
byte-derived argument/effect constraints reject wrong starting indices, inclusive
endpoints or constant-zero stores; no semantic field is silently repaired.
The model chooses equivalent loop syntax, not unknown fill semantics.

One fresh local `qwen2.5-coder:14b-instruct` run selected `for`, zero guard,
first index 0, `count_minus_one`, input `value`, on **request 1 of at most 4**.
It passed **514/514 training and the single terminal 257/257 holdout**, checking
all 544 source/guard/destination bytes per case against actual original code.
Training uses seeds 00h/FFh, holdout A5h, each with counts 0..256. These are
finite related within-routine cases, not held-out-project generalization.
The manually supplied positive control remains separate.

- Archive: session files `liero-fill-sketch-frozen-20261101`, retaining the
  freeze, exact schema/topology disclosure, method/rule/scheduler snapshots,
  raw JSON, rendered source and original/Pascal/control measurements.
- Local model digest:
  `9ec8897f747e246e970bc5cfdda85d22f1123dc2e3d34978a010a75968716849`.
- Selected source SHA256:
  `bdf3cef33e2f2260405b2205c69ddb2387cc9aef76e32562954045dc4d3e22dd`.
- Replay with `validate_fill_sketch_trial(root, output)` binds the selected
  sketch to the raw response, exact rendering and training/held-out traces.
  Tampered sketches are rejected. Restricted mode requires a fresh freeze;
  incompatible/resumed source-text runs are refused.
- **254 focused tests** pass, with Ruff/formatting/whitespace checks. Tests
  cover both loop forms, optional zero guard, dirty memory/count boundaries,
  typed/injection rejection, static conflicts, terminal selection and replay.
  Scripted workflow tests are mechanism tests, not additional live trials.

Reproduce only as a new recorded mechanism evaluation:

```sh
uv run python tools/liero_four_routine_pilot.py --leaf-trials \
  --leaf-byte-constraints --leaf-fill-sketch \
  --model qwen2.5-coder:14b-instruct \
  --output targets/liero/build/frozen-fill-sketch
```

This resolves the demonstrated 4905 syntax bottleneck, not original Pascal
structure, full ABI, normal-program pointer/allocation provenance or weight
learning. The result explicitly reports **zero new recoveries**, zero promoted
examples and `expansion_allowed=false`. The two earlier live strategies remain
0/2 failures. The passing sketch does not enter the new-routine yield numerator
or renew stale reviews. Older pilot-bound artifacts require their frozen
methods; this run is not a renewed current-method replay of the 492c reports.

### 3b22 byte-derived composition prerequisite

The existing instruction-facts module now recognizes the complete 59-byte
zero-mode initialization/shortstring shape. This is a developer-authored
recognizer on a manually known slice, not learned or unseen-routine recovery.
It reuses the conservative prefix facts and requires exact opcodes and
relative branches while reading supported constants from original operands.
For current 3b22 bytes at file offset **106594**, it derives:

- Destination/source far pointers from entry SS:SP slots **8/4**.
- Destination word 0 = zero, word 2 = D7B0h, then **22 zero words** at
  offsets 4..47; text starts at offset **48**.
- Source byte 0 is unsigned length; copy at most **min(length,79)** nonzero
  bytes starting at source offset 1, stop before first NUL and append one NUL.
  Bytes beyond those ordered writes remain untouched.
- The branch at routine offset **33** cannot be taken: entry `XOR DX,DX`
  sets DX to zero and no intervening instruction changes it. The loop tests
  and branch displacements remain exact, not inferred from a listing.
- Original `POP DS` and `RETF 8` are part of the recognized shape. This
  does not translate or certify host Pascal register/segment/stack/return ABI.

Preconditions explicitly require disjoint nonwrapping source, destination and
stack argument/return allocations, a valid 256-byte initialization window and
destination space through the maximum terminator. These are scoped harness
conditions, not established normal-program object provenance. Alternate
argument-slot experiments failed the shared prefix decoder; the implementation
retains 8/4 rather than guessing bindings or weakening that gate.

Predictions agree with original-byte DOSBox execution on all **544 memory
bytes per case** across **584 training cases**: the prior 512 dirty-seed/
length contexts plus 72 NUL/length boundary contexts on seeds 00h/FFh.
The Pascal program is a disclosed manual positive control. No model request,
model-heldout evaluation, new recovery, installation or promotion occurred.
Source/guards are unmasked; replay checks predicted, original and control
memory separately. Reusing prior training contexts is not independent evidence.

The saved `composition-contract.json`, input/trace/control hashes and frozen
rule/pilot/test snapshots are under session files
`liero-string-contract-final-20261101/test_shortstring_composition_p0/composition`.
The earlier failed alternate-slot test output is retained separately under
`liero-string-contract-check-20261101`.
Validation: **314 focused tests** pass, including opcode/branch/mode mutants,
varied supported constants/counts/limits, invalid argument/window rejection
and scripted frozen-prompt/contract-tampering checks. The existing constrained
pilot now supplies this entire contract, not just a prefix plus unknown suffix.
Freeze replay recomputes the contract from its bound original bytes.

Pilot/rule edits invalidate earlier current-method replays, including the
4905 sketch run; those outcomes remain historical under trusted frozen methods.
None of this renews stale ledger reports or changes source-acceptance counts.

Next **do not expand toward five or ten passes**. Extend the existing typed
sketch vocabulary to checked initialization/string composition, then freeze
one known-slice 3b22 synthesis run without inserting its manual body. Keep the
separate 492c caller/segment/aliasing/ABI gap explicit. Propagate only compatible
scoped constraints and reconsider leftovers under unchanged acceptance rules.

### Prepared unattended 3b22 optimization protocol

The existing pilot now has typed prefix/string rendering and one supplied
loop-flip operator (`for` versus `while`). Both forms compile under host
FPC `-Mtp -Cr` and pass guarded original-byte regression checks. Semantic
fields contradicting the byte contract and executable model text are rejected,
not repaired. This remains known-slice topology, not unseen algorithm recovery.

For the requested overnight run:

- Freeze the actual local model/tool/method/rule identities before proposals.
  At most four model requests are available; after the first training-passing
  sketch, compare it and its deterministic loop-flip neighbor. No model sweep.
- Compare eligible candidates on the **same** 512 seeded training inputs per
  batch. Source lengths cover 0..255, NUL positions cover 0/1/77/78/79/254 and
  no NUL, with varied nonzero text and dirty source/object/guards. A batch/index
  tag in preserved guard bytes guarantees distinct input payloads; heldout
  payloads are excluded without inspecting their outcomes.
- Check all 544 bytes per candidate/case against original execution, actual
  compiled Pascal and the independent memory specification. Preserve failures
  and remove failed candidates. At most 4096 batches = **2,097,152 distinct
  training inputs**, potentially 4,194,304 candidate-case comparisons.
- Stop stress testing at coverage completion, eight stress hours, 16 GiB
  artifacts, less than 2 GiB free disk, or no eligible candidate. Serial
  low-priority execution and an external nine-hour hard process limit bound
  shared-machine use; completion may occur early, not through filler retries.
- Select only a candidate passing every measured training check, using shorter
  source then SHA256 as a reproducible tie-break. This ranking is not evidence
  of original Pascal fidelity. Only the selected candidate gets **one terminal
  264-case holdout**, with no feedback-driven alternate selection.
- Atomic `progress.json`, `search.json`, final `result.json` or explicit
  `failure.json`, logs and per-batch traces retain the outcome. Infrastructure
  and resource failure cannot claim successful source recovery. No target
  installation, ledger renewal, example promotion or frontier expansion.

Run directory for this launch:
session files `liero-overnight-optimisation-20261101`; its sibling `.log`
captures startup/progress/final output. **Prepared/running is not a measured
pass.** Read final reports and replay relevant leaf traces before using results.
Do not mutate the bound pilot/rules/scheduler/tools during execution.

Launch verification confirmed the persistent detached process is running;
its first matched batch completed **512 distinct inputs / 1024 candidate-case
comparisons**, with both candidates still eligible after baseline training.
Shell handle: `liero-overnight-optimisation`. These initial observations are
not the final run outcome or heldout evaluation.

Pre-launch validation: **337 focused tests**, Ruff/format/syntax/whitespace
checks pass. A scripted five-second end-to-end test generated no live model
requests, compiled both loop forms, replayed three matched original/Pascal
batches (3072 candidate-case comparisons), and completed one 264-case terminal
holdout. It is explicitly workflow evidence, not a model recovery pass.
Its separate archive is `liero-overnight-scripted-smoke-20261101`.

```sh
uv run python -u tools/liero_four_routine_pilot.py --leaf-trials \
  --leaf-byte-constraints --leaf-string-sketch --optimise-loop-search \
  --overnight-hours 8 --model qwen2.5-coder:14b-instruct \
  --output targets/liero/build/overnight-composition
```

### Overnight lifecycle correction (2026-11-02)

The original overnight process stopped with **exit 139** after roughly
2161 stress seconds, not coverage/time-budget completion. Both candidate
batch-01105 directories contain complete reports, while the last search
checkpoint records only 1105 completed matched batches; those additional
reports must be replayed before counting them. No holdout directory exists.
Native failure is inferred from the exit status; exact process/cause is not
established, and no diagnostic traceback/core was available. Disk remained
well above the free-space floor.

Original progress is now explicitly interrupted; its previous bytes are kept
as `progress-at-crash.json`, and `interruption.json` records the diagnosis.
The new bounded continuation does not modify frozen source/rules or retry
unknown outcomes. `tools/liero_overnight_resume.py` authenticates and replays
the contiguous old evidence, then uses a fresh Python worker with faulthandler
per original/Pascal comparison. Worker crashes/timeouts are terminal explicit
errors with diagnostic logs, not training success or silently refunded attempts.
The wrapper records native supervisor termination too.

Original model/candidates/corpora/ranking/coverage remain fixed; no new model
request is issued. Remaining stress time is debited by the stale heartbeat's
elapsed time plus 180 seconds for an in-flight worker. Coverage remains 4096
batches, artifact use includes the old run under the same 16-GiB ceiling, and
the free-space floor remains 2 GiB. One selected terminal holdout remains the
only heldout evaluation; a permanent exclusive continuation claim blocks
duplicate resumes. Incomplete/unknown batches block continuation for review.

Continuation directory: session files
`liero-overnight-optimisation-resumed-20261102`, plus sibling `.log`.
Replay is not new independent support. **346 focused tests** pass, including
signal-error reporting, frozen-history validation, preserved budgets,
incomplete-batch rejection, duplicate-resume exclusion and terminal holdout.
A real isolated 16-case worker smoke check passed without model/holdout calls.

Continuation launch was then verified: both candidates' **1106 completed
batches** replayed successfully (**1,132,544 historical candidate-case
comparisons**), and one new matched batch completed **1024 fresh comparisons**.
The detached supervisor handle is `liero-overnight-supervised`; its process
liveness was checked. The remaining stress budget is **26,458.6 seconds**,
not a refunded eight hours. No new model requests or holdout evaluation.
This is a resumed running observation, not a final pass or a diagnosis of the
original native crash's underlying cause.

### Previous shared-rule checkpoint

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
