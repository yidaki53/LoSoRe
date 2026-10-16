/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_202c_0843
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=4 phi=4 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern uint8_t FUN_24dd_3b22(uint8_t *, uint16_t, uint8_t *, uint16_t);
extern uint8_t FUN_24dd_3b5d(uint8_t, uint8_t *, uint16_t);
extern uint8_t FUN_24dd_3bde(uint8_t *, uint16_t);
extern int FUN_24dd_04ed(void);

uint8_t __stdcall16far FUN_202c_0843(uint8_t *param_1) {
    uint8_t *pbVar6 = param_1;
    uint8_t local_104 = *param_1;
    uint8_t abStack_103[257];
    uint8_t pbVar2 = 0;
    uint8_t pbVar1;
    uint8_t uVar3;
    int iVar4;
    uint32_t uVar5;

    pbVar2 = 0;
    uVar5 = (uint32_t)local_104;
    while (uVar5 != 0) {
        pbVar1 = abStack_103[pbVar2];
        abStack_103[pbVar2] = *pbVar6;
        pbVar6 = pbVar6 + 1;
        pbVar2 = pbVar2 + 1;
        uVar5 = uVar5 - 1;
    }

    FUN_24dd_3b22(&local_104, 0, abStack_103, 0);
    *(uint8_t *)0x6422 = 0;
    FUN_24dd_3b5d(0x80, abStack_103, 0);
    FUN_24dd_3bde(abStack_103, 0);
    iVar4 = FUN_24dd_04ed();
    if ((iVar4 == 0) && (local_104 != 0)) {
        uVar3 = 1;
    } else {
        uVar3 = 0;
    }
    return uVar3;
}
