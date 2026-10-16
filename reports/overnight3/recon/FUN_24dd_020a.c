/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_020a
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_020a(uint16_t in_AX, uint16_t in_CX, uint16_t in_BX, uint16_t unaff_ES, uint16_t unaff_IP) {
    uint16_t uVar1;
    char cVar2;

    uVar1 = in_CX;
    cVar2 = (char)(in_AX / uVar1 + 0x30);
    FUN_24dd_0232(cVar2);
    return;
}
