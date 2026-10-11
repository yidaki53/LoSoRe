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

<!-- BEGIN AUTO (tools/provenance.py) -->
- files: 8
- LIERO.EXE: sha1=514511ffcdbefa6f compiler~borland?
- LEVEDIT.EXE: sha1=70c71bcd165cd1f4 compiler~borland?
- LIERO.SND: sha1=4d3f7e6d6dc56acb compiler~unknown
- NAMES.DAT: sha1=e89103b88a53381f compiler~unknown
- LIERO.CHR: sha1=2fb9f4f3c33440be compiler~unknown
- FILE_ID.DIZ: sha1=c2b28596106714e2 compiler~unknown
- LIERO.TXT: sha1=87bfe42023f455b9 compiler~unknown
- LIEROENG.TXT: sha1=d1d5ecba8d18f36c compiler~unknown
<!-- END AUTO -->
