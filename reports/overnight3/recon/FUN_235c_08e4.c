/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_08e4
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_2494_0050(uint16_t param_1);
void FUN_24dd_485f(uint8_t param_1, uint16_t param_2, uint16_t param_3);

void __stdcall16far FUN_235c_08e4(uint16_t *param_1) {
    uint16_t uVar1;
    uint16_t *base_address;

    if (*(char *)(0x7688) == '\0') {
        FUN_2494_0050(*param_1);
    }

    base_address = (uint16_t *)((int)param_1 >> 16);
    uVar1 = *param_1;
    FUN_24dd_485f(10, *base_address, *(base_address + 1));
    *param_1 = 0;
    *(param_1 + 1) = 0;
    return;
}
