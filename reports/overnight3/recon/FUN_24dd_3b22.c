/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3b22
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_3b22(uint8_t *param_1, uint16_t *param_2) {
    uint8_t *pbVar6 = (uint8_t *)(param_2 + 1);
    *param_2 = 0;
    pbVar6[0] = 0xb0;
    pbVar6[1] = 0xd7;
    
    for (int iVar3 = 0x16; iVar3 != 0; iVar3--) {
        pbVar6[0] = 0;
        pbVar6[1] = 0;
        pbVar6 += 2;
    }
    
    uint8_t *pbVar5 = param_1 + 1;
    uint32_t uVar4 = (uint32_t)*param_1;
    
    if (0x4e < *param_1) {
        for (uVar4 = (uint32_t)*param_1; uVar4 != 0; uVar4--) {
            uint8_t *pbVar1 = pbVar5;
            pbVar5++;
            if (*pbVar1 == 0) break;
            *pbVar6++ = *pbVar1;
        }
    }
    
    *pbVar6 = 0;
}
