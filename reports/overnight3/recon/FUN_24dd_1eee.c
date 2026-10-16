/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_1eee
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=3 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_0628(void);
extern void FUN_24dd_1f27(void);
extern void FUN_24dd_0642(void);
extern void FUN_24dd_10a7(uint16_t, uint16_t, int);

void FUN_24dd_1eee(void) {
    int iVar1;
    uint16_t unaff_SI;
    uint16_t *ptr = (uint16_t *)(0xd8);

    FUN_24dd_0628();
    FUN_24dd_1f27();
    FUN_24dd_0642();

    iVar1 = *ptr * 16 + 0xc; // *(int *)0xd8 + 0xc
    FUN_24dd_10a7((uint16_t)iVar1, (uint16_t)iVar1, *ptr * 16);

    FUN_24dd_10a7(unaff_SI, unaff_SI, (uint16_t)iVar1);

    *ptr = *ptr * 16 + 0x18; // *(int *)0xd8 = *(int *)0xd8 + 0x18
}
