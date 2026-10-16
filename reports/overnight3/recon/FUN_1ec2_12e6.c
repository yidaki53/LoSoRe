/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_12e6
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_1ec2_12e6(uint8_t param_1, char *param_2, uint32_t param_3, uint8_t param_4, uint16_t param_5) {
    char *pcVar1;
    uint8_t bVar2;
    char cVar3;
    uint8_t uVar4;
    char cVar5;
    char cVar6;
    char *pcVar7;
    uint8_t *puVar8;
    uint8_t *puVar9;
    uint16_t uVar10;
    uint16_t uVar11;

    uVar10 = (uint16_t)(param_3 >> 16);
    pcVar7 = param_2;
    uVar11 = (uint16_t)((uint32_t)param_2 >> 16);

    if (((param_5 + 8 < 8) || (0x13f < param_5 + 8)) || (param_4 + 7U < 7) || (199 < param_4 + 7U)) {
        bVar2 = param_4;
        puVar8 = (uint8_t *)((int32_t)param_3 + param_4 * 0x140 + param_5);
        cVar5 = '\a';
        do {
            cVar6 = '\b';
            do {
                puVar9 = puVar8;
                pcVar1 = pcVar7;
                pcVar7 = pcVar7 + 1;
                cVar3 = (char)param_5;
                if ((param_5 < 0x140) && (bVar2 < 200) && (*pcVar1 != '\0')) {
                    *puVar9 = param_1;
                }
                uVar4 = (uint8_t)(param_5 >> 8);
                param_5 = ((uint16_t)uVar4 << 8) | (cVar3 + 1);
                cVar6 = cVar6 - 1;
                puVar8 = puVar9 + 1;
            } while (cVar6 != '\0');
            puVar8 = puVar9 + 0x139;
            param_5 = ((uint16_t)uVar4 << 8) | (cVar3 - 7);
            bVar2 = bVar2 + 1;
            cVar5 = cVar5 - 1;
        } while (cVar5 != '\0');
    } else {
        puVar8 = (uint8_t *)((int32_t)param_3 + param_4 * 0x140 + param_5);
        cVar5 = '\a';
        do {
            cVar6 = '\b';
            do {
                puVar9 = puVar8;
                pcVar1 = pcVar7;
                pcVar7 = pcVar7 + 1;
                if (*pcVar1 != '\0') {
                    *puVar9 = param_1;
                }
                cVar6 = cVar6 - 1;
                puVar8 = puVar9 + 1;
            } while (cVar6 != '\0');
            puVar8 = puVar9 + 0x139;
            cVar5 = cVar5 - 1;
        } while (cVar5 != '\0');
    }
}
