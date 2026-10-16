/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_46b1
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_46b1(void) {
    uint16_t *ptr1 = (uint16_t *)(0x6412);
    uint16_t *ptr2 = (uint16_t *)(0x6414);
    uint16_t *ptr3 = (uint16_t *)(0x46e7);

    uint16_t uVar1 = *ptr3;
    uint16_t uVar2 = *ptr1;
    uint16_t uVar3 = *ptr2;

    uint16_t result = ((uint16_t)((uint16_t)uVar1 * 256 + uVar2) * 256 + uVar3) * 256 + *ptr1;

    *ptr1 = result >> 16;
    *ptr2 = result & 0xFFFF;
}
