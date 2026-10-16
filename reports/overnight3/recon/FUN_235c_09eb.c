/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_09eb
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_235c_09eb(char param_1) {
    char local_3 = 0;
    
    while (true) {
        if (*(char *)((uint16_t)local_3 * 10 + 0x6808) == param_1) {
            FUN_235c_09eb(local_3);
            *(char *)0x67ce = *(char *)0x67ce - 1;
            if (local_3 == 7) break;
        }
        local_3 = local_3 + 1;
    }
    return;
}
