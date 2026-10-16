/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_0530
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t DAT_640e; // Assuming this is the base address for the segment

uint16_t __cdecl16far FUN_24dd_0530(uint16_t param_1) {
    uint16_t uVar1;
    int16_t iVar2;

    if ((param_1 & 0x8000) != 0) {
        param_1 = -param_1;
    }

    iVar2 = (int16_t)(param_1 - DAT_640e);
    if (iVar2 < 0 || iVar2 >= 0x100) {
        return 0xca;
    }

    return param_1;
}
