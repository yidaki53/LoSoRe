/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_2fcd
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <stdbool.h>
#include <math.h>

extern void out(uint8_t, uint8_t);
extern uint16_t DAT_002c;
extern uint16_t DAT_7b40;
extern uint16_t DAT_7b3e;
extern uint8_t DAT_6421;

void FUN_24dd_2fcd(void) {
    int *piVar5 = (int *)0x0;
    uint16_t uVar4 = DAT_002c;
    int iVar3 = 0x7fff;
    bool bVar6;
    long double lVar7;
    long double lVar8;

    do {
        if (*piVar5 == 0) break;
        if (*piVar5 == 0x3738 && *(char *)(piVar5 + 1) == '=') {
            bVar6 = (((*(uint8_t *)(piVar5 + 1) >> 8) & 0xdf) == 0x59);
            goto LAB_24dd_3018;
        }
        bVar6 = true;
        do {
            if (iVar3 == 0) break;
            iVar3--;
            piVar5 = (int *)((int)piVar5 + 1);
            bVar6 = *piVar5 == 0;
        } while (!bVar6);
    } while (bVar6);

    out(0xf0, 0);
    DAT_7b40 = 0;
    DAT_7b40 = 0x37f;
    iVar3 = 0x14;
    do {
        iVar3--;
    } while (iVar3 != 0);

    bVar6 = ((DAT_7b40 & 0xf3f) == 0x33f);
LAB_24dd_3018:
    uVar4 = 0x1330;
    uint8_t uVar2 = 0;
    if (bVar6) {
        lVar8 = 1.0 / 0.0;
        lVar7 = -lVar8;
        DAT_7b40 = ((uint32_t)(lVar7 < lVar8) << 8) |
                   ((uint32_t)(isnan(lVar7) || isnan(lVar8)) << 10) |
                   ((uint32_t)(lVar7 == lVar8) << 14);
        uVar2 = 2;
        if ((DAT_7b40 & 0x4000) == 0) {
            uVar4 = 0x1332;
            uVar2 = 3;
        }
    }
    DAT_6421 = uVar2;
    DAT_7b3e = uVar4;
}
