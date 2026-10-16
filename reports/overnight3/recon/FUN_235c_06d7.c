/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_06d7
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_235c_06d7(uint16_t param_1, int16_t param_2, uint16_t param_3, int16_t param_4) {
    uint16_t local_6;
    uint16_t local_4;

    if ((param_4 < param_2) || ((param_4 <= param_2) && (param_3 < param_1))) {
        local_6 = param_3;
        local_4 = param_4;
    } else {
        local_6 = param_1;
        local_4 = param_2;
    }
    return (local_4 << 8) | local_6;
}
