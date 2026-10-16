/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_1519
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_1519(void) {
    uint16_t *puVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    int32_t iVar7;
    uint32_t uVar8;
    uint32_t uVar9;
    int32_t iVar10;
    int32_t iVar11;
    uint32_t uVar12;

    puVar1 = (uint16_t *)*(uint16_t *)0xd8;
    uVar9 = puVar1[3];
    uVar6 = puVar1[2];
    uVar8 = puVar1[1];
    iVar11 = (int32_t)puVar1[4] >> 1;
    uVar3 = uVar6;
    if ((puVar1[4] & 1) != 0) {
        iVar11 = iVar11 + 1;
        uVar3 = uVar9 & 1;
        uVar9 = uVar9 >> 1;
        uVar3 = (uint32_t)(((uVar3 != 0) << 15) | (uVar6 >> 1));
        uVar8 = (uint32_t)(((uVar6 & 1) != 0) << 15) | (uVar8 >> 1);
    }
    if (uVar9 < 0xfffe) {
        uVar6 = (uint32_t)(((uint32_t)uVar9 | 0x10000) >> 1);
        while (true) {
            uVar4 = (uint32_t)(((uint32_t)uVar9 << 16) | uVar3) / (uint32_t)uVar6;
            if (uVar6 - 1 <= uVar4) break;
            uVar6 = (uint32_t)(((uint32_t)uVar6 + uVar4) >> 1);
            if (((uint32_t)uVar6 + uVar4) < uVar6) uVar6 |= 0x8000;
        }
        uVar5 = uVar4;
        uVar12 = uVar6;
        if (uVar6 < uVar4) {
            uVar5 = uVar6;
            uVar12 = uVar4;
        }
        uVar2 = (((uint32_t)uVar9 << 16) | uVar3) % (uint32_t)uVar6;
        uVar2 = (uVar2 << 16) | uVar8;
        uVar2 /= (uint32_t)uVar12;
        uVar6 = (uint32_t)(((uint32_t)uVar12 + uVar5 & 1) << 15) | (uVar2 & 0xffff);
        uVar6 >>= 1;
        uVar9 = (uint32_t)(uVar2 & 1);
        iVar7 = uVar6 + uVar9;
        iVar10 = (int32_t)(((uint32_t)uVar12 + uVar5) >> 1);
        if (((uint32_t)uVar12 + uVar5) < uVar12) iVar10 |= 0x8000;
        if (((uint32_t)uVar6 + uVar9) < uVar6) iVar10++;
    } else {
        iVar10 = (int32_t)(((uint32_t)uVar9 | 0x10000) >> 1);
        iVar7 = (int32_t)(((uint32_t)uVar9 & 1) << 15) | (uVar3 >> 1);
    }
    puVar1[0] = 0;
    puVar1[1] = 0;
    puVar1[2] = (uint16_t)iVar7;
    puVar1[3] = (uint16_t)iVar10;
    puVar1[4] = (uint16_t)iVar11;
    puVar1[5] = 0;
    return;
}
