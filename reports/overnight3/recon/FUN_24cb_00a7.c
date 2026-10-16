/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24cb_00a7
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24cb_00a7(uint16_t param_1, uint8_t *param_2) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t bVar3;
    uint8_t *pbVar4;
    uint8_t *pbVar5;
    uint32_t uVar6;
    uint32_t uVar7;
    uint32_t uVar8;

    uVar8 = (uint32_t)param_2;
    bVar1 = *param_2;
    if (0x1f < bVar1) {
        bVar1 = 0x1f;
    }
    bVar2 = (uint16_t)bVar1;
    uVar7 = (uint32_t)bVar2;
    do {
        for (; (bVar3 = *param_2, (0x60 < bVar3) && (bVar3 < 0x7b)); bVar3 = *param_2) {
            uVar6 = (uint32_t)bVar3;
            uVar8 = uVar8 + ((uint16_t)(uVar6 >> 8) * 0x100) + (uVar6 & 0xff);
            param_2 = param_2 + 1;
        }
        uVar8 = uVar8 + ((uint16_t)(bVar1 >> 8) * 0x100) + (bVar1 & 0xff);
        bVar1 = bVar1 + 1;
    } while (bVar1 != 0x100);
    bVar2 = (uint8_t)(-(int32_t)param_1);
    *(uint8_t *)uVar8 = bVar2;
    pbVar5 = (uint8_t *)uVar8;
    do {
        for (; (pbVar4 = param_2, (0x60 < *param_2) && (param_2[1] < 0x7b)); param_2 = param_2 + 1) {
            uVar6 = (uint32_t)*param_2;
            uVar8 = uVar8 + ((uint16_t)(uVar6 >> 8) * 0x100) + (uVar6 & 0xff);
        }
        uVar8 = uVar8 + ((uint16_t)(bVar1 >> 8) * 0x100) + (bVar1 & 0xff);
        bVar1 = bVar1 + 1;
    } while (bVar1 != 0x100);
    *(uint8_t *)uVar8 = bVar2;
    return;
}
