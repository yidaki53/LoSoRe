/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_1162
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_235c_0aeb(void);
void FUN_235c_10a3(uint8_t);

void FUN_235c_1162(void) {
    uint8_t local_4 = 0;

    FUN_235c_0aeb();
    while (true) {
        if (*(char *)(0x67fc + local_4) != '\0') {
            FUN_235c_10a3(local_4 & 0xff);
        }
        if (local_4 == 7) {
            break;
        }
        local_4++;
    }
    return;
}
