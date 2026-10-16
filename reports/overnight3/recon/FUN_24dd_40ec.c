/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_40ec
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_24dd_40ec(unsigned char param_1, int param_2) {
    unsigned char *ptr = (unsigned char *)(param_2 >> 16);
    *ptr = *ptr | (param_1 << (param_1 & 7));
}
