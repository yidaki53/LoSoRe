/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_0303
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=5 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

int __cdecl16far FUN_24dd_0303(void) {
    uint32_t uVar1;

    // Call an external function and store the result in uVar1
    uVar1 = ((uint32_t (*)())0x2031c)();

    // Combine the lower and upper bytes of uVar1 into a 32-bit integer
    return (int)uVar1 + (int)((uVar1 >> 0x10) * 0x10);
}
