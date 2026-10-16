/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4654
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_4531(void);

uint32_t FUN_24dd_4654(uint16_t param_1) {
    uint32_t uVar1;
    uint32_t uVar2;
    uint16_t *ptr = (uint16_t *)0x0000; // Assuming 0x0000 is the base address for the segment

    uVar1 = FUN_24dd_4531();
    uVar2 = ((uint32_t)*ptr * param_1) >> 16;
    return ((uint32_t)*ptr * param_1) << 16 | ((uint32_t)*ptr * param_1) << 16 | uVar2;
}
