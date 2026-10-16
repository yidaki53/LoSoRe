/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_0548
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern char FUN_24dd_2fcd(void);
extern void FUN_24dd_3054(void);

void FUN_24dd_0548(void) {
    char cVar1;
    uint16_t *ptr = (uint16_t *)(0x640e);

    cVar1 = FUN_24dd_2fcd();
    if (cVar1 == '\0') {
        *ptr = 0xe6;
    }
    FUN_24dd_3054();
}
