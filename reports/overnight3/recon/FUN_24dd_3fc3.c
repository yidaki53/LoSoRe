/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3fc3
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_24dd_3fc3(int param_1, undefined1 *param_2, undefined1 *param_3) {
    undefined1 *puVar1;
    undefined1 *puVar2;
    undefined1 *puVar3;

    puVar3 = param_3;
    puVar2 = param_2;
    *puVar3 = (char)param_1;
    for (; param_1 != 0; param_1--) {
        puVar1 = puVar2;
        puVar2 = puVar2 + 1;
        puVar3 = puVar3 + 1;
        *puVar3 = *puVar1;
    }
    return;
}
