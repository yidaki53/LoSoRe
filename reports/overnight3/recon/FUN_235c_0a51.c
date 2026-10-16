/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0a51
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_235c_091d(uint16_t param_1);

void FUN_235c_0a51(void) {
    uint8_t local_3 = 0;
    
    while (true) {
        if (*(char *)(0x67fc + local_3) != '\0') {
            uint32_t uVar4 = *(uint32_t *)((uint32_t)local_3 * 10 + 0x6804);
            uint16_t uVar6 = (uint16_t)(uVar4 >> 16);
            int iVar5 = (int)uVar4;
            int iVar1 = *(int *)(iVar5 + 8);
            uint32_t uVar2 = *(uint32_t *)((uint32_t)local_3 * 10 + 0x6809);
            int iVar3 = *(int *)((uint32_t)local_3 * 10 + 0x680b);
            
            if ((iVar1 < iVar3) || ((iVar1 <= iVar3 && (*(uint32_t *)(iVar5 + 6) <= uVar2)))) {
                FUN_235c_091d(iVar1);
            }
            
            *(char *)0x67ce = *(char *)0x67ce - 1;
        }
        
        if (local_3 == 7) break;
        
        local_3 = local_3 + 1;
    }
}
