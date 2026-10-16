/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_2e94
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_2e94(uint16_t param_1, uint16_t *param_2) {
    uint16_t uVar1;
    uint16_t *puVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint8_t bVar5;
    uint16_t uVar6;
    uint16_t uVar7;

    if ((param_1 & 2) != 0) {
        asm volatile (
            "sti"
            : "=si" (puVar2), "=ax" (uVar1)
            : "0" (param_2), "1" (0x8000)
            : "memory"
        );
        uVar4 = (uint16_t)((uint8_t)(param_1 >> 8));
        if ((param_1 & 0x80) != 0) {
            puVar2 = puVar2 - 2;
            uVar6 = *puVar2;
            uVar3 = uVar6 & 0xff;
            if ((uVar3 < 9) && ((uVar6 & 0x100) != 0)) {
                puVar2 = puVar2 - 2;
                uVar7 = *puVar2;
                bVar5 = (uint8_t)(uVar7 >> 8);
                if ((bVar5 == 0) || ((bVar5 & 0x80) != 0)) {
                    puVar2 = puVar2 - 2;
                    uVar1 = *puVar2;
                    *puVar2 = ((uint16_t)(uVar1 >> 8) << 16) | 0x9b90;
                }
            }
        } else if ((param_1 & 0x40) != 0) {
            puVar2 = puVar2 - 2;
            uVar1 = *puVar2;
            *puVar2 = ((uint16_t)(uVar1 >> 8) << 16) | 0x9b;
        }
    }
    return;
}
