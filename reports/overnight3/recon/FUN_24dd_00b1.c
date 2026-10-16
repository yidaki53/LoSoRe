/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_00b1
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_00b1(void) {
    uint16_t uVar1;
    uint8_t bVar2;
    uint8_t *pbVar3;

    uVar1 = (uint16_t)((uint8_t)(uint16_t)0x0000 << 16) | 0x0000;
    bVar2 = (uint8_t)(uint16_t)0x0000;
    pbVar3 = (uint8_t *)0x6420;
    if ((bVar2 & 0xf0) != 0xf0) {
        do {
            uVar1 = (uint16_t)((uint8_t)(uint16_t)0x0000 << 16) | 0x0001;
            bVar2 = (uint8_t)(uint16_t)0x0000;
            pbVar3 = (uint8_t *)0x6420;
        } while ((bVar2 & 0xf0) != 0xf0);
    }
    do {
        uVar1 = (uint16_t)((uint8_t)(uint16_t)0x0000 << 16) | 0x0001;
        bVar2 = (uint8_t)(uint16_t)0x0000;
        pbVar3 = (uint8_t *)0x6420;
    } while ((bVar2 & 0xf0) != 0xf0);
    *pbVar3 = (uint8_t)0x00;
    return;
}
