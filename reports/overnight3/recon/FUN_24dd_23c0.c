/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_23c0
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_24dd_23c0(uint16_t in_DX, uint16_t *unaff_SI) {
    uint16_t uVar1 = *unaff_SI;
    uint8_t bVar2 = (uint8_t)(uVar1 >> 8);
    uint16_t result = ((uint16_t)(bVar2 >> 4) * '\n' + (bVar2 & 0xf)) * 10 + (uVar1 >> 4 & 0xf) * 10 + (uVar1 & 0xf);
    return result;
}
