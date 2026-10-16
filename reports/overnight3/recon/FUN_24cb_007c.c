/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24cb_007c
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24cb_007c(uint16_t *param_1) {
    uint16_t bx;
    uint16_t es;

    // Simulate the interrupt call
    asm volatile (
        "int $0x21"
        : "=b" (bx), "=S" (es)
        :
        : "memory"
    );

    *param_1 = bx;
    *(param_1 + 1) = es;
    return;
}
