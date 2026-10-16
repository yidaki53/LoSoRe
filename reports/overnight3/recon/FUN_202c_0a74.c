/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_0a74
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_48e1(uint16_t);

uint8_t FUN_202c_0a74(int param_1, int param_2, int param_3) {
    uint8_t local_3 = 0;
    
    if (param_3 + param_1 <= param_3 + param_2) {
        int local_6 = param_3 + param_1;
        while (true) {
            int local_8 = param_3 + param_2;
            while (true) {
                uint16_t uVar4 = 0x20;
                FUN_24dd_48e1(0x14a0);
                if (local_8 < 0 || local_8 > 0x15e || local_6 < 0 || local_6 > 0x1f8) break;
                if (local_8 == param_3 + param_2 && local_6 == param_3 + param_1) {
                    local_3 = 1;
                    break;
                }
            }
            if (local_8 == param_3 + param_2 && local_6 == param_3 + param_1) break;
        }
    }
    return local_3;
}
