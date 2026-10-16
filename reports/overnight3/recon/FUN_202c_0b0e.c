/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_0b0e
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_202c_0843(uint8_t *param_1, uint16_t seg);
extern void FUN_24dd_3b22(uint8_t *param_1, uint16_t seg, uint8_t *param_2, uint16_t seg2);
extern void FUN_24dd_3b5d(uint8_t param_1, uint8_t *param_2, uint16_t seg);
extern void FUN_24dd_04f4(void);
extern void FUN_24dd_3c48(uint8_t *param_1, uint16_t seg, uint16_t param_2, int param_3, int param_4, uint8_t *param_5, uint16_t seg2);
extern void FUN_24dd_3bde(uint8_t *param_1, uint16_t seg);

uint16_t FUN_202c_0b0e(uint16_t param_1, uint8_t *param_2) {
    uint8_t *pbVar7 = param_2;
    uint8_t local_104 = *param_2;
    uint8_t abStack_103[256];
    uint8_t *pbVar2 = abStack_103;
    uint8_t local_184[128];
    int local_186;
    uint8_t local_188[2];
    uint8_t local_3;
    uint8_t uVar5;
    uint8_t extraout_AH;
    uint32_t uVar3;
    uint16_t uVar4;
    uint uVar6;

    for (uVar6 = (uint)local_104; uVar6 != 0; uVar6--) {
        *pbVar2++ = *pbVar7++;
    }

    uVar4 = FUN_202c_0843(&local_104, 0); // Assuming unaff_SS is 0
    local_3 = (char)uVar4;
    uVar5 = (uint8_t)(uVar4 >> 8);

    if (local_3 != '\0') {
        FUN_24dd_3b22(&local_104, 0, local_184, 0);
        FUN_24dd_3b5d(1, local_184, 0);
        FUN_24dd_04f4();
        local_186 = 0;

        while (local_186 <= 0x15d) {
            uVar3 = *(uint32_t *)((int)*(uint32_t *)0x6674 + local_186 * 4);
            FUN_24dd_3c48(local_188, 0, 0x1f8, (int)uVar3, (int)((uint32_t)uVar3 >> 0x10), local_184, 0);
            FUN_24dd_04f4();
            local_186++;
        }

        FUN_24dd_3bde(local_184, 0);
        FUN_24dd_04f4();
        uVar5 = extraout_AH;
    }

    return (uint16_t)((uint16_t)uVar5 << 8 | (uint16_t)local_3);
}
