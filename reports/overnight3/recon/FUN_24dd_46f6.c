/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_46f6
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_4712(void);

void FUN_24dd_46f6(uint16_t in_AX, uint16_t in_DX, uint16_t *unaff_DI) {
    uint32_t uVar1;
    uint16_t bVar2;
    char cVar3;

    if ((int16_t)in_DX < 0) {
        FUN_24dd_4712();
        *(unaff_DI - 1) = 0x2d;
        return;
    }

    do {
        uVar1 = (uint32_t)in_DX;
        in_DX = in_DX / 10;
        uVar1 = (uVar1 % 10) << 0x10 | (uint32_t)in_AX;
        in_AX = uVar1 / 10;
        cVar3 = (char)(uVar1 % 10);
        bVar2 = cVar3 + 0x30;
        if (0x39 < bVar2) {
            bVar2 = cVar3 + 0x37;
        }
        unaff_DI--;
        *unaff_DI = bVar2;
    } while (in_AX != 0 || in_DX != 0);
}
