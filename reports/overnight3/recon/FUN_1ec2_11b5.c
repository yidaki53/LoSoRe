/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_11b5
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declaration of external function
void FUN_1ec2_10cf(uint16_t, uint16_t, uint16_t, uint16_t);

void FUN_1ec2_11b5(int param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *pbVar7 = local_302;
    uint8_t *pbVar6 = param_2;
    uint8_t local_303 = 0;

    // Copy 768 bytes from param_2 to local_302
    for (int iVar5 = 0x300; iVar5 != 0; iVar5--) {
        *pbVar7 = *pbVar6;
        pbVar7++;
        pbVar6++;
    }

    // Process each set of 3 bytes in local_302
    while (true) {
        uint local_306 = param_1 * 0x3f + (uint8_t)local_302[local_303 * 3] * (0x20 - param_1) >> 5;
        uint local_308 = param_1 * 0x3f + (uint8_t)local_302[local_303 * 3 + 1] * (0x20 - param_1) >> 5;
        uint uVar3 = param_1 * 0x3f + (uint8_t)local_302[local_303 * 3 + 2] * (0x20 - param_1);
        uint local_30a = uVar3 >> 5;

        // Clamp values to 0x3f
        if (local_306 > 0x3f) local_306 = 0x3f;
        if (local_308 > 0x3f) local_308 = 0x3f;
        if (local_30a > 0x3f) local_30a = 0x3f;

        uint8_t bVar4 = (uint8_t)(uVar3 >> 0xd);

        // Call external function with computed values
        FUN_1ec2_10cf(((uint16_t)bVar4 << 8) | (uint16_t)local_30a,
                      ((uint16_t)bVar4 << 8) | (uint16_t)local_308,
                      ((uint16_t)bVar4 << 8) | (uint16_t)local_306,
                      ((uint16_t)bVar4 << 8) | (uint16_t)local_303);

        if (local_303 == 0xff) break;
        local_303++;
    }
}
