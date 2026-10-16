/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0c11
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_1ec2_0c11(uint16_t param_1, int param_2) {
    uint16_t local_4;

    if (param_2 < 0) {
        local_4 = 0xffff;
    } else if (param_2 < 1) {
        local_4 = 0;
    } else {
        local_4 = 1;
    }
    return local_4;
}
