/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_03a1
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void out(uint16_t port, uint8_t value);

void FUN_235c_03a1(void) {
    out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ee));
    out(*(uint16_t *)(0x67e0), 0);
    out(*(uint16_t *)(0x67e2), *(uint8_t *)(0x67ef));
    out(*(uint16_t *)(0x67e4), *(uint8_t *)(0x6e76));
    out(*(uint16_t *)(0x67e4), *(uint8_t *)(0x6e77));
    out(*(uint16_t *)(0x67e6), (char)(*(uint16_t *)(0x67f0) - 1));
    out(*(uint16_t *)(0x67e6), (char)(((uint16_t)(*(uint16_t *)(0x67f0)) - 1) >> 8));
    out(*(uint16_t *)(0x67e8), *(uint8_t *)(0x67ed));
    out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67cd));
    out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67cc));
    if (*(char *)(0x67ee) == '\0') {
        out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ee));
        out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ee));
    } else {
        out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ee));
        out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ee));
    }
    return;
}
