/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_0ac7
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_0530(void);
extern char FUN_24dd_4654(uint16_t);
extern void FUN_202c_1b84(uint16_t, uint16_t, uint16_t, uint16_t);
extern char FUN_1000_0961(int, uint16_t, uint16_t);

void FUN_1000_0ac7(void) {
    char cVar1;
    int iVar2;
    uint16_t uVar3;
    int iVar4;
    uint16_t uVar5;
    uint16_t *local_8;
    int local_4;

    FUN_24dd_0530();

    for (local_4 = 1;
         (*(char *)((*(uint32_t *)0x6698) + local_4 * 0xe - 2) != '\0' &&
          (local_4 <= (int)(uint8_t)*(uint8_t *)0x669c));
         local_4++) {
    }

    if (local_4 <= (int)(uint8_t)*(uint8_t *)0x669c) {
        uVar5 = (*(uint32_t *)0x6698) >> 0x10;
        iVar4 = (*(uint32_t *)0x6698) + local_4 * 0xe;
        local_8 = (uint16_t *)((uVar5 << 0x10) | ((uint32_t)(uint16_t)(*(uint32_t *)0x6698 + local_4 * 0xe - 0xe)));
        cVar1 = FUN_24dd_4654(2);
        *(char *)(iVar4 - 2) = cVar1 + 1;
        iVar2 = FUN_24dd_4654((uint16_t)((*(uint8_t *)(iVar4 - 2) * 2) + 0x1364));
        *(int *)(iVar4 - 4) = *(int *)((*(uint8_t *)(iVar4 - 2) * 2) + 0x1360) + iVar2;

        if (*(char *)(iVar4 - 2) == 1) {
            cVar1 = FUN_24dd_4654(0x28);
            *(char *)(iVar4 - 1) = cVar1 + 1;
            while (*(char *)(*(uint8_t *)(iVar4 - 1) + 0x66af) == 2) {
                cVar1 = FUN_24dd_4654(0x28);
                *(char *)(iVar4 - 1) = cVar1 + 1;
            }
        }

        *(uint16_t *)(iVar4 - 8) = 0;
        *(uint16_t *)(iVar4 - 6) = 0;

        do {
            uVar3 = FUN_24dd_4654(0x1f8);
            *local_8 = uVar3;
            uVar3 = FUN_24dd_4654(0x15e);
            *(uint16_t *)(iVar4 - 10) = uVar3;
            cVar1 = FUN_1000_0961(local_4, *(uint16_t *)(iVar4 - 10), *local_8);
        } while (cVar1 == '\0');

        FUN_202c_1b84(0x24dd, *(uint16_t *)(iVar4 - 10), *local_8, 8);
    }
}
