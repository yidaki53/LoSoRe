/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_a8f7
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <stdbool.h>

extern void FUN_24dd_0530(void);
extern uint32_t FUN_24dd_3d80(void);
extern uint32_t CARRY2(uint32_t a, uint32_t b);

void FUN_1000_a8f7(uint16_t param_1, int *param_2, uint8_t *param_3) {
    uint8_t *pbVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    int iVar5;
    uint8_t *pbVar6;
    int *piVar7;
    uint16_t uVar8;
    uint16_t unaff_SS;
    bool bVar9;
    uint32_t local_10a;
    int local_108;
    uint8_t local_102[252];

    FUN_24dd_0530();
    pbVar6 = param_3;
    local_102[0] = *param_3;
    pbVar1 = local_102;
    for (uVar4 = (uint32_t)local_102[0]; pbVar1 != local_102 + (int32_t)uVar4; pbVar1++, pbVar6++) {
        *pbVar1 = *pbVar6;
    }
    uVar8 = (uint16_t)((uint32_t)param_2 >> 0x10);
    piVar7 = (int *)(uint32_t)param_2;
    *param_2 = 0;
    piVar7[1] = 0;
    uVar4 = (uint32_t)local_102[0];
    if (uVar4 != 0) {
        local_10a = 1;
        local_108 = 0;
        while (true) {
            iVar5 = piVar7[1];
            uVar2 = FUN_24dd_3d80();
            uVar3 = local_102[local_10a] - 0x30;
            *param_2 = uVar3 + uVar2;
            piVar7[1] = ((int32_t)uVar3 >> 0xf) + iVar5 + (uint32_t)CARRY2(uVar3, uVar2);
            if ((local_108 == 0) && (local_10a == uVar4)) break;
            bVar9 = 0xfffe < local_10a;
            local_10a = local_10a + 1;
            local_108 = local_108 + (uint32_t)bVar9;
        }
    }
}
