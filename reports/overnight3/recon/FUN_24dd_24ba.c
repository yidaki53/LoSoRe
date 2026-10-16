/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_24ba
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_24dd_24ba(uint16_t in_AX, uint16_t in_DX, uint16_t *unaff_DI) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t bVar3;

    bVar3 = (uint8_t)(in_DX / 100);
    bVar2 = (uint8_t)(in_DX % 100);
    bVar1 = bVar3 % 10;
    bVar3 = (bVar3 / 10 << 4) | bVar1;
    *unaff_DI = ((uint16_t)bVar3 << 16) | bVar2;
    return ((uint16_t)bVar3 << 16) | bVar2 | in_AX;
}
