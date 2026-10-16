/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3d36
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_3d36(void) {
    uint16_t uVar1;
    uint8_t *pbVar2;
    uint8_t *pbVar3;
    uint32_t uVar4;
    int in_DX;

    uVar1 = *(uint16_t *)0x640c;
    uVar4 = (uint32_t)*(uint8_t *)0x80;
    pbVar2 = (uint8_t *)0x81;
    do {
        for (; (pbVar3 = pbVar2, uVar4 != 0 && (*pbVar2 < 0x21)); pbVar2 = pbVar2 + 1) {
            uVar4 = uVar4 - 1;
        }
        for (; (uVar4 != 0 && (0x20 < *pbVar3)); pbVar3 = pbVar3 + 1) {
            uVar4 = uVar4 - 1;
        }
    } while ((pbVar3 != pbVar2) && (in_DX = in_DX + -1, pbVar2 = pbVar3, in_DX != 0));
}
