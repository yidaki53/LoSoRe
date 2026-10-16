/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4161
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=3 verdict=contested
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

int16_t __cdecl16far FUN_24dd_4161(uint16_t in_AX, uint16_t in_DX) {
    int8_t sVar1;
    uint8_t bVar2;
    uint8_t bVar3;

    bVar2 = (uint8_t)(in_AX >> 3);
    bVar3 = (uint8_t)(in_DX >> 8);
    if ((bVar3 <= bVar2) && ((uint8_t)(bVar2 - bVar3) < (uint8_t)in_DX)) {
        sVar1 = (int8_t)(in_AX & 0xff07);
        bVar2 = (uint8_t)((in_AX & 0xff07) >> 8);
        return ((uint16_t)bVar2 << 8) | (bVar2 << sVar1) | (bVar2 >> (8 - sVar1));
    }
    return (int16_t)(in_AX >> 0xf);
}
