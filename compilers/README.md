# Original toolchains and compatibility proxies

Docker recipes are not proof that the original compiler is being used.
Historical proprietary compilers require lawful user-supplied media;
never commit compiler binaries or assume an "abandonware" label grants a
license.

- [Dockerfile.dos-tp7](Dockerfile.dos-tp7) is the current Liero path:
  Free Pascal with `-Mtp`, not Borland TP7 or an exact DOS cross-compiler.
  FPC compilation checks compatibility; separate DOSBox probes execute
  original routine bytes. Installing both in one image does not make an
  FPC candidate ABI-equivalent to the original.
- Dockerfile.msvc42 — Win9x/DOS-Win (LEGO Island pattern: isledecomp/isle). Needs user MSVC 4.2 media.
- Dockerfile.watcom — DOS Open Watcom proxy; the earlier Liero/OMF/Jazz hypothesis is not the current Pascal recovery path.
- Dockerfile.djgpp — DOS free (Slicks/Scorched fallback).
- Dockerfile.psx — PS1 (gcc 2.7.2 + maspsx + splat pattern per open-spyro).
Usage: `docker build -f compilers/Dockerfile.<tgt> -t rev:<tgt> compilers/` then `engine/verify.py` invokes `docker run`.

Exact binary matching would require the evidenced original compiler/RTL
and build conditions. Do not migrate toolchains without a demonstrated
blocker in the active slice. See [oracle distinctions](../docs/ORACLES.md)
and [current recovery TODOs](../docs/RECOVERY_TODO.md).
