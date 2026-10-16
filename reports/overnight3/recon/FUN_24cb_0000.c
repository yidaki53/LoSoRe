/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24cb_0000
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24cb_0000(uint16_t param_1, uint16_t *param_2) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t uVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    uint16_t uVar9;
    uint16_t uVar10;

    uVar10 = (uint16_t)((uintptr_t)param_2 >> 16);
    puVar3 = (uint16_t *)param_2;
    uVar7 = (uint16_t)((uintptr_t)param_1 >> 16);
    puVar5 = (uint16_t *)param_1;
    uVar6 = *param_2;
    if (0x4e < uVar6) {
        uVar6 = 0x4f;
    }
    uVar8 = (uint16_t)(uint16_t)uVar6;
    puVar1 = puVar5;
    while (uVar8 != 0) {
        uVar9 = (uint16_t)(uint16_t)*puVar3;
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        uVar8 = uVar8 - 1;
        *puVar1 = uVar9;
    }
    *puVar5 = 0;
    uVar10 = 0x21;
    ((void (*)())uVar10)();
    uVar10 = 0x21;
    ((void (*)())uVar10)();
    return;
}
