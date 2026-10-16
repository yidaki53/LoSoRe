/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_47d9
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=4 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_46f6(void);

void FUN_24dd_47d9(int param_1, uint8_t *param_2, int param_3) {
    uint8_t *puVar1;
    int in_CX = 0; // Assuming in_CX is initialized to 0 or some meaningful value
    uint8_t *puVar2;
    uint8_t *puVar3;
    uint16_t uVar4;
    uint16_t unaff_SS = 0; // Assuming unaff_SS is initialized to 0 or some meaningful value

    FUN_24dd_46f6();

    uVar4 = (uint16_t)((uint32_t)(uintptr_t)param_2 >> 0x10);

    if (param_1 < param_3) {
        param_3 = param_1;
    }
    if (param_1 < in_CX) {
        in_CX = param_1;
    }
    if (param_3 < in_CX) {
        param_3 = in_CX;
    }

    puVar3 = param_2 + 1;
    *param_2 = (uint8_t)param_3;
    param_3 = param_3 - in_CX;
    puVar2 = (uint8_t *)&unaff_SS; // Assuming stack0xfffe is represented by unaff_SS

    if (param_3 != 0) {
        while (param_3 != 0) {
            puVar1 = puVar3;
            puVar3 = puVar3 + 1;
            *puVar1 = 0x20; // Space character
            param_3 = param_3 - 1;
        }
    }

    while (in_CX != 0) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar1 = *puVar2;
        puVar2 = puVar2 + 1;
        in_CX = in_CX - 1;
    }
}
