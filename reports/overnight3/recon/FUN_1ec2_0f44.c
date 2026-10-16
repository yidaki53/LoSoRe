/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0f44
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_1ec2_0f44(char *param_1, uint32_t param_2, char param_3, uint8_t param_4, uint8_t param_5, int param_6, uint32_t param_7, int param_8, int param_9);

void FUN_1ec2_0f44(char *param_1, uint32_t param_2, char param_3, uint8_t param_4, uint8_t param_5, int param_6, uint32_t param_7, int param_8, int param_9) {
    int iVar1;
    int iVar2;
    uint8_t bVar3;
    uint32_t uVar4;
    char *pcVar5;
    uint8_t *pbVar6;
    uint16_t uVar7;

    if (((param_8 < 0x9e) && (param_9 < 0x9e)) && (-1 < param_8 + param_6) && (-1 < (int)(param_9 + param_7))) {
        pcVar5 = param_1;
        uVar7 = (uint16_t)(param_2 >> 0x10);
        pbVar6 = (uint8_t *)((int)param_2 + param_8 * 0x140 + param_9);
        iVar1 = 0x140 - (param_7 & 0xff);

        do {
            uVar4 = param_7 & 0xff;
            if (-1 < param_8) {
                iVar2 = param_9;
                if (0x9d < param_8) {
                    return;
                }
                do {
                    if (-1 < iVar2) {
                        if (0x9d < iVar2) {
                            pbVar6 = pbVar6 + uVar4 + iVar1;
                            pcVar5 = pcVar5 + uVar4;
                            goto joined_r0x0001fbf4;
                        }
                        if ((*pcVar5 != '\0') && (bVar3 = *pbVar6, param_5 <= bVar3) && (bVar3 <= param_4)) {
                            *pbVar6 = bVar3 + param_3;
                        }
                    }
                    pbVar6 = pbVar6 + 1;
                    pcVar5 = pcVar5 + 1;
                    iVar2 = iVar2 + 1;
                    bVar3 = (uint8_t)uVar4 - 1;
                    uVar4 = (uint32_t)bVar3;
                } while (bVar3 != 0);
                pbVar6 = pbVar6 + iVar1;
                param_8 = param_8 + 1;
                param_6 = param_6 - 1;
                if (param_6 == 0) {
                    return;
                }
            }
            pbVar6 = pbVar6 + 0x140;
            pcVar5 = pcVar5 + uVar4;
joined_r0x0001fbf4:
            param_6 = param_6 - 1;
            param_8 = param_8 + 1;
        } while (param_6 != 0);
    }
}
