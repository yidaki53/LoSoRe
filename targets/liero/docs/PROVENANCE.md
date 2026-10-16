# liero provenance (P0 findings 2026-10-10, BYOD confirmed 2026-10-11)
- Version: v1.33 freeware by MetsänEläimet (Joosa Riekkinen), 1998-1999
- License: "The source code of this game is not distributed freely" [liero.be] -> source-lost CONFIRMED
- Language: Turbo Pascal 7, 16-bit real-mode DOS (CRT unit bug / runtime error 200 in changelog; 560kB conventional mem, no extender)
- EXE set: LIERO.EXE, KEYSETUP.EXE, LEVEDIT.EXE + LIERO.CHR/SND, NAMES.DAT
- Compiler ID (confirmed via strings): "Portions Copyright (c) 1983,92 Borland" + "Runtime error" -> Borland Pascal RTL = TP7
- BYOD source: Internet Archive item `lierodos` -> liero133.zip (LIERO.EXE sha1 514511ffcdbefa6f...)
- Recreations (NOT source): gliptic/liero, openliero/openliero
- Format docs: liero.nl/lierohack DAT spec; openliero tctool as clean-room format reference
- BYOD: extracted/liero/ (gitignored); Oracle plan: format parity -> behavioral trace -> byte-exact if TP7 RTL found

## Two archives are byte-identical (2026-10-11)
- `lierov133winxp.zip` and `Liero_DOS_EN_v133.zip` both contain the SAME DOS v1.33
  binary: liero.exe sha1=514511ffcdbefa6f3e8842d91cd37c00ef234662 (CHR/SND/NAMES also match).
- The "winxp" archive = same MZ DOS exe + WINXP.BAT launcher + LIERO.DAT/OPT wrapper.
- => ONE code binary; kept as two targets (liero, liero-dos) as a parity/oracle test.

## Ghidra ingest (2026-10-11)
- Toolchain: Ghidra 12.1.4 headless, JDK 25 (or JDK 21 with JAVA_HOME_OVERRIDE),
  post-script tools/ghidra/ExportFuncs.java (Java, not PyGhidra — no jpype for py3.14).
- Processor: x86:LE:16:Real Mode. Result: 295 functions, image base 0000:0000.
- Real TP7 signatures: __cdecl16near/far, __stdcall16near/far; heavy CALLF (far calls).
- Outputs: targets/liero/{asm,decomp}/ (295 each) + functions.json; learn.py mined
  toolchain recipe + few-shot examples into knowledge/knowledge.json.

<!-- BEGIN AUTO (tools/provenance.py) -->
- files: 12
- detected toolchain: turbo-pascal-7 (high), language=pascal, platform=dos
- LIEROENG.TXT: sha1=d1d5ecba8d18f36c compiler~borland-rtl
- LIERO.TXT: sha1=87bfe42023f455b9 compiler~borland-rtl
- WINXP.BAT: sha1=8adb05de9c5ca8d6 compiler~unknown
- LIERO.DAT: sha1=11746b9fe8c9d17d compiler~unknown
- LEVEDIT.EXE: sha1=70c71bcd165cd1f4 compiler~turbo-pascal-7,borland-rtl,borland?
- LIERO.OPT: sha1=3e90fb1095f951c6 compiler~unknown
- LIERO.CHR: sha1=2fb9f4f3c33440be compiler~unknown
- LIERO.EXE: sha1=514511ffcdbefa6f compiler~turbo-pascal-7,borland-rtl,borland?
- FILE_ID.DIZ: sha1=c2b28596106714e2 compiler~unknown
- LICENSE.TXT: sha1=d61602db0e2099cd compiler~unknown
- LIERO.SND: sha1=4d3f7e6d6dc56acb compiler~unknown
- NAMES.DAT: sha1=7c24b0d6e58f27b1 compiler~unknown
<!-- END AUTO -->
