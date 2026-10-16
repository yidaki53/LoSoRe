/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_131a
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24cb_0094(uint16_t, uint16_t, uint16_t, uint8_t);

void __cdecl16far FUN_235c_131a(void) {
    uint16_t *ptr1 = (uint16_t *)(0x67dc);
    uint8_t *ptr2 = (uint8_t *)(0x67eb);
    uint16_t *ptr3 = (uint16_t *)(0x67f2);
    uint16_t *ptr4 = (uint16_t *)(0x67f4);
    uint8_t *ptr5 = (uint8_t *)(0x67ec);
    uint8_t *ptr6 = (uint8_t *)(0x67fa);

    uint8_t bVar1 = *ptr1;
    *ptr1 = bVar1 | *ptr2;
    FUN_24cb_0094(*ptr3, *ptr4, *ptr5, *ptr6);
    *ptr6 = 0;
}
