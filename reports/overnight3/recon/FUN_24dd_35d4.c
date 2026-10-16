/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_35d4
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=4 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_1ee4(void);
extern uint16_t swi_3c(void);
extern void swi_3a(void);

void FUN_24dd_35d4(void) {
    uint16_t in_AX;
    uint16_t uVar5;
    uint16_t uVar4;
    uint16_t uVar2;
    uint16_t iVar3;

    // Assume in_AX is initialized or passed in some way
    // Placeholder for actual initialization of in_AX
    in_AX = 0; // Replace with actual initialization

    if (0x1000 < in_AX) {
        iVar3 = swi_3c();
        in_AX = iVar3 - 0xfff;
    }
    if (in_AX < -0x1000) {
        iVar3 = swi_3c();
        in_AX = iVar3 + 0x1001;
    }
    if (in_AX != 0) {
        swi_3c();
        uVar4 = FUN_24dd_1ee4();
        uVar4 >>= 1;
        while (uVar4 != 0) {
            uVar2 = uVar4 & 1;
            uVar4 >>= 1;
            if (uVar2 != 0) {
                uVar5 = swi_3c();
                uVar4 = ((uVar5 >> 8) << 1) | ((uVar5 & 0xFF) + '3');
            }
        }
        if (-1 < in_AX) {
            swi_3a();
            return;
        }
        swi_3a();
    }
}
