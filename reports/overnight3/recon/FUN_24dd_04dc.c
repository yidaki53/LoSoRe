/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_04dc
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_24dd_04dc(uint16_t in_AX) {
    uint16_t uVar1;
    
    uVar1 = in_AX;
    uVar1 = ((uint8_t)(uVar1 >> 8) & 8) | ((uint8_t)uVar1 >> 7) | ((uint8_t)uVar1 >> 6) | ((uint8_t)uVar1 >> 5);
    return uVar1;
}
