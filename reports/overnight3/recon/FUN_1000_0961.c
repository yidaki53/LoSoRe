/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_0961
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=None verdict=judge-error
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t FUN_24dd_4161(void);
extern void FUN_24dd_0530(void);

uint8_t FUN_1000_0961(uint16_t param_1, int16_t param_2, int16_t param_3) {
    uint16_t uVar1;
    uint8_t bVar2;
    int16_t iVar3;
    int16_t iVar4;
    int16_t iVar5;

    FUN_24dd_0530();

    iVar3 = param_3 - 2;
    if (iVar3 <= param_3 + 2) {
        while (true) {
            iVar4 = param_2 - 2;
            if (iVar4 <= param_2 + 2) {
                while (true) {
                    iVar5 = 0x20;
                    bVar2 = FUN_24dd_4161();
                    if ((*(uint8_t *)(iVar5 + 0x6604) & bVar2) != 0) {
                        return 0;
                    }
                    if (iVar4 == param_2 + 2) break;
                    iVar4++;
                }
            }
            if (iVar3 == param_3 + 2) break;
            iVar3++;
        }
    }

    while (true) {
        iVar3 = 0x20;
        bVar2 = FUN_24dd_4161();
        if ((*(uint8_t *)(iVar3 + 0x14c0) & bVar2) == 0) break;
        param_2++;
    }

    if (*(uint8_t *)0x669c != 0) {
        uVar1 = 1;
        while (true) {
            if ((uVar1 != param_1) &&
                (*(char *)((int)*(uint32_t *)0x6698 + uVar1 * 0xe - 2) != '\0') &&
                (param_3 - 0x1e < *(int16_t *)((int)*(uint32_t *)0x6698 + uVar1 * 0xe - 0xe)) &&
                ((*(int16_t *)((int)*(uint32_t *)0x6698 + uVar1 * 0xe - 0xe) < param_3 - 0x1e) &&
                 (param_2 - 0x1e < *(int16_t *)((int)*(uint32_t *)0x6698 + uVar1 * 0xe - 10)) &&
                 (*(int16_t *)((int)*(uint32_t *)0x6698 + uVar1 * 0xe - 10) < param_2 - 0x1e))) {
                return 0;
            }
            if (uVar1 == *(uint8_t *)0x669c) break;
            uVar1++;
        }
    }

    return 1;
}
