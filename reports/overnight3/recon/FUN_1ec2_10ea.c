/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_10ea
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=3 phi=3 verdict=contested
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_1ec2_10cf(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t);

void FUN_1ec2_10ea(int param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *pbVar5 = param_2;
    uint8_t *pbVar4 = local_302;
    int iVar3 = 0x300;

    while (iVar3 != 0) {
        *pbVar4++ = *pbVar5++;
        iVar3--;
    }

    uint8_t local_303 = 0;
    while (true) {
        uint local_306 = (uint8_t)local_302[(uint16_t)local_303 * 3] * param_1 >> 5;
        uint local_308 = (uint8_t)local_302[(uint16_t)local_303 * 3 + 1] * param_1 >> 5;
        uint local_30a = (uint8_t)local_302[(uint16_t)local_303 * 3 + 2] * param_1 >> 5;
        uint local_30e = (uint8_t)local_302[(uint16_t)local_303 * 3 + 1] * param_1 >> 5;

        if (local_303 == 0xff) break;

        FUN_1ec2_10cf(local_306, local_308, local_30a, local_30e, local_303, 0, 0, 0);
    }
}
