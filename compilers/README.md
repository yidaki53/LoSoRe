# Pinned original toolchains — one Dockerfile per target. BYOD license: compilers themselves are abandonware/licensed; Dockerfiles reference user-supplied media, never commit binaries.
- Dockerfile.msvc42 — Win9x/DOS-Win (LEGO Island pattern: isledecomp/isle). Needs user MSVC 4.2 media.
- Dockerfile.watcom — DOS (Liero/OMF/Jazz hypothesis: Open Watcom 1.9 as proxy, verify vs period Watcom 10.x strings).
- Dockerfile.djgpp — DOS free (Slicks/Scorched fallback).
- Dockerfile.psx — PS1 (gcc 2.7.2 + maspsx + splat pattern per open-spyro).
Usage: `docker build -f compilers/Dockerfile.<tgt> -t rev:<tgt> compilers/` then `engine/verify.py` invokes `docker run`.
