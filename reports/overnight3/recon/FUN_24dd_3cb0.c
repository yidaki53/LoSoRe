/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3cb0
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_3cb0(uint16_t param_1, uint16_t param_2, uint16_t *param_3) {
    int iVar1;
    uint16_t uVar2;
    uint16_t *base_address = (uint16_t *)0x4200;

    uVar2 = (uint16_t)((uintptr_t)param_3 >> 16);

    if (*(char *)param_3 == '\0') {
        iVar1 = 0;
        while (true) {
            uVar2 = uVar2 * param_2 + *param_3;
            if (uVar2 < 0x8000) break;
            uVar2 = uVar2 - 0x8000;
            iVar1 = iVar1 + 1;
            param_3 = (uint16_t *)((int)param_3 + 1);
        }
        *(uint16_t *)0x6410 = uVar2;
        return;
    }

    iVar1 = 0;
    while (true) {
        uVar2 = uVar2 * param_2 + *param_3;
        if (uVar2 < 0x8000) break;
        uVar2 = uVar2 - 0x8000;
        iVar1 = iVar1 + 1;
        param_3 = (uint16_t *)((int)param_3 + 1);
    }
    *(uint16_t *)0x6410 = uVar2;
    return;
}
