/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_374d
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=2 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __stdcall16far FUN_24dd_374d(void) {
    uint16_t *ptr = (uint16_t *)(0x6410);
    uint16_t uVar1;

    uVar1 = *(uint16_t *)(0x0000); // Assuming 0x0000 is the base address for the segment

    void (*func_ptr)(uint16_t, uint16_t) = (void (*)(uint16_t, uint16_t))(*(uint16_t *)(0x0000)); // Assuming 0x0000 is the base address for the segment

    func_ptr(uVar1, 0x24dd); // Assuming 0x24dd is the offset for the segment

    if (uVar1 != 0) {
        *ptr = uVar1;
    }
}
