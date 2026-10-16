/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1ec2_13c5
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

void __cdecl16far FUN_1ec2_13c5(void) {
    // External function declarations
    extern char in(uint16_t port);

    // Variables
    char cVar1;

    // Wait for the vertical retrace to start
    do {
        cVar1 = in(0x3da);
    } while ((cVar1 & 8) != 0);

    // Wait for the vertical retrace to end
    do {
        cVar1 = in(0x3da);
    } while ((cVar1 & 8) == 0);
}
