/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_1380
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __cdecl16far FUN_235c_1380(void) {
    uint8_t bVar1;

    bVar1 = in(0x2f);
    if ((bVar1 & 0x80) != 0) {
        out(0x2f, 1);
    } else {
        out(0x2f, 0);
    }
    return;
}
