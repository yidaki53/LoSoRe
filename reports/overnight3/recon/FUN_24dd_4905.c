/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_4905
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_24dd_4905(byte param_1, uint16_t param_2, byte *param_3) {
    int iVar1;
    byte *pbVar2;

    pbVar2 = param_3;
    for (iVar1 = param_2; iVar1 != 0; iVar1--) {
        *pbVar2 = param_1;
        pbVar2++;
    }
    return;
}
