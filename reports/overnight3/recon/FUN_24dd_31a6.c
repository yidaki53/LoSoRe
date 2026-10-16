/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_31a6
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_31a6(void) {
    uint16_t uVar1;
    uint16_t *ptr = (uint16_t *)0x7b40;

    do {
        uVar1 = *ptr;
        if ((uVar1 & 0x4500) != 0) {
            if ((uVar1 & 0x4000) != 0) {
                if ((uVar1 & 0x400) != 0) {
                    break;
                }
            } else {
                break;
            }
        } else {
            break;
        }
    } while (true);

    return uVar1;
}
