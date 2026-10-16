/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_24dd_14c4
 * Generated: 2026-10-16 by distilled-Qwen2.5-Coder-1.5B (distilled-g3)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=- phi=- verdict=not-judged
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_24dd_04f8(void);
void FUN_24dd_1519(void);
void FUN_24dd_1277(int, uint16_t, int);
void FUN_24dd_13e2(int, uint16_t, int);
void FUN_24dd_1551(void);
void FUN_24dd_1588(void);

void FUN_24dd_14c4(void) {
    uint16_t uVar1;
    uint16_t *base_address = (uint16_t *)0xd8;
    int *int_ptr = (int *)0x804a054;

    if (-0x3fff < *int_ptr) {
        if (0x3fff < *int_ptr) {
            if (*(char *)(int_ptr + 1) == '\0') {
                FUN_24dd_04f8();
                FUN_24dd_1519();
                uVar1 = *base_address;
                FUN_24dd_1277(0x804a054, uVar1, 0x804a058);
                FUN_24dd_13e2(0x804a054, uVar1, 0x804a05c);
                FUN_24dd_1551();
                FUN_24dd_1588();
                *int_ptr = *int_ptr - 1;
                *base_address = *base_address + 0xc;
                return;
            }
            FUN_24dd_1551();
            FUN_24dd_1588();
            *int_ptr = *int_ptr - 1;
            *base_address = *base_address + 0xc;
            return;
        }
        FUN_24dd_1551();
        FUN_24dd_1588();
        *int_ptr = *int_ptr - 1;
        *base_address = *base_address + 0xc;
        return;
    }
    FUN_24dd_1551();
    FUN_24dd_1588();
    *int_ptr = *int_ptr - 1;
    *base_address = *base_address + 0xc;
    return;
}
