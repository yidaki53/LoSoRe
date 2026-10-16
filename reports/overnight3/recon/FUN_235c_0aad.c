/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0aad
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __stdcall16far FUN_235c_0aad(uint8_t param_1) {
    uint16_t uVar1;

    *((uint8_t*)(0x6854)) = param_1;
    uVar1 = *((uint16_t*)((uint16_t)0x6e60 + (uint16_t)param_1 * 4));
    *((uint16_t*)(0x6e6c)) = uVar1;
    *((uint16_t*)(0x6e6e)) = *((uint16_t*)((uint16_t)0x6e62 + (uint16_t)param_1 * 4));
    return;
}
