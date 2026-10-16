/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_2361
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void swi(uint16_t);

uint16_t FUN_24dd_2361(uint16_t in_AX, uint16_t in_CX, uint16_t in_BX, uint16_t unaff_ES) {
    uint16_t uVar5;
    uint8_t bVar4;
    uint8_t bVar2;
    uint16_t uVar3;
    uint16_t *ptr_d0 = (uint16_t *)0xd0;
    uint16_t *ptr_d2 = (uint16_t *)0xd2;
    uint8_t *ptr_d4 = (uint8_t *)0xd4;
    uint8_t *ptr_d6 = (uint8_t *)0xd6;

    uVar5 = ((uint16_t)((uint8_t)(in_CX >> 8)) << 8) | *ptr_d6;
    bVar4 = (uint8_t)uVar5 ^ 0x3f;
    bVar2 = *ptr_d4 | (uint8_t)(uVar5 >> 8);
    if (((bVar2 & bVar4 ^ bVar2) & 8) != 0) {
        bVar2 = bVar2 | 0x20;
    }
    if ((bVar4 & bVar2) != 0) {
        *ptr_d4 = bVar2 | 0x80;
        if ((bVar2 & bVar4) == 0x20) {
            return in_AX;
        }
        swi(0x21);
        *ptr_d0 = in_BX;
        *ptr_d2 = unaff_ES;
        uVar3 = (*(uint16_t(*)())*ptr_d0)();
        return uVar3;
    }
    *ptr_d4 = bVar2 & 0x7f;
    return in_AX;
}
