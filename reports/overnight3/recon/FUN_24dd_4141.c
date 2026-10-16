/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4141
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_4141(uint16_t param_1, uint8_t *param_2, uint32_t param_3) {
    uint8_t *puVar1;
    uint8_t *puVar2;
    uint8_t *puVar3;
    uint8_t *puVar4;

    puVar4 = param_2;
    puVar3 = (uint8_t *)((int)param_3 + (param_1 >> 8));
    for (param_1 = param_1 & 0xff; param_1 != 0; param_1--) {
        puVar2 = puVar4;
        puVar4 = puVar4 + 1;
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar2 = *puVar1;
    }
}
