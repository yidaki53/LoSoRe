/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_001a
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t in(uint16_t port);

uint8_t FUN_235c_001a(void) {
    uint8_t bVar1;
    uint8_t uVar2;
    const uint16_t addr1 = 0x67d6;
    const uint16_t addr2 = 0x67d2;

    do {
        bVar1 = in(addr1);
    } while ((bVar1 & 0x80) == 0);

    uVar2 = in(addr2);
    return uVar2;
}
