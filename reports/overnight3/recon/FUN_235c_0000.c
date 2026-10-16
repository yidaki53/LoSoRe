/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_0000
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t in(uint16_t port);
extern void out(uint16_t port, uint8_t data);

uint8_t FUN_235c_0000(uint8_t param_1) {
    uint8_t bVar1;
    const uint16_t address = 0x67d4;

    do {
        bVar1 = in(address);
    } while ((bVar1 & 0x80) != 0);

    out(address, param_1);
    return param_1;
}
