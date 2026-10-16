/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_01df
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declarations of external functions
void FUN_1ec2_0dc8(uint16_t uVar6, uint16_t uVar7, uint16_t value, int param5, int param6);
void FUN_1ec2_0e06(uint16_t uVar6, uint16_t uVar7, uint16_t value, int param5, int param6);

void FUN_1ec2_01df(char param_1, char param_2, uint32_t param_3, uint8_t *param_4, int param_5, int param_6) {
    uint8_t local_102[256];
    uint8_t *puVar5 = local_102;
    uint8_t *puVar4 = param_4;
    int iVar3;
    uint16_t uVar6 = (uint16_t)param_3;
    uint16_t uVar7 = (uint16_t)(param_3 >> 16);
    int local_108;
    int local_104;

    // Copy data from param_4 to local_102
    for (iVar3 = 0x100; iVar3 != 0; iVar3--) {
        *puVar5++ = *puVar4++;
    }

    if (param_1 == '\0') {
        if (param_2 == '\0') {
            local_108 = 0;
            while (true) {
                for (local_104 = 2;
                     FUN_1ec2_0dc8(uVar6, uVar7,
                                   ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104],
                                   param_5 + local_108,
                                   (0xe - local_104) + param_6),
                     local_104 != 0xb; local_104++) {
                }
                if (local_108 == 8) break;
                local_108++;
            }
        } else {
            local_108 = 0;
            while (true) {
                for (local_104 = 2;
                     FUN_1ec2_0dc8(uVar6, uVar7,
                                   ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104],
                                   param_5 + local_108,
                                   param_6 + local_104),
                     local_104 != 0xb; local_104++) {
                }
                if (local_108 == 8) break;
                local_108++;
            }
        }
    } else if (param_1 == '\x01') {
        if (param_2 == '\0') {
            local_108 = 0;
            while (true) {
                for (local_104 = 2;
                     FUN_1ec2_0e06(uVar6, uVar7,
                                   ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104],
                                   param_5 + local_108,
                                   (0xe - local_104) + param_6),
                     local_104 != 0xb; local_104++) {
                }
                if (local_108 == 8) break;
                local_108++;
            }
        } else {
            local_108 = 0;
            while (true) {
                for (local_104 = 2;
                     FUN_1ec2_0e06(uVar6, uVar7,
                                   ((uint16_t)((uint8_t)(local_104 >> 8)) << 8) | local_102[local_108 * 0x10 + local_104],
                                   param_5 + local_108,
                                   param_6 + local_104),
                     local_104 != 0xb; local_104++) {
                }
                if (local_108 == 8) break;
                local_108++;
            }
        }
    }
}
