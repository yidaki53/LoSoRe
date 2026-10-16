/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_455e
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

uint16_t FUN_24dd_455e(uint16_t in_AX, uint16_t in_DX) {
    uint16_t uVar1;
    uint8_t bVar2;
    int iVar3;
    uint16_t uVar4;
    uint16_t uVar5;

    if (in_AX != 0 || in_DX != 0) {
        if ((int16_t)in_DX < 0) {
            uVar4 = -in_AX;
            uVar5 = -in_DX;
            bVar2 = (uint8_t)(uVar5 >> 8);
            uVar1 = uVar4 ^ uVar5;
            iVar3 = (int16_t)uVar5;
            if (bVar2 != 0) {
                iVar3 = -iVar3;
            }
            return ((uint16_t)(iVar3 >> 8) << 16) | iVar3;
        }
        uVar1 = 0;
        bVar2 = (uint8_t)(in_DX >> 8);
        while (true) {
            uVar5 = in_DX;
            in_DX = in_DX / 10;
            uVar4 = in_AX;
            in_AX = uVar5 - (in_AX * 10);
            if (bVar2 != 0) {
                iVar3 = -uVar4;
            } else {
                iVar3 = uVar4;
            }
            if (in_AX == 0 && in_DX == 0) break;
            uVar1 = ((uint16_t)(iVar3 >> 8) << 16) | iVar3;
        }
        return uVar1;
    }
    return 0;
}
