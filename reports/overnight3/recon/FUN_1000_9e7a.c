/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_9e7a
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_0530(void);

uint16_t FUN_1000_9e7a(void) {
    uint16_t uVar1;
    uint8_t bVar2;
    int iVar3;
    uint16_t uVar4;
    uint16_t *base_address = (uint16_t *)0x6670;
    uint8_t *data_ptr = (uint8_t *)0x66ac;
    uint16_t *param_1 = (uint16_t *)0x66a1;
    uint16_t *param_2 = (uint16_t *)0x66a3;
    uint16_t *param_5 = (uint16_t *)0x66a5;
    uint16_t *param_6 = (uint16_t *)0x66a8;
    uint16_t *param_7 = (uint16_t *)0x66aa;
    uint16_t *param_9 = (uint16_t *)0x66b3;
    uint16_t *param_10 = (uint16_t *)0x66b6;
    uint16_t *param_11 = (uint16_t *)0x66b8;

    uVar1 = FUN_24dd_0530();
    if (*data_ptr == '\0') {
        if (*(int *)(*base_address + 0x3a) != 0) {
            if (*(uint16_t *)(*base_address + 0x38) != 1) {
                if (*(uint16_t *)(*base_address + 0xe4) != 0) {
                    if (*(uint16_t *)(*base_address + 0xe2) != 1) {
                        bVar2 = 0;
                    } else {
                        bVar2 = 1;
                    }
                } else {
                    bVar2 = 1;
                }
            } else {
                bVar2 = 1;
            }
        } else {
            bVar2 = 1;
        }
    } else {
        bVar2 = 1;
    }

    if (bVar2 == 0) {
        uVar4 = (uint16_t)((uint32_t)*param_1 >> 16);
        if ((-(int)((uint32_t)*param_1 & 0xFFFF) - 1 < *(int *)(*base_address + 0x46)) ||
            (-(int)((uint32_t)*param_2 & 0xFFFF) - 1 < *(int *)(*base_address + 0x44)) ||
            (-(int)((uint32_t)*param_5 & 0xFFFF) - 1 < *(int *)(*base_address + 0xf0)) ||
            (-(int)((uint32_t)*param_6 & 0xFFFF) - 1 < *(int *)(*base_address + 0xee)) ||
            (-(int)((uint32_t)*param_7 & 0xFFFF) - 1 < *(int *)(*base_address + 0xea))) {
            bVar2 = 0;
        }
    } else if ((bVar2 == 1) && (uVar4 != 0)) {
        uVar1 = 0;
    }

    if (bVar2 == 0) {
        uVar4 = (uint16_t)((uint32_t)*param_9 >> 16);
        if ((-(int)((uint32_t)*param_10 & 0xFFFF) - 1 < *(int *)(*base_address + 0x42)) ||
            (-(int)((uint32_t)*param_11 & 0xFFFF) - 1 < *(int *)(*base_address + 0x40))) {
            bVar2 = 0;
        }
    } else if ((bVar2 == 1) && (uVar4 != 0)) {
        uVar1 = 0;
    }

    if (bVar2 == 0) {
        return 0;
    }

    return 1;
}
