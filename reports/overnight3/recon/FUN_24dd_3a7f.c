/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_3a7f
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=3 phi=4 verdict=contested
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_37ec(void);
extern uint16_t swi_35(void);
extern void swi_3d(void);
extern uint16_t swi_39(void);

uint16_t FUN_24dd_3a7f(void) {
    uint16_t uVar2;
    uint16_t uVar3;

    FUN_24dd_37ec();
    uVar2 = swi_35();
    // Assuming out() writes uVar2 to a specific port, replace with actual I/O operation if needed
    // out(extraout_DX, uVar2); // Placeholder for actual I/O operation
    swi_3d();
    *(uint16_t *)0x6410 = 0x6a;
    uVar3 = swi_39();
    return uVar3 ^ 0xcdee;
}
