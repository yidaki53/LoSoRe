/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3fde
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declarations of external functions
void FUN_24dd_3ed3(int param_1, int param_2, uint16_t param_3, uint16_t param_4);
void FUN_24dd_3f14(int param_1, int param_2);
void FUN_24dd_3eaf(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint8_t *param_4, uint16_t param_5);

void FUN_24dd_3fde(int param_1, uint16_t param_2, uint32_t param_3, uint32_t param_4) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar5;
    uint8_t *puVar3;
    uint8_t *puVar4;
    uint8_t local_202[256];
    uint8_t local_102[256];

    if (param_1 < 1) {
        param_1 = 1;
    }

    puVar4 = local_102;
    uVar2 = (uint16_t)(param_3 >> 16);
    uVar1 = (uint16_t)param_3;
    uVar5 = 0; // Placeholder for unaff_SS, assuming it's not used elsewhere

    FUN_24dd_3ed3(param_1 - 1, 1, uVar1, uVar2);
    FUN_24dd_3f14((int)param_4, (int)(param_4 >> 16));
    puVar3 = local_202;
    FUN_24dd_3ed3(0xff, param_1, uVar1, uVar2);
    FUN_24dd_3f14((int)puVar3, uVar5);
    FUN_24dd_3eaf(param_2, uVar1, uVar2, puVar4, uVar5);
}
