/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3b5d
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=1 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __cdecl16far FUN_24dd_3b5d(void) {
    uint16_t *ptr = (uint16_t *)(0x6422);
    uint16_t uVar1 = 0x3d;
    uint16_t uVar2 = 0;

    while (true) {
        *(uint16_t *)(uVar2 * 16 + 0x6410) = *ptr;
        if (uVar2 == 0xff) break;
        uVar2++;
    }
}
