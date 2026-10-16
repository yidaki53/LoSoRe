/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24cb_0058
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24cb_0058(void) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t uVar6;

    uVar6 = (uint16_t)((uint16_t)0x10000 >> 16);
    puVar1 = (uint16_t *)0x10000;
    do {
        for (uVar2 = 0x100; *puVar1 != 0; uVar2--) {
            puVar3 = puVar1;
            puVar1 = puVar1 + 1;
        }
        puVar5 = puVar1;
        puVar1 = puVar1 - 1;
        uVar4 = 0;
        do {
            for (uVar6 = 0x100; *puVar3 != 0; uVar6--) {
                puVar5 = puVar5 + 1;
                puVar3 = puVar3 + 1;
            }
            puVar5 = puVar5 - 1;
            puVar3 = puVar3 - 1;
            uVar4 = uVar4 + 1;
        } while (uVar4 != 0);
        puVar5 = puVar5 - 1;
        puVar3 = puVar3 - 1;
    } while (uVar6 != 0);
    *(uint16_t *)0x78ee = 0;
    return;
}
