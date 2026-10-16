/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0810
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declaration of external function
void __stdcall16far FUN_1ec2_10cf(uint8_t, uint8_t, uint8_t, uint8_t);

void __stdcall16far FUN_1ec2_0810(uint8_t param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *puVar5 = local_302;
    uint8_t *puVar4 = param_2;
    
    for (int iVar3 = 0x300; iVar3 != 0; iVar3--) {
        *puVar5 = *puVar4;
        puVar5++;
        puVar4++;
    }
    
    FUN_1ec2_10cf(local_302[(uint8_t)param_1 * 3 + 2],
                  local_302[(uint8_t)param_1 * 3 + 1],
                  local_302[(uint8_t)param_1 * 3],
                  param_1);
}
