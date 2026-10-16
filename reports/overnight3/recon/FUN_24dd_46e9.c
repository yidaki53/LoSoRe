/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_46e9
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __cdecl16far FUN_24dd_46e9(void) {
    uint16_t extraout_DX;
    uint16_t extraout_CX;

    // Simulate the interrupt call
    asm volatile (
        "int $0x21"
        : "=c" (extraout_CX), "=d" (extraout_DX)
        :
        : "memory"
    );

    *(uint16_t *)(0x6412) = extraout_CX;
    *(uint16_t *)(0x6414) = extraout_DX;
}
