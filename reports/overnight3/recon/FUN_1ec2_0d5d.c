/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0d5d
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_1ec2_0d5d(byte param_1, int param_2, int param_3, byte *param_4) {
    int iVar1;
    byte *pbVar2;
    byte *pbVar3;

    pbVar3 = param_4;
    iVar1 = param_3;
    do {
        for (; iVar1 != 0; iVar1--) {
            pbVar2 = pbVar3;
            pbVar3 = pbVar3 + 1;
            *pbVar2 = param_1;
        }
        param_4 = param_4 + (0x140 - param_3);
        iVar1 = param_3;
    } while (param_2 != 0);
    return;
}
