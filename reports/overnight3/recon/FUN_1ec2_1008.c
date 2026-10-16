/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_1008
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_1ec2_1008(uint16_t *param_1, uint16_t *param_2, char param_3, char param_4, char param_5, char param_6, uint8_t param_7, int param_8, uint param_9, int param_10, int param_11) {
    int iVar1;
    int iVar2;
    uint8_t bVar3;
    uint uVar4;
    uint8_t *pbVar5;
    uint8_t *pbVar6;
    uint16_t uVar7;
    uint16_t uVar8;

    if ((param_11 < 0x9e) && (param_10 < 0x9e) && (-1 < param_11 + param_8) && (-1 < (int)(param_10 + param_9))) {
        uVar8 = (uint16_t)((uintptr_t)param_1 >> 16);
        pbVar5 = (uint8_t *)param_1;
        uVar7 = (uint16_t)((uintptr_t)param_2 >> 16);
        pbVar6 = (uint8_t *)((int)param_2 + param_11 * 0x140 + param_10);
        iVar1 = 0x140 - param_9;

        while (param_11 != 0) {
            uVar4 = param_9;
            while (uVar4 != 0) {
                iVar2 = param_8;
                while (iVar2 != 0) {
                    bVar3 = *pbVar5;
                    *pbVar6 = bVar3;
                    pbVar5++;
                    pbVar6++;
                    iVar2--;
                }
                uVar4--;
                pbVar5 = (uint8_t *)((int)pbVar5 + iVar1);
                pbVar6 = (uint8_t *)((int)pbVar6 + iVar1);
            }
            param_11--;
            pbVar5 = (uint8_t *)((int)pbVar5 + iVar1);
            pbVar6 = (uint8_t *)((int)pbVar6 + iVar1);
        }
    }
}
