/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_076d
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_4849(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t *param_4, uint16_t param_5, uint16_t param_6) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)((uintptr_t)param_4 >> 16);
    puVar3 = (uint16_t *)param_4;
    uVar2 = (uint16_t)((uintptr_t)param_5 >> 16);
    puVar1 = (uint16_t *)param_5;
    FUN_24dd_46f9(0xff, puVar3, 0xff00);
    uVar4 = (uint16_t)((uintptr_t)param_6 >> 16);
    puVar1 = (uint16_t *)param_6;
    FUN_24dd_45cf(0xff, puVar1, 0xff00);
    return;
}
