/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_12ad
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_1ec2_12ad(void *param_1, int param_2, uint param_3, uint param_4, uint param_5) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)(uint32_t)param_5 >> 16;
    puVar3 = (uint16_t *)((uint16_t)param_5 + param_2 * 0x140 + (param_4 >> 1));
    uVar2 = param_4 >> 1;
    if (param_4 & 1) {
        puVar1 = puVar3;
        puVar3 = (uint16_t *)((uint16_t)puVar3 + 1);
        *(uint8_t *)puVar1 = (uint8_t)param_3;
    }
    while (uVar2 != 0) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar1 = (uint16_t)param_3;
    }
    uVar4 = (uint16_t)(uint32_t)param_5 >> 16;
    puVar3 = (uint16_t *)((uint16_t)param_5 + param_2 * 0x140 - param_4);
    uVar2 = param_4 >> 1;
    if (param_4 & 1) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *(uint8_t *)puVar1 = (uint8_t)param_3;
    }
    while (uVar2 != 0) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar1 = (uint16_t)param_3;
    }
    return;
}
