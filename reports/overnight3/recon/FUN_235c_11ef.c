/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_11ef
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_235c_0000(uint16_t);

void FUN_235c_11ef(void) {
    uint16_t *ptr_67de = (uint16_t *)(0x67de);
    uint8_t *ptr_67ee = (uint8_t *)(0x67ee);
    uint16_t *ptr_67e0 = (uint16_t *)(0x67e0);
    uint16_t *ptr_67e2 = (uint16_t *)(0x67e2);
    uint8_t *ptr_67ef = (uint8_t *)(0x67ef);
    uint16_t *ptr_67e4 = (uint16_t *)(0x67e4);
    uint8_t *ptr_6854 = (uint8_t *)(0x6854);
    uint16_t *ptr_67e6 = (uint16_t *)(0x67e6);
    uint16_t *ptr_67f0 = (uint16_t *)(0x67f0);
    uint16_t *ptr_67e8 = (uint16_t *)(0x67e8);
    uint8_t *ptr_67ed = (uint8_t *)(0x67ed);

    out(*ptr_67de, *ptr_67ee);
    out(*ptr_67e0, 0);
    out(*ptr_67e2, *ptr_67ef);
    out(*ptr_67e4, *(uint8_t *)((uint8_t)*ptr_6854 * 2 + 0x6e80));
    out(*ptr_67e4, *(uint8_t *)((uint8_t)*ptr_6854 * 2 + 0x6e81));
    out(*ptr_67e6, (char)*ptr_67f0 - 1);
    out(*ptr_67e6, (char)((int16_t)(*ptr_67f0 - 1) >> 8));
    out(*ptr_67e8, *(uint8_t *)(*(uint8_t *)ptr_6854 + 0x6e7f));
    out(*ptr_67de, *ptr_67ed);
    FUN_235c_0000(0x14);
    FUN_235c_0000(0xffff);
    FUN_235c_0000(1);
}

// Note: The `out` function is assumed to be defined elsewhere, as it is not provided in the pseudocode.
