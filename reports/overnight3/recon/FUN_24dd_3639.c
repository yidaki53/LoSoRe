/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3639
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_3639(uint8_t *param_1, uint16_t *param_2) {
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    int iVar3;
    uint32_t uVar4;
    uint8_t *pbVar5;
    uint16_t *puVar6;
    uint8_t *pbVar7;
    uint16_t uVar8;

    uVar8 = (uint16_t)((uint32_t)(uint16_t)param_2 >> 0x10);
    puVar6 = (uint16_t *)param_2;
    *param_2 = 0;
    puVar6[1] = 0xd7b0;
    puVar6[2] = 0x80;
    puVar6[3] = 0;
    puVar6[4] = 0;
    puVar6[5] = 0;
    puVar6[6] = (uint16_t)(puVar6 + 0x40);
    puVar6[7] = uVar8;
    pbVar7 = (uint8_t *)(puVar6 + 9);
    puVar6[8] = 0x420c;
    pbVar7[0] = 0xdd;
    pbVar7[1] = 0x24;
    for (iVar3 = 0xe; iVar3 != 0; iVar3--) {
        pbVar7[0] = 0;
        pbVar7[1] = 0;
        pbVar7 += 2;
    }
    uVar4 = 0x4f;
    pbVar5 = param_1 + 1;
    if (*param_1 < 0x4e) {
        uVar4 = (uint32_t)*param_1;
    }
    for (; uVar4 != 0; uVar4--) {
        pbVar1 = pbVar5;
        pbVar5++;
        if (*pbVar1 == 0) {
            break;
        }
        pbVar2 = pbVar7;
        pbVar7++;
        *pbVar2 = *pbVar1;
    }
    *pbVar7 = 0;
}
