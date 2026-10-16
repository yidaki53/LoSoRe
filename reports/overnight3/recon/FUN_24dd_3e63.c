/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3e63
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_24dd_3e63(uint16_t in_AX, uint16_t in_CX, uint16_t in_DX) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;

    if (*(char *)(0x6420) < 2) {
        for (uVar3 = in_CX & 0x1f; uVar3 != 0; uVar3--) {
            uVar2 = in_DX & 1;
            in_DX >>= 1;
            in_AX = ((uint16_t)(uVar2 != 0) << 15) | (in_AX >> 1);
        }
        return in_AX;
    }
    uVar4 = in_CX & 0x1f;
    in_DX = in_DX >> uVar4;
    in_AX = in_AX >> uVar4;
    return in_AX;
}
