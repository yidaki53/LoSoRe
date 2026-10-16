/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_047d
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = lenient
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_047d(uint16_t *cx, int bx, uint16_t *di, int es) {
    uint8_t bVar3;
    int iVar1;
    int iVar2;
    int iVar4;

    bVar3 = (uint8_t)((int)cx + cx[2]);
    if ((bx + cx[3] + (0xf < bVar3) != es) ||
        ((uint16_t)(((uint)((int)cx + cx[2]) >> 8) << 8) | (bVar3 - 0x10) & 0xff0f) != di) {
        *cx = di;
        cx[1] = es;
        return;
    }
    if ((es == *(int *)0x63f0) && (di == (uint16_t *)*(uint16_t *)0x63ee)) {
        *(uint16_t *)0x63ee = cx;
        *(int *)0x63f0 = bx;
        return;
    }
    *cx = *di;
    cx[1] = di[1];
    iVar1 = di[3];
    iVar4 = di[2] + cx[2];
    iVar2 = cx[3];
    bVar3 = (uint8_t)iVar4;
    cx[2] = ((uint16_t)(((uint)iVar4 >> 8) << 8) | (bVar3 - 0x10) & 0xff0f);
    cx[3] = iVar1 + iVar2 + (0xf < bVar3);
    return;
}
