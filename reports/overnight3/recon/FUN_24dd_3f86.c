/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3f86
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_3f86(uint8_t *param_1, uint8_t *param_2) {
    uint8_t bVar1;
    uint16_t uVar2;
    uint8_t *pbVar3;
    uint8_t *pbVar4;

    pbVar3 = param_2;
    pbVar4 = param_1;
    bVar1 = *param_2;
    if (*param_1 < *param_2) {
        bVar1 = *param_1;
    }
    if (bVar1 != 0) {
        uVar2 = (uint16_t)bVar1;
        do {
            pbVar4 = pbVar4 + 1;
            pbVar3 = pbVar3 + 1;
            if (uVar2 == 0) {
                return;
            }
            uVar2 = uVar2 - 1;
        } while (*pbVar3 == *pbVar4);
    }
    return;
}
