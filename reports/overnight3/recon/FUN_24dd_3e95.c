/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3e95
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_24dd_3e95(byte *param_1, byte *param_2) {
    byte bVar1;
    uint uVar2;
    byte *pbVar3;
    byte *pbVar4;

    pbVar4 = param_2;
    pbVar3 = param_1;
    bVar1 = *param_1;
    *param_2 = bVar1;
    uVar2 = (uint)bVar1;
    while (true) {
        pbVar4 = pbVar4 + 1;
        pbVar3 = pbVar3 + 1;
        if (uVar2 == 0) break;
        uVar2 = uVar2 - 1;
        *pbVar4 = *pbVar3;
    }
    return;
}
