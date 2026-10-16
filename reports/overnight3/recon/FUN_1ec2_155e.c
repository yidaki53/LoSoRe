/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_155e
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_1ec2_155e(uint16_t param_1) {
    uint8_t local_3 = 0;
    
    while (true) {
        uint16_t uVar2 = (uint16_t)(uint8_t)local_3;
        uint16_t uVar6 = uVar2 * 3;
        uint16_t uVar8 = uVar2 * 3 + 1;
        uint16_t uVar4 = uVar2 * 3 + 2;
        
        uint16_t *ptr1 = (uint16_t *)((int16_t)param_1 * 16 + uVar6);
        uint16_t *ptr2 = (uint16_t *)((int16_t)param_1 * 16 + uVar8);
        uint16_t *ptr3 = (uint16_t *)((int16_t)param_1 * 16 + uVar4);
        
        uint8_t *data1 = (uint8_t *)((int16_t)param_1 * 16 + uVar2 * 4);
        uint8_t *data2 = (uint8_t *)((int16_t)param_1 * 16 + uVar2 * 4 + 1);
        
        FUN_2971_65df(*data1, *data2, *ptr1, *ptr2, *ptr3, local_3);
        
        if (local_3 == 0xff) break;
        
        local_3++;
    }
}
