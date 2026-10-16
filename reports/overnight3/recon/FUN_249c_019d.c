/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_249c_019d
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t __far FUN_249c_019d(uint8_t param_1) {
    uint8_t uVar1;
    uint8_t *ptr1 = (uint8_t *)(0x159c);
    uint8_t *ptr2 = (uint8_t *)(0x159c);

    uVar1 = in(0x21);
    if (*ptr1 == '\0') {
        if (param_1 == 3) {
            out(0x23);
        }
    } else if (param_1 == 4) {
        uVar1 = in(0x21);
    }

    return uVar1;
}
