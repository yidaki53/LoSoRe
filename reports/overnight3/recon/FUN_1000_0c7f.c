/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_0c7f
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t FUN_24dd_0530(void);
extern uint8_t FUN_24dd_4161(void);

uint8_t FUN_1000_0c7f(int param_1, int param_2, int param_3, int param_4, int param_5, int param_6) {
    uint8_t local_3 = 1;
    uint32_t uVar4;
    int iVar2, iVar3, iVar5;
    uint8_t bVar1;

    FUN_24dd_0530();

    uVar4 = (param_4 - param_6) >> 0xF;
    if (((((int)((param_4 - param_6) ^ uVar4) - uVar4) < 0xA1) &&
         (uVar4 = (param_3 - param_5) >> 0xF, (int)((param_3 - param_5) ^ uVar4) - uVar4 < 0xA1)) ||
        ((uVar4 = (param_2 - param_6) >> 0xF, (int)((param_2 - param_6) ^ uVar4) - uVar4 < 0xA1 &&
         (uVar4 = (param_1 - param_5) >> 0xF, (int)((param_1 - param_5) ^ uVar4) - uVar4 < 0xA1)))) {
        local_3 = 0;
    } else {
        for (iVar2 = param_6 - 3; iVar2 <= param_6 + 3; iVar2++) {
            for (iVar3 = param_5 - 4; iVar3 <= param_5 + 4; iVar3++) {
                iVar5 = 0x20;
                bVar1 = FUN_24dd_4161();
                if ((*(uint8_t *)(iVar5 + 0x14A0) & bVar1) != 0) {
                    return 0;
                }
            }
        }
    }
    return local_3;
}
