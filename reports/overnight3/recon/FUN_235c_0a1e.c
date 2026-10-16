/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0a1e
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint8_t FUN_235c_0a1e(uint8_t param_1) {
    uint8_t local_3 = 0;
    uint8_t local_4 = 0;

    while (true) {
        if (*(uint8_t *)((uint16_t)local_4 * 10 + 0x6808) == param_1) {
            local_3 = 1;
        }
        if (local_4 == 7) break;
        local_4++;
    }
    return local_3;
}
