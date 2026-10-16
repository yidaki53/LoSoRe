/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_091d
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_235c_091d(uint8_t param_1);

void FUN_235c_091d(uint8_t param_1) {
    uint16_t iVar1;
    uint8_t *ptr1 = (uint8_t *)(param_1 + 0x67fc);
    uint16_t *ptr2 = (uint16_t *)((uint16_t)param_1 * 10 + 0x6804);

    *ptr1 = 0;
    iVar1 = (uint16_t)param_1 * 10;
    *ptr2 = 0;
    *(ptr2 + 1) = 0;
    *(uint8_t *)(iVar1 + 0x6808) = 0;
    *(uint16_t *)(iVar1 + 0x6809) = 0;
    *(uint16_t *)(iVar1 + 0x680b) = 0;
    *(uint8_t *)(iVar1 + 0x680d) = 0;
}
