/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_15bb
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declaration of external function
void __stdcall16far FUN_1ec2_152f(int param1, uint16_t param2, int param3, uint16_t param4, int param5, uint16_t param6, byte* param7, uint16_t param8);

void __stdcall16far FUN_1ec2_15bb(uint32_t param_1) {
    int iVar1;
    uint16_t uVar2;
    uint8_t local_3 = 0;

    while (true) {
        uVar2 = (uint16_t)(param_1 >> 0x10);
        iVar1 = (int)param_1;
        FUN_1ec2_152f(iVar1 + local_3 * 3 + 2, uVar2, iVar1 + local_3 * 3 + 1, uVar2, iVar1 + local_3 * 3, uVar2, &local_3, 0);
        if (local_3 == 0xff) {
            break;
        }
        local_3++;
    }
}
