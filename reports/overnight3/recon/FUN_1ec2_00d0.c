/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_00d0
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = lenient
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_3dbd(void);
extern void FUN_24dd_3eaf(uint8_t, uint8_t*, uint16_t, uint8_t, uint16_t);
extern void FUN_24dd_3e95(uint8_t*, uint16_t);
extern void FUN_202c_076d(uint16_t, int);
extern void FUN_24dd_3f14(uint8_t*, uint16_t);

void __stdcall16far FUN_1ec2_00d0(uint16_t param_1, int param_2, uint32_t param_3) {
    uint16_t uVar1 = 0x3c;
    int iVar2 = 0;
    uint16_t local_6 = FUN_24dd_3dbd();
    int local_4 = param_2;
    uint8_t local_c[6] = {0};
    uint8_t local_20c[256];
    uint8_t local_10c[256];
    uint16_t unaff_SS = 0; // Assuming unaff_SS is initialized to 0 or some known value

    FUN_24dd_3dbd();
    if ((local_4 < 0) || ((local_4 < 1 && (local_6 < 10)))) {
        FUN_24dd_3eaf(5, local_c, unaff_SS, 0xcc, 0x24dd);
    }

    uint8_t* puVar5 = local_20c;
    uint16_t uVar6 = unaff_SS;
    FUN_24dd_3e95(local_c, unaff_SS);
    uint8_t* puVar3 = local_10c;
    uint16_t uVar4 = unaff_SS;
    FUN_202c_076d(local_6, local_4);
    FUN_24dd_3f14(puVar3, uVar4);
    FUN_24dd_3f14(0xce, 0x24dd);
    FUN_24dd_3eaf(5, local_c, unaff_SS, puVar5, uVar6);

    if ((iVar2 < 0) || ((iVar2 < 1 && (uVar1 < 10)))) {
        puVar5 = local_10c;
        uVar4 = unaff_SS;
        FUN_24dd_3e95(local_c, unaff_SS);
        FUN_24dd_3f14(0xcc, 0x24dd);
        FUN_24dd_3eaf(5, local_c, unaff_SS, puVar5, uVar4);
    }

    puVar5 = local_20c;
    uVar6 = unaff_SS;
    FUN_24dd_3e95(local_c, unaff_SS);
    puVar3 = local_10c;
    uVar4 = unaff_SS;
    FUN_202c_076d(uVar1, iVar2);
    FUN_24dd_3f14(puVar3, uVar4);
    FUN_24dd_3eaf(5, local_c, unaff_SS, puVar5, uVar6);
    FUN_24dd_3eaf(0xff, (int)param_3, (int)((uint32_t)param_3 >> 0x10), local_c, unaff_SS);
}
