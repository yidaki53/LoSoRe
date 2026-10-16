/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_b3fe
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_0530(void);
extern void FUN_24ba_00d8(void);

uint16_t FUN_1000_b3fe(void) {
    uint8_t uVar1;
    int iVar2;
    uint8_t extraout_AL;
    uint8_t extraout_AH;
    uint16_t uStack_6 = 0x10000109;

    FUN_24dd_0530();

    while (((*(uint8_t *)((uStack_6 >> 8) + 0x783b)) = 0), (uStack_6 & 0xFFFF) != 0xAB) {
        uStack_6 = (((uStack_6 & 0xFF00) | ((uStack_6 & 0xFF) + 1)) << 8) & 0xFFFF;
    }

    do {
        FUN_24ba_00d8();
    } while (extraout_AL == '\0');

    uStack_6 = ((uStack_6 & 0xFF00) | 0x100);

    while (true) {
        iVar2 = uStack_6 & 0xFFFF;
        if (*(uint8_t *)(iVar2 + 0x783b) != '\0') {
            uVar1 = uStack_6 >> 8;
            uStack_6 = ((uVar1 << 8) | (uStack_6 & 0xFF)) | ((uStack_6 & 0xFF00) >> 8);
            *(uint8_t *)(iVar2 + 0x783b) = 0;
        }
        if ((uStack_6 & 0xFFFF) == 0xAB) break;
        uStack_6 = (((uStack_6 & 0xFF00) | ((uStack_6 & 0xFF) + 1)) << 8) & 0xFFFF;
    }

    return ((uint16_t)extraout_AH << 8) | (uStack_6 >> 8);
}
