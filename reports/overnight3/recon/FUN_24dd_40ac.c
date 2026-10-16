/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_40ac
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_40ac(uint16_t param_1, uint8_t *param_2, uint8_t *param_3) {
    uint8_t *puVar1;
    uint8_t *puVar2;
    uint16_t uVar3;
    uint8_t bVar4;
    uint8_t *puVar5;
    uint8_t *puVar6;

    puVar6 = param_3;
    puVar5 = param_2;
    bVar4 = (uint8_t)(param_1 >> 8);

    for (uVar3 = bVar4; uVar3 != 0; uVar3--) {
        *puVar6 = 0;
        puVar6++;
    }

    for (uVar3 = param_1 & 0xff; uVar3 != 0; uVar3--) {
        *puVar6 = *puVar5;
        puVar6++;
        puVar5++;
    }

    for (uVar3 = (uint16_t)((uint8_t)(' ' - (uint8_t)param_1) - bVar4); uVar3 != 0; uVar3--) {
        *puVar6 = 0;
        puVar6++;
    }
}
