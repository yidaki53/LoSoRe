/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1e7d_0082
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>
#include <string.h>

extern uint16_t FUN_24dd_3eaf(uint8_t, uint8_t*, uint16_t, uint8_t*, uint16_t);
extern uint16_t FUN_24dd_3fb1(uint16_t);
extern int FUN_24dd_3f40(uint8_t*, uint16_t, uint8_t*, uint16_t);
extern void FUN_24dd_403d(uint16_t, uint16_t, uint8_t*, uint16_t);
extern uint16_t FUN_24dd_3e95(uint8_t, uint16_t);
extern void FUN_24dd_3fde(uint8_t, uint8_t, uint8_t*, uint16_t, uint8_t*, uint16_t);
extern uint16_t FUN_24dd_4824(int*, uint16_t, uint8_t*, uint16_t);

uint16_t FUN_1e7d_0082(char param_1, uint8_t param_2, uint8_t* param_3) {
    uint8_t local_408[254];
    uint8_t local_30a[2];
    uint8_t local_308[256];
    int local_208[2];
    uint8_t local_204[256];
    uint8_t local_104;
    uint8_t abStack_103[255];
    uint16_t local_4 = 0;
    uint8_t* pbVar6 = param_3;
    uint8_t* pbVar2 = abStack_103;
    uint8_t* pbVar1;
    uint16_t unaff_SS = 0; // Assuming unaff_SS is a constant or initialized elsewhere
    uint8_t extraout_AH = 0; // Assuming extraout_AH is set by FUN_24dd_3fb1

    local_104 = *param_3;
    for (uint uVar5 = local_104; uVar5 != 0; uVar5--) {
        *pbVar2++ = *pbVar6++;
    }

    FUN_24dd_3eaf(0xff, local_204, unaff_SS, &local_104, unaff_SS);

    uint16_t uVar4 = unaff_SS;
    FUN_24dd_3fb1((uint16_t)(extraout_AH | (param_2 << 8)));

    int iVar3 = FUN_24dd_3f40(local_204, unaff_SS, local_308, uVar4);
    if (iVar3 == 0) {
        local_4 = 0xff;
    } else {
        uint16_t uVar8 = 1;
        uint16_t uVar10 = unaff_SS;

        FUN_24dd_3fb1((uint16_t)(param_2 << 8));
        uVar4 = FUN_24dd_3f40(local_204, unaff_SS, local_408, uVar4);
        FUN_24dd_403d(uVar4, uVar8, local_204, uVar10);

        FUN_24dd_3e95(0x7e, 0x24dd);
        uVar4 = FUN_24dd_3f40(local_204, unaff_SS, local_30a, uVar4);
        FUN_24dd_403d(0xff, uVar4, local_204, uVar10);

        if (param_1 != '\0') {
            FUN_24dd_3e95(0x80, 0x24dd);
            FUN_24dd_3fde(1, 0xff, local_204, unaff_SS, local_30a, uVar4);
        }

        local_4 = FUN_24dd_4824(local_208, unaff_SS, local_204, unaff_SS);
        if (local_208[0] != 0) {
            local_4 = 0xff;
        }
    }

    return local_4;
}
