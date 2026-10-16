/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_05a4
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=3 verdict=contested
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void __cdecl16far FUN_24dd_0530(void);
void __cdecl16far FUN_235c_0f1d(uint16_t);
void __cdecl16far FUN_235c_032e(void);
void __cdecl16far FUN_235c_08e4(uint16_t, uint16_t);
void __cdecl16far FUN_235c_04a2(void);

void __cdecl16far FUN_1000_05a4(void) {
    uint16_t uVar1;
    int local_4;

    FUN_24dd_0530();
    if (*(char *)(0x4b8) != '\0') {
        FUN_235c_0f1d(0x235c);
        FUN_235c_032e();
        local_4 = 1;
        while (true) {
            uVar1 = (uint16_t)(local_4 * 4) + 0x6734;
            FUN_235c_08e4(uVar1, 0x1000);
            if (local_4 == 0x1e) break;
            local_4++;
        }
        FUN_235c_04a2();
    }
    return;
}
