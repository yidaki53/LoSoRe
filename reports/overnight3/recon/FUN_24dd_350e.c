/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_350e
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_350e(void) {
    uint16_t uVar1;
    char *in_SI;

    uVar1 = (uint16_t)0x28;
    in_SI = (char *)0x0000; // Assuming in_SI is initialized to some valid memory location

    while (*in_SI != '\0') {
        in_SI++;
        uVar1--;
    }

    *in_SI = 0x30;
}
