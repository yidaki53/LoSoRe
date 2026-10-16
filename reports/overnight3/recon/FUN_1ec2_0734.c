/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0734
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declaration of external function
void FUN_1ec2_0e4a(int param1, uint16_t param2, int param3, int param4);

void FUN_1ec2_0734(char param_1, uint32_t param_2, char *param_3, int param_4, int param_5) {
    char local_102[256];
    char *pcVar5 = local_102;
    char *pcVar4 = param_3;
    int iVar3;

    // Copy 256 bytes from param_3 to local_102
    for (iVar3 = 0x100; iVar3 != 0; iVar3--) {
        *pcVar5 = *pcVar4;
        pcVar5++;
        pcVar4++;
    }

    uint16_t uVar6 = (uint16_t)(param_2 >> 0x10);

    if (param_1 == '\0') {
        for (int local_108 = 0; local_108 < 9; local_108++) {
            for (int local_104 = 2; local_104 <= 0xb; local_104++) {
                if (local_102[local_108 * 0x10 + local_104] != '\0') {
                    FUN_1ec2_0e4a((int)param_2, uVar6, param_4 + local_108, (0xe - local_104) + param_5);
                }
            }
        }
    } else {
        for (int local_108 = 0; local_108 < 9; local_108++) {
            for (int local_104 = 2; local_104 <= 0xb; local_104++) {
                if (local_102[local_108 * 0x10 + local_104] != '\0') {
                    FUN_1ec2_0e4a((int)param_2, uVar6, param_4 + local_108, param_5 + local_104);
                }
            }
        }
    }
}
