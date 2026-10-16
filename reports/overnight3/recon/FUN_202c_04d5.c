/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_04d5
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t FUN_24dd_4161(void);
extern uint32_t *DAT_6674;
extern uint8_t DAT_6644[0x20];

void FUN_202c_04d5(char param_1, uint32_t param_2, int param_3, int param_4) {
    uint32_t uVar1;
    uint32_t uVar3;
    uint32_t uVar4;
    int iVar5;
    int iVar6;
    int iVar7;
    int local_a;
    int local_8;

    iVar7 = (int)param_2;
    if (param_1 == '\0') {
        for (local_a = 0; (iVar5 = local_a + param_3) < 0x15e; local_a++) {
            if (iVar5 >= 0) {
                local_8 = 0;
                while (true) {
                    iVar6 = local_8 + param_4;
                    if ((iVar6 >= 0) && (iVar6 < 0x1f8) && (*(char *)(iVar7 + local_a * 7 + local_8) != '\0')) {
                        uVar1 = *(uint32_t *)((int)*DAT_6674 + iVar5 * 4);
                        *(uint8_t *)((int)uVar1 + iVar6) = *(uint8_t *)(iVar7 + local_a * 7 + local_8);
                    }
                    if (local_8 == 6) break;
                    local_8++;
                }
            }
            if (local_a == 6) {
                return;
            }
        }
    } else {
        for (local_a = 0; (uVar3 = local_a + param_3) < 0x15e; local_a++) {
            if (uVar3 < 0x8000) {
                local_8 = 0;
                while (true) {
                    uVar4 = local_8 + param_4;
                    if ((uVar4 < 0x8000) && ((int)uVar4 < 0x1f8) && (*(char *)(iVar7 + local_a * 7 + local_8) != '\0')) {
                        int iVar5 = 0x20;
                        uint8_t bVar2 = FUN_24dd_4161();
                        if ((DAT_6644[iVar5] & bVar2) == 0) {
                            uVar1 = *(uint32_t *)((int)*DAT_6674 + uVar3 * 4);
                            *(uint8_t *)((int)uVar1 + uVar4) = *(uint8_t *)(iVar7 + local_a * 7 + local_8) + 3;
                        } else {
                            uVar1 = *(uint32_t *)((int)*DAT_6674 + uVar3 * 4);
                            *(uint8_t *)((int)uVar1 + uVar4) = *(uint8_t *)(iVar7 + local_a * 7 + local_8);
                        }
                    }
                    if (local_8 == 6) break;
                    local_8++;
                }
            }
            if (local_a == 6) {
                return;
            }
        }
    }
}
