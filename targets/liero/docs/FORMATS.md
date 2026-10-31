# LIERO.CHR graphics format (from liero.nl/lierohack + openliero tctool — clean-room reference, verify against BYOD)
- Palette: VGA 6-bit (0..63 per channel) — cf. DAT spec "range is 0...63d"
- Worm sprites, level tiles, weapon sprites: byte-planar bitmaps; exact layout TODO after BYOD ingest
- Parity test: extract CHR via tools/liero_chr.py → PNG; compare vs openliero tctool output (format parity, not byte match)
# LIERO.SND format: raw samples + index; lierolibre provides replacements; original SND stays BYOD-only
# LIERO.DAT settings format: the file is 155 bytes (0000h-009Ah; 009Bh is
# the exclusive end offset). The current parser models 20 documented bytes;
# the remaining 135 bytes are preserved opaquely. Byte-exact round-trip proves
# preservation only, not that those opaque bytes' semantics are understood.
