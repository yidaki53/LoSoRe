/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_0673
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern int __stdcall16far FUN_202c_0673(uint16_t *param_1);

int __stdcall16far FUN_202c_0673(uint16_t *param_1) {
    uint8_t *pbVar3 = (uint8_t *)param_1;
    uint8_t local_104[258];
    uint8_t *pbVar1;
    uint uVar2;
    int local_108;
    uint local_106;

    local_104[0] = *param_1;
    pbVar1 = local_104;
    for (uVar2 = local_104[0]; uVar2 != 0; uVar2--) {
        *pbVar1++ = *pbVar3++;
    }
    local_108 = 1;
    if (local_104[0] != 0) {
        local_106 = 1;
        while (1) {
            if (local_104[local_106] == 0xff) {
                local_106 += 2;
            }
            local_108 += (uint8_t)((local_104[local_106] - 2) * 0x40 + 0x19e5);
            if (local_106 == local_104[0]) break;
            local_106++;
        }
    }
    return local_108 + 2;
}
