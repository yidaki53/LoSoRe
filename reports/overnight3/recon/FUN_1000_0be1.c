/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_1000_0be1
 * Generated: 2026-10-16 by phi4:14b (sumfirst)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=5 phi=5 verdict=real
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

extern void FUN_24dd_0530(void);
extern char FUN_24dd_4654(int);

void FUN_1000_0be1(uint16_t param_1, uint16_t param_2, uint16_t param_3, uint16_t param_4,
                   uint16_t param_5, uint16_t param_6) {
    char cVar1;
    int iVar2;
    uint16_t uVar3;
    uint16_t *baseAddress = (uint16_t *)0x6690;
    uint16_t local_4;

    FUN_24dd_0530();
    for (local_4 = 0; (*(char *)(baseAddress[0] + local_4 * 0x11) != '\0') && (local_4 < 700); local_4++) {
    }

    cVar1 = FUN_24dd_4654(2);
    *(char *)(baseAddress[0] + local_4 * 0x11) = cVar1 + 'P';
    *(uint16_t *)(baseAddress[0] + local_4 * 0x11 + 3) = param_6;
    *(uint16_t *)(baseAddress[0] + local_4 * 0x11 + 7) = param_5;
    uVar3 = baseAddress[0] >> 0x10;
    iVar2 = baseAddress[0] + local_4 * 0x11;
    *(uint16_t *)(iVar2 + 9) = param_3;
    *(uint16_t *)(iVar2 + 0xb) = param_4;
    uVar3 = baseAddress[0] >> 0x10;
    iVar2 = baseAddress[0] + local_4 * 0x11;
    *(uint16_t *)(iVar2 + 0xd) = param_1;
    *(uint16_t *)(iVar2 + 0xf) = param_2;
}
