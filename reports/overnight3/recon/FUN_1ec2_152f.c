/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_152f
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void out(uint16_t port, uint8_t value);
uint8_t in(uint16_t port);

void __stdcall16far FUN_1ec2_152f(uint8_t *param_1, uint8_t *param_2, uint8_t *param_3, uint8_t *param_4) {
    uint8_t uVar1;

    out(0x3c7, *param_4);
    uVar1 = in(0x3c9);
    *param_3 = uVar1;
    uVar1 = in(0x3c9);
    *param_2 = uVar1;
    return;
}
