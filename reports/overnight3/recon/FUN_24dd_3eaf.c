/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3eaf
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_3eaf(uint8_t param_1, uint8_t *param_2, uint8_t *param_3) {
    uint8_t bVar1;
    uint16_t uVar2;
    uint8_t *pbVar3;
    uint8_t *pbVar4;

    pbVar3 = param_3;
    pbVar4 = param_2;
    bVar1 = *param_3;
    if (param_1 < bVar1) {
        bVar1 = param_1;
    }
    *param_2 = bVar1;
    uVar2 = (uint16_t)bVar1;
    while (uVar2 != 0) {
        pbVar4++;
        pbVar3++;
        uVar2--;
        *pbVar4 = *pbVar3;
    }
}
