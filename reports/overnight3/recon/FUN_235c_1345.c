/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_1345
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __cdecl16far FUN_235c_1345(void) {
    // Assuming 0x67f6 and 0x67f8 are addresses in the DS segment.
    // Assuming 0x6402 and 0x6404 are addresses in the ES segment.

    // Copy values from DS to ES.
    *((uint16_t*)(0x6402)) = *((uint16_t*)(0x67f6));
    *((uint16_t*)(0x6404)) = *((uint16_t*)(0x67f8));

    // Call external function with CS as parameter.
    FUN_24dd_465d();
    FUN_235c_121e(0x2000);
}
