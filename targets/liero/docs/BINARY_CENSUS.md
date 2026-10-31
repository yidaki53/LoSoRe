# Liero executable census

## Initial measured baseline

The census compares the BYOD MZ load image to the routine metadata and decoded
Ghidra assembly listings. Run it from the repository root with:

```sh
make binary-census TARGET=liero
```

The full machine-readable output is written to
`reports/liero-binary-census.json`. The census uses Ghidra's metadata `size` as
an approximate function span and includes a span in the byte-coverage total
only when its assembly listing contains decoded instructions and its address
maps into the file-backed MZ image.
The report also records per-function CFG summaries, direct call targets that
resolve to exported entries, absolute memory operands, and instruction-count
or entry-address mismatches. It does not infer a semantic label for those
operands or claim that all indirect calls/data references have been recovered.

The current executable is 135,856 bytes with SHA-256
`e45653ab0f915238f7394b2846b70288d0cc35a2595debc2a49502078398c7d1`. Its MZ
header declares a 6,000-byte header and a 129,856-byte load image, including
1,492 relocation entries, all within the file-backed load image. Its minimum
additional allocation is 71,456 bytes. The metadata entry point agrees with
the executable header's initial IP when mapped using Ghidra's inferred load
segment `0x1000`.

The exported inventory has 295 routines and 295 assembly files. Two entries
(`FUN_2971_65df` and `FUN_2971_67f6`) have no decoded instructions and map to
the minimum-allocated, uninitialized MZ tail rather than file-backed bytes.
They are retained as unresolved exports, not treated as executable code.
One additional listing (`FUN_24dd_3249`) has the expected 82 decoded
instructions, but its first listed address is `24dd:3202`, not the metadata
entry `24dd:3249`; its span is excluded from evidence-backed byte coverage
until the export discrepancy is reviewed. Among the remaining 292 routine
spans, the union covers 91,899 bytes (70.77%) of the load image. The other
37,957 bytes (29.23%) are in 80 unclassified ranges. One pair of metadata
spans overlaps by 10 bytes. These are leads for further analysis, not a finding
that the complement is code or that the current routine boundaries are
correct.

The census output deliberately labels the complement *unclassified*. A full
census still needs instruction/data classification, cross-references into
gaps, overlay or runtime-generated-code analysis, and review of the two empty
exports. MZ `minalloc` means memory may exist beyond the file-backed image; it
does not supply bytes for those addresses.

For this binary hash, the report contains 1,816 direct call edges: 1,813
resolve to exported routine entries, one additional target falls within the
approximate `entry` span, and two targets are outside the file-backed image.
Twelve indirect or non-literal call instructions have no statically recovered
target. No statically resolved direct call targets an unclassified file-backed
range; this does not rule out indirect control flow into those ranges.

## Verification environment at the initial census

This list is historical readiness evidence, not the current oracle inventory.
Subsequent original-byte DOSBox routine probes now produce guarded-memory,
DOS-service and stack observations; normal-gameplay/full-executable parity
is still not established. The latest shared global-rule checks passed
three original-only 8192-byte comparisons, not Pascal or complete ABI parity.
See [current reconstruction status](RECONSTRUCTION.md) and
[recovery TODOs](../../../docs/RECOVERY_TODO.md). This documentation update
does not rerun the census or revise its coverage numbers.

- BYOD format: DOS MZ executable; the on-disk length matches the MZ-declared
  length.
- `fpc` is available locally at version 3.2.2. The target build uses Free
  Pascal's `-Mtp` compatibility mode, not the historical Borland compiler.
- DOSBox 0.74-3 accepts scripted DOS commands and can write to a mounted
  temporary directory. Launching the copied game under the dummy video driver
  stayed active until an 8-second timeout; this did not establish that it
  reached gameplay or provide routine-level input/output observations.
- The tested environment had no available keyboard automation or screen
  capture utility, so DOSBox is not yet a usable behavioral oracle here.
- Java is available, but `ghidra`/`ghidraRun` are not on `PATH` and
  `LSR_GHIDRA` is unset. The existing Ghidra exports can be audited, but this
  environment cannot currently regenerate them.
- The project identifies Turbo Pascal 7 as the likely original compiler, but
  exact TP7 binary matching is not presently demonstrated. Compile success
  under FPC remains a compatibility check only.

## Next census work

1. Reconcile decoded instructions with raw file offsets and relocation sites;
   preserve address mapping assumptions in the generated report.
2. Analyze all unclassified ranges with executable-aware disassembly and data
   references. Keep undecided ranges visible with a reason and evidence link.
3. Investigate empty Ghidra exports separately from file-backed routine
   coverage; do not silently delete them from the ledger.
4. Add P-Code/dataflow evidence when Ghidra is available; keep it distinct from
   the current disassembly-derived CFG, call, and absolute-operand summaries.
5. If Ghidra becomes available, regenerate exports and compare the result
   against this immutable binary hash before updating the function inventory.
