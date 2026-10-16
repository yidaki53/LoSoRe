/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_13b0
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_1ec2_13b0(void *param_1, void *param_2) {
    int iVar1;
    uint16_t *puVar2;
    uint16_t *puVar3;

    puVar2 = (uint16_t *)param_2;
    puVar3 = (uint16_t *)param_1;
    for (iVar1 = 16000; iVar1 != 0; iVar1 = iVar1 + -1) {
        puVar3 = puVar3 + 1;
        puVar2 = puVar2 + 1;
    }
    return;
}
