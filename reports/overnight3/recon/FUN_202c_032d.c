/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_032d
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t FUN_24dd_4161(void);
extern uint32_t* DAT_6674;
extern uint32_t* DAT_6644;

void FUN_202c_032d(char param_1, uint32_t param_2, int param_3, int param_4) {
    uint32_t uVar1;
    uint8_t bVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    int iVar5;
    int iVar6;
    int iVar7;
    uint16_t uVar8;
    int local_a;
    int local_8;

    iVar7 = (int)param_2;
    uVar8 = (uint16_t)((uint32_t)param_2 >> 0x10);

    if (param_1 == '\0') {
        for (local_a = 0; (iVar5 = local_a + param_3) < 0x15e; local_a++) {
            if (-1 < iVar5) {
                local_8 = 0;
                while (true) {
                    iVar6 = local_8 + param_4;
                    if ((-1 < iVar6) && (iVar6 < 0x1f8) &&
                        (*(char *)(iVar7 + local_a * 0x10 + local_8) != '\0')) {
                        uVar1 = *(uint32_t *)((int)*DAT_6674 + iVar5 * 4);
                        *(uint8_t *)((int)uVar1 + iVar6) = *(uint8_t *)(iVar7 + local_a * 0x10 + local_8);
                    }
                    if (local_8 == 0xf) break;
                    local_8++;
                }
            }
            if (local_a == 0xf) {
                return;
            }
        }
    } else {
        for (local_a = 0; (uVar3 = local_a + param_3) < 0x15e; local_a++) {
            if (uVar3 < 0x8000) {
                local_8 = 0;
                while (true) {
                    uVar4 = local_8 + param_4;
                    if ((uVar4 < 0x8000) && ((int)uVar4 < 0x1f8) &&
                        (*(char *)(iVar7 + local_a * 0x10 + local_8) != '\0')) {
                        int iVar5 = 0x20;
                        bVar2 = FUN_24dd_4161();
                        if ((*(uint8_t *)(iVar5 + (int)*DAT_6644) & bVar2) == 0) {
                            uVar1 = *(uint32_t *)((int)*DAT_6674 + uVar3 * 4);
                            *(uint8_t *)((int)uVar1 + uVar4) = *(uint8_t *)(iVar7 + local_a * 0x10 + local_8) + 3;
                        } else {
                            uVar1 = *(uint32_t *)((int)*DAT_6674 + uVar3 * 4);
                            *(uint8_t *)((int)uVar1 + uVar4) = *(uint8_t *)(iVar7 + local_a * 0x10 + local_8);
                        }
                    }
                    if (local_8 == 0xf) break;
                    local_8++;
                }
            }
            if (local_a == 0xf) {
                return;
            }
        }
    }
}
