/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_38f0
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_37ec(void);
void FUN_24dd_397a(void);

void __stdcall16far FUN_24dd_38f0(uint16_t param_1) {
    int iVar1;
    int bVar2;

    iVar1 = (int)param_1;
    bVar2 = 1;
    FUN_24dd_37ec();
    if (bVar2 && (*(int *)(iVar1 + 0x1a) != 0)) {
        FUN_24dd_397a();
    }
    return;
}
