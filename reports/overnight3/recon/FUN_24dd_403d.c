/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_403d
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declarations of external functions
void FUN_24dd_3ed3(uint8_t, uint8_t, uint16_t, uint16_t);
void FUN_24dd_3f14(uint8_t*, uint16_t);
void FUN_24dd_3eaf(uint8_t, uint16_t, uint16_t, uint8_t*, uint16_t);

void __stdcall16far FUN_24dd_403d(int param_1, int param_2, uint32_t param_3) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t unaff_SS;
    uint8_t *puVar3;
    uint8_t *puVar4;
    uint16_t uVar5;
    uint8_t local_202[256];
    uint8_t local_102[256];

    if ((param_1 > 0) && (param_2 > 0) && (param_2 < 0x100)) {
        if (param_1 > 0xff) {
            param_1 = 0xff;
        }
        puVar4 = local_102;
        uVar2 = (uint16_t)(param_3 >> 0x10);
        uVar1 = (uint16_t)param_3;
        uVar5 = unaff_SS;
        FUN_24dd_3ed3(param_2 - 1, 1, uVar1, uVar2);
        puVar3 = local_202;
        FUN_24dd_3ed3(0xff, param_2 + param_1, uVar1, uVar2);
        FUN_24dd_3f14(puVar3, unaff_SS);
        FUN_24dd_3eaf(0xff, uVar1, uVar2, puVar4, uVar5);
    }
}
