/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3ed3
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_3ed3(uint16_t param_1, uint16_t param_2, uint8_t *param_3, uint8_t *param_4) {
    uint8_t *pbVar4 = param_4;
    uint16_t uVar2;
    uint8_t *pbVar3 = param_3 + param_2;

    if ((int16_t)param_2 < 1) {
        param_2 = 1;
    }

    if (*param_3 < param_2) {
        uVar2 = 0;
    } else {
        uVar2 = (*param_3 - param_2) + 1;
        if ((int16_t)param_1 < 0) {
            param_1 = 0;
        }
        if (param_1 < uVar2) {
            uVar2 = param_1;
        }
    }

    *param_4 = (uint8_t)uVar2;

    while (uVar2 != 0) {
        *pbVar4 = *pbVar3;
        pbVar4++;
        pbVar3++;
        uVar2--;
    }
}
