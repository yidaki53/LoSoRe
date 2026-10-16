/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_0706
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_4824(int *param1, uint16_t param2, uint8_t *param3, uint16_t param4);
extern void FUN_24dd_46e9();

uint16_t __stdcall16far FUN_202c_0706(uint8_t *param_1) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint32_t uVar3;
    int local_10c;
    uint16_t local_10a;
    uint16_t local_108;
    uint8_t local_106;
    uint8_t abStack_105[259];

    pbVar2 = param_1;
    local_106 = *param_1;
    pbVar1 = abStack_105;
    for (uVar3 = (uint32_t)local_106; pbVar1 = pbVar1 + 1, pbVar2 = pbVar2 + 1, uVar3 != 0; uVar3 = uVar3 - 1) {
        *pbVar1 = *pbVar2;
    }

    local_108 = FUN_24dd_4824(&local_10c, 0, &local_106, 0);
    if (local_108 != 0) {
        return ((uint16_t)local_10c << 16) | local_10a;
    }

    FUN_24dd_46e9();
    if (local_108 != 0) {
        return ((uint16_t)local_10c << 16) | local_10a;
    }

    return ((uint16_t)local_10c << 16) | local_10a;
}
