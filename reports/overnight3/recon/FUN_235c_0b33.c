/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0b33
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint16_t FUN_24dd_415f(uint16_t, uint16_t, uint16_t, uint16_t);
extern uint16_t FUN_24dd_4193(uint16_t, uint16_t, uint16_t, uint16_t);

uint16_t FUN_235c_0b33(uint16_t param_1, uint16_t param_2) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint16_t uVar7;

    uVar7 = FUN_24dd_415f(param_1, param_2, 0, 0);
    uVar6 = FUN_24dd_415f(param_1, param_2, 0, 0);
    uVar3 = 0x10;
    uVar5 = 0;
    uVar1 = FUN_24dd_4193(uVar3, 0, uVar7, uVar6);
    uVar2 = FUN_24dd_4193(uVar3, 0, uVar7, uVar6);
    return ((uint16_t)(uVar1 >> 16) << 16) | uVar2;
}
