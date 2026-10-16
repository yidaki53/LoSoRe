/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_0e06
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_1ec2_0e06(void *param_1, char param_2, int param_3, int param_4) {
    if (param_2 != '\0') {
        if ((param_4 >= -1 && param_4 < 0x9e) && (param_3 >= -1 && param_3 < 0x9e)) {
            if (param_2 < 0x27) {
                param_2 = param_2 + 9;
            }
            ((char *)((char *)param_1 + param_3 * 0x140 + param_4))[0] = param_2;
        }
    }
    return;
}
