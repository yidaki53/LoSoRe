/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_13e9
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_2971_67f6(uint16_t, uint16_t, uint16_t, uint16_t, int, uint16_t, int, int);

void FUN_1ec2_13e9(uint32_t param_1, uint32_t param_2, uint8_t param_3, uint8_t *param_4, int param_5, int param_6) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t *pbVar3;
    uint8_t bVar4;
    int iVar5;
    uint32_t uVar6;
    uint8_t *pbVar7;
    int iVar8;
    uint16_t uVar9;
    uint16_t uVar10;
    uint8_t local_105;
    uint32_t local_104;
    uint8_t local_102[256];

    iVar5 = param_6;
    bVar4 = param_3;
    pbVar7 = param_4;
    bVar1 = *param_4;
    pbVar3 = local_102;
    local_102[0] = bVar1;

    for (uVar6 = (uint32_t)bVar1; uVar6 != 0; uVar6--, pbVar3++, pbVar7++) {
        *pbVar3 = *pbVar7;
    }

    uVar9 = (uint16_t)(param_1 >> 0x10);
    iVar8 = (int)param_1;
    *(uint8_t *)0x65f0 = *(uint8_t *)(iVar8 + 0x273f);

    if (bVar1 != 0) {
        local_104 = 1;
        while (1) {
            local_105 = local_102[local_104];
            if (local_105 == 0) {
                param_5 += *(uint8_t *)0x65f0;
                param_6 = iVar5;
            } else {
                if (local_105 == 0xff) {
                    if (bVar4 == 1) {
                        param_3 = local_102[local_104 + 1];
                    }
                    local_105 = local_102[local_104 + 2];
                    local_104 += 2;
                }
                local_105 -= 2;
                bVar2 = *(uint8_t *)(iVar8 + (uint32_t)local_105 * 0x40 + 0x3f);
                uVar10 = (uint16_t)(param_2 >> 0x10);

                if ((int)(0x13f - (uint32_t)bVar2) < param_6) {
                    param_5 += *(uint8_t *)0x65f0;
                    FUN_2971_67f6(0x1ec2, ((uint16_t)((uint32_t)local_105 * 0x40 >> 8) | param_3),
                                  (uint16_t)(iVar8 + (uint32_t)local_105 * 0x40), uVar9, (int)param_2, uVar10, param_5, iVar5);
                    param_6 = iVar5;
                } else {
                    FUN_2971_67f6(0x1ec2, ((uint16_t)((uint32_t)local_105 * 0x40 >> 8) | param_3),
                                  (uint16_t)(iVar8 + (uint32_t)local_105 * 0x40), uVar9, (int)param_2, uVar10, param_5, param_6);
                }
                param_6 += (uint32_t)bVar2;
            }
            if (local_104 == bVar1) break;
            local_104++;
        }
    }
}
