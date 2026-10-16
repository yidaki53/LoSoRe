/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3d80
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint32_t FUN_24dd_3d80(uint16_t in_AX, uint16_t in_DX, uint16_t in_BX, uint16_t in_CX) {
    uint32_t uVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;

    if (*(char *)(0x6420) < 2) {
        uVar4 = (uint32_t)(in_AX >> 16);
        uVar1 = (uint32_t)in_AX;
        uVar3 = (uint32_t)in_BX;
        uVar2 = (uint32_t)in_CX;
        return ((uint32_t)(uVar4 * uVar3) << 16) | (uVar1 * uVar3 + uVar2 * uVar4) << 16 | uVar1 * uVar2;
    }
    uVar4 = (uint32_t)(in_AX >> 16);
    uVar1 = (uint32_t)in_AX;
    uVar3 = (uint32_t)in_BX;
    uVar2 = (uint32_t)in_CX;
    return ((uint32_t)(uVar4 * uVar3) << 16) | (uVar1 * uVar3 + uVar2 * uVar4) << 16 | uVar1 * uVar2;
}
