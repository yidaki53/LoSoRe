/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0aff
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_3d80(void);

uint16_t FUN_235c_0aff(uint16_t param_1) {
    uint16_t uVar1;
    int16_t iVar2;
    
    iVar2 = 0;
    uVar1 = FUN_24dd_3d80();
    uint16_t result = ((uint16_t)(iVar2 + ((param_1 >> 16) + uVar1)) << 16) | (param_1 + iVar2);
    return result;
}
