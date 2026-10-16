/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0d88
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_1ec2_0d88(uint8_t param_1, int param_2, int param_3, uint8_t *param_4) {
    uint8_t *puVar1;
    int iVar2;
    uint8_t *puVar3;
    uint8_t *puVar4;

    iVar2 = param_3 - 2;
    puVar3 = param_4;
    puVar4 = puVar3;
    puVar3 = puVar3 + (0x140 - param_3);
    for (; param_2 != 0; param_2--) {
        puVar1 = puVar4;
        puVar4 = puVar4 + 1;
        *puVar1 = param_1;
    }
    puVar4 = puVar3;
    puVar3 = puVar3 + (0x140 - param_3);
    for (; param_2 != 0; param_2--) {
        puVar1 = puVar4;
        puVar4 = puVar4 + 1;
        *puVar1 = param_1;
    }
    puVar4 = puVar3;
    puVar3 = puVar3 + (0x140 - param_3);
    for (; param_2 != 0; param_2--) {
        puVar1 = puVar4;
        puVar4 = puVar4 + 1;
        *puVar1 = param_1;
    }
    return;
}
