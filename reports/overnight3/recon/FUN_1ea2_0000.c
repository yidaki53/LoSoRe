/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ea2_0000
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_0303(void);
extern uint32_t FUN_24dd_028a(uint16_t);

uint8_t __stdcall16far FUN_1ea2_0000(uint16_t param_1, uint16_t param_2, uint32_t *param_3) {
    int iVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint16_t *puVar4;
    uint16_t uVar5;
    uint32_t uVar6;
    int local_6;
    uint8_t local_3 = 0;

    if (*(char *)0x65ee < 3) {
        *(uint16_t *)(*(char *)0x65ee * 2 + 0x65e2) = param_2;
        *(uint16_t *)(*(char *)0x65ee * 2 + 0x65e8) = param_1;
        uVar2 = FUN_24dd_0303();
        if ((param_1 < 0x8000) &&
            ((param_1 > 0 ||
             ((uint32_t)(*(int16_t *)(*(char *)0x65ee * 2 + 0x65e2) * *(int16_t *)(*(char *)0x65ee * 2 + 0x65e8)) <=
              uVar2)))) {
            uVar6 = FUN_24dd_028a(*(int16_t *)(*(char *)0x65ee * 2 + 0x65e8) << 2);
            uVar2 = (uint32_t)((uint32_t)uVar6 >> 0x10);
            *(int32_t *)param_3 = (int32_t)uVar6;
            *(uint32_t *)((int32_t)param_3 + 2) = uVar2;
            iVar1 = *(int16_t *)(*(char *)0x65ee * 2 + 0x65e8);
            local_6 = 0;
            while (1) {
                uVar3 = FUN_24dd_0303();
                if (0x7fff < uVar2) {
                    return 0;
                }
                if ((int32_t)uVar2 < 1 && uVar3 < *(uint16_t *)(*(char *)0x65ee * 2 + 0x65e2)) {
                    return 0;
                }
                uVar6 = FUN_24dd_028a(*(uint16_t *)(*(char *)0x65ee * 2 + 0x65e2));
                uVar2 = (uint32_t)((uint32_t)uVar6 >> 0x10);
                uVar5 = (uint16_t)((uint32_t)*param_3 >> 0x10);
                puVar4 = (uint16_t *)((int32_t)*param_3 + local_6 * 4);
                *puVar4 = (int32_t)uVar6;
                puVar4[1] = uVar2;
                if (local_6 == iVar1 - 1) break;
                local_6++;
            }
            *(char *)0x65ee = *(char *)0x65ee + 1;
            local_3 = 1;
        }
    }
    return local_3;
}
