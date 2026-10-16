/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_095c
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_235c_095c(uint16_t param_1, uint16_t param_2, uint8_t param_3, uint8_t param_4) {
    uint8_t local_4 = 0xff;
    uint8_t local_3 = 0;

    while (true) {
        if (*(char *)(0x67fc + local_3) == '\0') {
            local_4 = local_3;
            break;
        }
        local_3++;
    }

    if (local_3 == 0xff) {
        return;
    }

    uint16_t uVar5 = (uint16_t)(local_3 * 10);
    uint16_t uVar6 = (uint16_t)(local_4 * 10);

    *(uint16_t *)(0x6804 + uVar5) = param_1;
    *(uint16_t *)(0x6806 + uVar5) = param_2;
    *(uint8_t *)(0x6808 + uVar5) = param_3;
    *(uint16_t *)(0x6809 + uVar5) = 0;
    *(uint16_t *)(0x680b + uVar5) = 0;
    *(uint8_t *)(0x680d + uVar5) = param_4;
    *(uint16_t *)(0x67fc + local_3) = 1;
}
