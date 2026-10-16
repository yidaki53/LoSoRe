/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_0d70
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_0530(void);
extern uint8_t FUN_24dd_4161(void);

uint8_t FUN_1000_0d70(int param_1, int param_2, uint8_t param_3, uint8_t param_4) {
    uint8_t bVar1;
    int iVar2;
    int iVar3;
    int iVar4;
    int iVar5;
    int local_b;
    int local_9;
    int base_address = *(int *)0x6670;
    int offset = (uint)param_4 * 0xaa;

    FUN_24dd_0530();

    if (*(char *)(base_address + offset + 0x9a) != '\0') {
        iVar2 = (param_2 - *(int *)(base_address + offset + 6)) + 7;
        iVar3 = (param_1 - *(int *)(base_address + offset + 10)) + 5;

        if (*(char *)(base_address + offset + 0x9b) == '\0') {
            iVar2 = 0xe - iVar2;
        }

        local_9 = iVar2 - (uint)param_3;

        if (local_9 <= (int)((uint)param_3 + iVar2)) {
            while (true) {
                iVar4 = (uint)param_3 + iVar3;
                local_b = iVar3 - (uint)param_3;

                if (local_b <= iVar4) {
                    while (true) {
                        if ((0 < local_9) && (local_9 < 0xe) && (-1 < local_b) && (local_b < 10)) {
                            iVar5 = 0x20;
                            bVar1 = FUN_24dd_4161();

                            if ((*(uint8_t *)(iVar5 + 0x28) & bVar1) != 0) {
                                return 1;
                            }
                        }

                        if (local_b == iVar4) break;
                        local_b++;
                    }
                }

                if (local_9 == (uint)param_3 + iVar2) break;
                local_9++;
            }
        }
    }

    return 0;
}
