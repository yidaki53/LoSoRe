/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0f1d
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_454d(void);
void FUN_24dd_452f(uint16_t, uint16_t, uint16_t);

void __cdecl16far FUN_235c_0f1d(void) {
    if (*(char *)(0x67cd) != '\0') {
        if (*(char *)(0x6e58) != 0) {
            FUN_24dd_454d();
            if (*(char *)(0x6e5a) != 0) {
                FUN_24dd_452f(0x1000, *(uint16_t *)(0x6e58), *(uint16_t *)(0x6e5a));
            } else {
                FUN_24dd_452f(0x800, *(uint16_t *)(0x6e58), *(uint16_t *)(0x6e5a));
            }
        } else {
            FUN_24dd_452f(0x1000, 0, 0);
        }
    } else {
        FUN_24dd_452f(0x800, 0, 0);
    }
    return;
}
