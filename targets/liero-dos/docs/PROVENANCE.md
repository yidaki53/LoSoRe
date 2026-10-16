# liero-dos provenance

Same binary as the `liero` target (see targets/liero/docs/PROVENANCE.md for the full
research). Kept as a second target as a parity/oracle test: two independent ingests
of the byte-identical v1.33 DOS binary must agree.

- kind: game
- Version: Liero v1.33 freeware (MetsänEläimet / Joosa Riekkinen), 1998-1999
- License: source not freely distributed -> source-lost (preservation/BYOD only)
- Compiler (detected, high confidence): Turbo Pascal 7 / Borland Pascal RTL,
  16-bit real-mode DOS. See config/toolchain.yaml for evidence.
- Language: pascal (same-language rebuild policy)
- liero.exe sha1=514511ffcdbefa6f3e8842d91cd37c00ef234662 (identical to liero/LIERO.EXE)
- BYOD: extracted/liero-dos/ (gitignored)
- Oracle: dat-parity (real); byte-exact stretch only with genuine TP7 + identical RTL

<!-- BEGIN AUTO (tools/provenance.py) -->
- files: 7
- detected toolchain: turbo-pascal-7 (high), language=pascal, platform=dos
- liero.chr: sha1=2fb9f4f3c33440be compiler~unknown
- liero.snd: sha1=4d3f7e6d6dc56acb compiler~unknown
- levedit.exe: sha1=70c71bcd165cd1f4 compiler~turbo-pascal-7,borland-rtl,borland?
- lieroeng.txt: sha1=d1d5ecba8d18f36c compiler~borland-rtl
- liero.txt: sha1=87bfe42023f455b9 compiler~borland-rtl
- liero.exe: sha1=514511ffcdbefa6f compiler~turbo-pascal-7,borland-rtl,borland?
- names.dat: sha1=7c24b0d6e58f27b1 compiler~unknown
<!-- END AUTO -->
