/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_48e1
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_24dd_48e1(int param_1, undefined1 *param_2, undefined1 *param_3) {
    undefined1 *puVar1;
    undefined1 *puVar2;
    undefined1 *puVar3;
    undefined1 *puVar4;

    puVar3 = param_3;
    puVar4 = param_2;
    if (param_3 < param_2) {
        puVar4 = puVar4 + param_1;
        puVar3 = puVar3 - param_1;
    }
    for (; param_1 != 0; param_1--) {
        puVar2 = puVar4;
        puVar4 = puVar4 + 1;
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar2 = *puVar1;
    }
    return;
}
