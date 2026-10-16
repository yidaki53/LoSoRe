/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_04bc
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_48cf(uint16_t, uint16_t, uint8_t, uint16_t);

void __stdcall16far FUN_235c_04bc(uint16_t param_1, uint8_t *param_2) {
    uint8_t *pbVar1;
    uint32_t uVar2;
    uint8_t *pbVar3;
    uint8_t local_102;
    uint8_t abStack_101[255];

    pbVar3 = param_2;
    local_102 = *param_2;
    pbVar1 = abStack_101;
    for (uVar2 = (uint32_t)local_102; pbVar3 = pbVar3 + 1, uVar2 != 0; uVar2 = uVar2 - 1) {
        pbVar1 = pbVar1 + 1;
        *pbVar1 = *pbVar3;
    }

    *(uint8_t *)0x7690 = 1;
    FUN_24dd_48cf(0x7692, 0, local_102, 0xff);
}
