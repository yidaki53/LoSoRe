/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3711
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_374d(void);

void FUN_24dd_3711(uint32_t param_1) {
    int iVar1;
    uint16_t uVar2;
    uint16_t *ptr;

    uVar2 = (uint16_t)(param_1 >> 16);
    iVar1 = (int)param_1;
    ptr = (uint16_t *)(iVar1 + 2);

    if (*ptr != (int16_t)-0x284f) {
        if (*ptr != (int16_t)-0x284e) {
            *(uint16_t *)0x6410 = 0x67;
            return;
        }
        FUN_24dd_374d();
    }
    FUN_24dd_374d();
    *ptr = 0xd7b0;
}
