/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0e4a
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_1ec2_0e4a(uint16_t param_1, int param_2, int param_3, void *param_4) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    uint16_t *puVar3;
    uint16_t uVar4;
    uint8_t bVar5;

    if (((-1 < param_3) && (param_3 < 0x9e)) && (-1 < param_2) && (param_2 < 0x9e)) {
        uVar4 = (uint16_t)((uintptr_t)param_4 >> 16);
        puVar1 = (uint16_t *)((uintptr_t)param_4 + param_2 * 0x140 + param_3);
        bVar5 = *puVar1;
        if ((0x9f < bVar5) && (bVar5 < 0xa4)) {
            puVar2 = (uint16_t *)((uintptr_t)param_4 + param_2 * 0x140 + param_3 + param_4);
            puVar3 = (uint16_t *)((uintptr_t)param_4 + param_2 * 0x140 + param_3 + 1);
            *puVar2 = (uint8_t)((uint8_t)*puVar3 + 4);
        }
    }
    return;
}
