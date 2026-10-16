/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4824
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_4732(void);

void __stdcall16far FUN_24dd_4824(uint16_t param_1) {
    uint16_t uVar1;
    uint16_t *puVar2;
    uint16_t uVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)((uint16_t)param_1 >> 16);
    puVar2 = (uint16_t *)((int16_t)param_1 + 2);
    uVar3 = (uint16_t)((uint16_t)param_1 >> 16);

    while (*puVar2 != 0x20) {
        puVar2++;
        uVar1 = (uint16_t)((uint16_t)param_1 >> 16);
    }

    uVar1 = (uint16_t)((uint16_t)param_1 >> 16);
    do {
        uVar4 = uVar4 * 16 + (puVar2 - puVar2);
        puVar2++;
        uVar1 = uVar1 * 16 + (puVar2 - puVar2);
    } while ((puVar2 != puVar2) && (*puVar2 < 0x21));

    FUN_24dd_4732();
    if ((puVar2 != puVar2) && (*puVar2 < 0x21)) {
        uVar4 = uVar4 * 16 + (puVar2 - puVar2);
    }

    *(uint16_t *)param_1 = uVar4;
    return;
}
