/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_40d6
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_24dd_40d6(uint16_t param_1, uint16_t *param_2) {
    int iVar1;
    uint16_t *puVar2;

    puVar2 = param_2;
    *param_2 = param_1;
    for (iVar1 = 0xf; iVar1 != 0; iVar1--) {
        puVar2++;
        *puVar2 = 0;
    }
    return;
}
