/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0372
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_3dbd(void);

uint16_t FUN_235c_0372(void) {
    uint16_t uVar1;
    int iVar2;
    uint8_t bVar3;

    iVar2 = 0xf;
    uVar1 = FUN_24dd_3dbd();
    bVar3 = (uint8_t)((-(uint16_t)(0x100 < uVar1) - iVar2) << 8 | (0x100 - uVar1));
    return bVar3;
}
