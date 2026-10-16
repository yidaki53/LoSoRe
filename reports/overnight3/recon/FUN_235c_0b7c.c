/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0b7c
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void FUN_235c_0b7c(void) {
    int *memory = (int *)0x7286; // Assuming 0x7286 is the offset in the segment
    int *base = (int *)0xfc00; // Assuming 0xfc00 is the base address

    for (int i = -0x400; i < 0x400; i++) {
        if (i < -0x80) {
            i = -0x80;
        }
        if (0x7f < i) {
            i = 0x7f;
        }
        memory[i + 0x80] = base[i] + 0x80;
    }
}
