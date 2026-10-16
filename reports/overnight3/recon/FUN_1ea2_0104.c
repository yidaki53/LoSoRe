/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ea2_0104
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_029f(uint16_t, uint16_t, uint16_t);

uint16_t __stdcall16far FUN_1ea2_0104(uint32_t *param_1) {
    int iVar1;
    uint16_t in_AX;
    uint8_t uVar2;
    uint8_t extraout_AH;
    int *piVar3;
    uint16_t *puVar4;
    uint16_t uVar5;
    uint16_t unaff_DS;
    int local_6;
    uint8_t local_3;

    uVar2 = (uint8_t)((uint16_t)in_AX >> 8);
    local_3 = 0;

    if (-1 < *(char *)0x65ee) {
        iVar1 = *(int *)(*(char *)0x65ee * 2 + 0x65e8);
        local_6 = 0;

        while (true) {
            uVar5 = (uint16_t)((uint32_t)*param_1 >> 0x10);
            piVar3 = (int *)((int)*param_1 + local_6 * 4);

            if (*piVar3 != 0 || piVar3[1] != 0) {
                uVar5 = (uint16_t)((uint32_t)*param_1 >> 0x10);
                puVar4 = (uint16_t *)((int)*param_1 + local_6 * 4);
                FUN_24dd_029f(*(uint16_t *)(*(char *)0x65ee * 2 + 0x65e2), *puVar4, puVar4[1]);
            }

            if (local_6 == iVar1 + -1) break;
            local_6 = local_6 + 1;
        }

        FUN_24dd_029f(*(int *)(*(char *)0x65ee * 2 + 0x65e8) << 2, *(uint16_t *)param_1, *(uint16_t *)((int)(uint32_t *)param_1 + 2));
        *(char *)0x65ee = *(char *)0x65ee + -1;
        local_3 = 1;
        uVar2 = extraout_AH;
    }

    return (uint16_t)((uVar2 << 8) | local_3);
}
