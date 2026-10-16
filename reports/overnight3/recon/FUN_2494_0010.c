/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_2494_0010
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __cdecl16far FUN_2494_0010(void) {
    uint16_t bx;
    uint16_t es;

    // Simulate the interrupt call
    asm volatile (
        "int $0x2f"
        : "=b" (bx), "=S" (es)
        :
        : "memory"
    );

    *(uint16_t *)(0x7838) = bx;
    *(uint16_t *)(0x783a) = es;
}
