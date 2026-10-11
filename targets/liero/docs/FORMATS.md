# LIERO.CHR graphics format (from liero.nl/lierohack + openliero tctool — clean-room reference, verify against BYOD)
- Palette: VGA 6-bit (0..63 per channel) — cf. DAT spec "range is 0...63d"
- Worm sprites, level tiles, weapon sprites: byte-planar bitmaps; exact layout TODO after BYOD ingest
- Parity test: extract CHR via tools/liero_chr.py → PNG; compare vs openliero tctool output (format parity, not byte match)
# LIERO.SND format: raw samples + index; lierolibre provides replacements; original SND stays BYOD-only
# LIERO.DAT settings format: fully documented at liero.nl/lierohack/docformats/liero-dat.html (offsets 0000h-009Bh)
