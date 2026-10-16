/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3bde
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __cdecl16far FUN_24dd_3bde(uint16_t param_1) {
    int iVar1;
    uint16_t uVar2;
    uint8_t bVar3;

    bVar3 = 0;
    FUN_24dd_3b33();
    if (*(int *)(param_1 + 0x6410) < 4) {
        uVar2 = 0x4;
        while (true) {
            iVar1 = 0x21;
            bVar3 = in(iVar1) != 0;
            if (bVar3) break;
            uVar2 = uVar2 * 10 + *(uint8_t *)(param_1 + 0x6410);
        }
        *(uint16_t *)(param_1 + 0x6410) = 0;
        *(uint16_t *)((int)param_1 + 2) = 0xd7b0;
    }
    return;
}
