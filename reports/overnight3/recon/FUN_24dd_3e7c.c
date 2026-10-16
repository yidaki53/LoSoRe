/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3e7c
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_24dd_3e7c(uint16_t in_AX, uint16_t in_CX) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;

    if (*(char *)(0x6420) < 2) {
        for (uVar3 = in_CX & 0x1f; uVar3 != 0; uVar3--) {
            uVar2 = in_AX & 1;
            in_AX = in_AX >> 1;
            uVar1 = uVar2;
        }
    } else {
        uVar1 = 0;
    }

    return in_AX | (uint16_t)uVar1 << 16;
}
