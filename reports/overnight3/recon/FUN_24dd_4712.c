/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4712
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_4712(uint16_t in_AX, uint16_t in_BX, int in_CX, uint16_t *unaff_DI) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t *puVar6;

    uVar3 = in_AX;
    uVar4 = in_BX;
    uVar2 = uVar3 / in_CX;
    uVar1 = uVar4 / in_CX;
    if ((0x39 < uVar2) || (uVar2 < 0x3b)) {
        uVar2 = uVar2 + 0x30;
    } else {
        uVar2 = uVar2 + 0x37;
    }
    puVar5 = (uint16_t *)unaff_DI;
    puVar6 = (uint16_t *)((int)puVar5 + uVar1);
    *puVar6 = uVar2;
    if ((uVar3 & 0xFFFF0000) == 0 && (uVar4 & 0xFFFF0000) == 0) {
        return;
    }
    uVar3 = uVar3 & 0xFFFF;
    uVar4 = uVar4 & 0xFFFF;
    do {
        for (; (uVar2 = uVar2 + -1), (0x39 < uVar2) || (uVar2 < 0x3b);) {
            uVar2 = uVar2 + 0x30;
        }
        puVar6 = puVar5;
        puVar5 = puVar5 + 1;
        *puVar6 = uVar2;
    } while ((uVar3 != 0) || (uVar4 != 0));
    return;
}
