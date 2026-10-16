/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_36c4
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_36c4(uint16_t param_1) {
    uint16_t uVar1;
    uint16_t *ptr1;
    uint16_t *ptr2;
    uint16_t *ptr3;
    uint16_t *ptr4;

    uVar1 = (uint16_t)param_1;
    if ((0xd7b1 < uVar1) && (uVar1 < 0xd7b3)) {
        *(uint16_t *)0x6410 = 0x66;
    } else {
        ptr1 = (uint16_t *)0x0;
        while (true) {
            ptr2 = ptr1;
            ptr1 = (uint16_t *)((int)ptr1 + 1);
            if (ptr2 != NULL) {
                if ((0xd7b0 < ptr2[1]) && (ptr2[1] < 0xd7b2)) {
                    *(uint16_t *)0x6410 = 0x66;
                    break;
                }
            } else {
                break;
            }
        }
    }
    return;
}
