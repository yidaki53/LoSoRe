/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0000
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_1ec2_0000(uint param_1, undefined4 *param_2, undefined4 *param_3) {
    undefined4 *puVar1;
    undefined4 *puVar2;
    undefined4 *puVar3;
    undefined4 *puVar4;

    puVar3 = param_3;
    puVar4 = param_2;
    for (param_1 = param_1 >> 2; param_1 != 0; param_1--) {
        puVar2 = puVar4;
        puVar4 = puVar4 + 1;
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar2 = *puVar1;
    }
    return;
}
