/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_00a5
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void FUN_1ec2_00a5(int param_1, int param_2, undefined1 *param_3, undefined1 *param_4) {
    undefined1 *puVar1;
    undefined1 *puVar2;
    int iVar3;
    int iVar4;

    iVar4 = param_2;
    puVar2 = param_3;
    puVar1 = param_4;
    while (param_1 != 0) {
        iVar3 = iVar4;
        do {
            puVar2 = puVar2 + 1;
            puVar1 = puVar1 + 1;
            iVar3 = iVar3 - 1;
        } while (iVar3 != 0);
        param_1 = param_1 - 1;
        iVar4 = -0x142;
    }
    return;
}
