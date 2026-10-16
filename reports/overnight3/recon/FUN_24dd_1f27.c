/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_1f27
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_0582(void);
extern void FUN_24dd_0ee2(int, uint16_t, uint16_t);
extern void FUN_24dd_1277(int, uint16_t, uint16_t);
extern void FUN_24dd_1371(void);
extern void FUN_24dd_1468(void);
extern void FUN_24dd_1563(void);
extern void FUN_24dd_1651(void);
extern void FUN_24dd_1749(void);
extern void FUN_24dd_1847(void);
extern void FUN_24dd_1935(void);
extern void FUN_24dd_1a33(void);
extern void FUN_24dd_1b30(void);
extern void FUN_24dd_1c28(void);
extern void FUN_24dd_1d26(void);
extern void FUN_24dd_1e24(void);
extern void FUN_24dd_1f27(void) {
    int *piVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    int *piVar4;
    uint16_t uVar5;
    int iVar6;
    int iVar7;
    uint16_t uVar8;
    int *piVar9;
    uint16_t uVar10;

    uVar10 = *(uint16_t *)0xd8;
    iVar6 = *(int *)(*(uint16_t *)0xd8 + 8);
    if (iVar6 < -0x40) {
        *(uint16_t *)0xd8 = uVar10 - 0xc;
        FUN_24dd_0582();
        uVar5 = *(uint16_t *)0xd8;
        puVar3 = (uint16_t *)0x0;
        while (true) {
            uVar8 = uVar10;
            uVar10 = uVar10 + 1;
            if (puVar3 != 0) break;
            puVar3 = (uint16_t *)*(uint16_t *)0x1dc9;
        }
        iVar7 = 0;
        while (true) {
            piVar9 = (int *)*(uint16_t *)0x1dc9;
            uVar2 = *(uint16_t *)0xd8;
            FUN_24dd_0ee2(iVar7, uVar2, uVar10);
            FUN_24dd_1277(iVar7, uVar2, uVar10);
            FUN_24dd_1371();
            FUN_24dd_1468();
            FUN_24dd_1563();
            FUN_24dd_1651();
            FUN_24dd_1749();
            FUN_24dd_1847();
            FUN_24dd_1935();
            FUN_24dd_1a33();
            FUN_24dd_1b30();
            FUN_24dd_1c28();
            FUN_24dd_1d26();
            FUN_24dd_1e24();
            piVar4 = piVar9;
            iVar7 = iVar7 + 1;
            if (piVar4 != 0) break;
        }
        *(int *)(*(uint16_t *)0xd8 + 8) = iVar6 + 1;
        *(uint16_t *)0xd8 = uVar10;
        return;
    }
    *(uint16_t *)0xd8 = uVar10;
    return;
}
