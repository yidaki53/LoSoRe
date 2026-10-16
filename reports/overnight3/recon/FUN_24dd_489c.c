/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_489c
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_489c(uint16_t param_1) {
    uint16_t uVar1;
    uint16_t *base_address = (uint16_t *)0x6410;

    if (*(char *)(param_1 + 2) == -0x7b3) {
        uVar1 = param_1;
        *(uint16_t *)(uVar1 + 1) = 0x4201;
        *(uint16_t *)(uVar1 + 2) = 0x4202;
        *(uint16_t *)(uVar1 + 3) = 0x4200;
        *(uint16_t *)base_address = 0x67;
    } else {
        *(uint16_t *)base_address = 0x0;
    }
}
