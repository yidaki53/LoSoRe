/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_249c_0180
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint8_t __stdcall16far FUN_249c_0180(uint8_t param_1) {
    uint8_t uVar1;
    int iVar2;
    
    iVar2 = 0;
    uVar1 = in(0x21);
    if (param_1 == 0xff) {
        iVar2 = 1;
    }
    return ((uint8_t)iVar2) << 8 | uVar1;
}
