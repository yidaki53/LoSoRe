/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24ba_00d8
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t DAT_783b; // Assuming this is the base address for the segment

uint8_t __cdecl16far FUN_24ba_00d8(void) {
    uint8_t local_4 = 0xab;
    
    while (true) {
        if (*(uint8_t *)(DAT_783b + local_4) != '\0') {
            return 1;
        }
        if (local_4 == 1) {
            break;
        }
        local_4--;
    }
    return 0;
}
