/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_029f
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_041e(void);
void FUN_24dd_010f(void);

void __stdcall16far FUN_24dd_029f(void) {
    uint8_t cf;

    FUN_24dd_041e();
    __asm__ volatile ("pushf; pop %%ax; setc %%al" : "=a" (cf));
    if (cf == 0) {
        return;
    }
    FUN_24dd_010f();
    return;
}
