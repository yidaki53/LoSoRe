/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_b28f
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = lenient
 * Dual-judge: qwen=3 phi=4 verdict=contested
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

// Forward declarations of external functions
void FUN_24dd_0530(void);
void FUN_202c_076d(uint16_t, uint16_t);
void FUN_24dd_3f14(uint16_t, uint16_t);
void FUN_24dd_3eaf(uint16_t, uint16_t, uint16_t, uint8_t*, uint16_t);

void FUN_1000_b28f(int param_1) {
    uint16_t unaff_SS;
    uint8_t local_103[253];
    uint16_t uVar2;
    uint8_t *puVar1;
    uint8_t local_3 = 0x10;

    FUN_24dd_0530();

    puVar1 = local_103;
    uVar2 = unaff_SS;

    FUN_202c_076d(*(uint16_t *)((*(uint8_t *)(param_1 + 6) * 2) + 0x66e8), 0);
    FUN_24dd_3f14(0xb28d, 0x202c);

    FUN_24dd_3eaf(0xc, param_1 - 0xa1, unaff_SS, puVar1, uVar2);

    puVar1 = local_103;
    uVar2 = unaff_SS;

    FUN_202c_076d(*(uint8_t *)((*(uint8_t *)(param_1 + 6) * 3) + 0x66d8), 0);
    FUN_24dd_3eaf(0xc, param_1 - 0x94, unaff_SS, puVar1, uVar2);

    puVar1 = local_103;
    uVar2 = unaff_SS;

    FUN_202c_076d(*(uint8_t *)((*(uint8_t *)(param_1 + 6) * 3) + 0x66d9), 0);
    FUN_24dd_3eaf(0xc, param_1 - 0x87, unaff_SS, puVar1, uVar2);

    puVar1 = local_103;
    uVar2 = unaff_SS;

    FUN_202c_076d(*(uint8_t *)((*(uint8_t *)(param_1 + 6) * 3) + 0x66da), 0);
    FUN_24dd_3eaf(0xc, param_1 - 0x7a, unaff_SS, puVar1, uVar2);

    local_3 = 0;
    while (true) {
        FUN_24dd_3eaf(0xc, param_1 + (local_3 + 5) * 0xd - 0xae,
                      unaff_SS,
                      (*(uint8_t *)((*(uint8_t *)(param_1 + 6) * 7) + local_3 + 0x6720) * 0xd) + 0x5b19,
                      unaff_SS);

        if (local_3 == 6) break;

        local_3++;
    }

    FUN_24dd_3eaf(0xc, param_1 - 0x12, unaff_SS,
                  (*(uint8_t *)(*(uint8_t *)(param_1 + 6) + 0x66a7) * 6) + 900,
                  unaff_SS);
}
