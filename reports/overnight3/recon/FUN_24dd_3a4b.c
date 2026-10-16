/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3a4b
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_3a4b(uint16_t param_1, int param_2, uint16_t *param_3) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)((uintptr_t)param_3 >> 16);
    puVar3 = (uint16_t *)param_3;
    FUN_24dd_3866();
    uVar2 = (uint16_t)((uintptr_t)puVar3 >> 16);
    puVar1 = puVar3;
    if (param_2 < 0) {
        param_2 = -param_2;
        puVar1 = puVar3 + param_2;
    }
    FUN_24dd_38b9(uVar4, puVar1, uVar2);
    return;
}
