/* Libre Reconstruction — LoSoRe preservation project
 * Function:  FUN_235c_10a3
 * Generated: 2026-10-16 by qwen2.5-coder:14b (bans)
 * Gate:      gcc -fsyntax-only = strict
 * Dual-judge: qwen=2 phi=3 verdict=junk
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */

#include <stdint.h>

void FUN_235c_0f57(uint8_t, int, uint16_t, uint16_t, uint16_t, uint16_t);

void FUN_235c_10a3(uint8_t param_1) {
    char *pcVar1;
    uint32_t uVar2;
    char *pcVar3;
    int iVar4;
    int iVar5;
    int *piVar6;
    uint16_t uVar7;
    uint32_t local_8;
    int local_4;

    iVar4 = (uint32_t)param_1 * 10;
    local_8 = (uint32_t)((uint16_t)0x235c << 16) + (iVar4 + 0x6804);
    if (*(char *)(0x235c << 16 + (iVar4 + 0x680d)) == '\0') {
        uVar7 = (uint16_t)(local_8 >> 16);
        iVar5 = (int)local_8;
        uVar2 = *(uint32_t *)(iVar5 + 6);
        iVar5 = (*(int *)(iVar5 + 8) - *(int *)(0x235c << 16 + (iVar4 + 0x680b))) -
                (uint32_t)(uVar2 < *(uint32_t *)(0x235c << 16 + (iVar4 + 0x6809)));
        if ((iVar5 < 1) && ((iVar5 < 0 || (uVar2 - *(uint32_t *)(0x235c << 16 + (iVar4 + 0x6809)) < 0x201)))) {
            local_4 = *(int *)((int)local_8 + 6) - *(int *)(0x235c << 16 + (iVar4 + 0x6809));
        } else {
            local_4 = 0x200;
        }
    } else {
        local_4 = 0x200;
    }
    FUN_235c_0f57(*(uint8_t *)(0x235c << 16 + (iVar4 + 0x680d)), local_4, (uint16_t)(0x235c << 16) + (iVar4 + 0x6809),
                0x235c, *(uint16_t *)(0x235c << 16 + (iVar4 + 0x6804)),
                *(uint16_t *)(0x235c << 16 + (iVar4 + 0x6806)));
    pcVar3 = (char *)0x6856;
    piVar6 = (int *)0x6a58;
    do {
        pcVar1 = pcVar3;
        pcVar3 = pcVar3 + 1;
        *piVar6 = *piVar6 + (int)*pcVar1;
        piVar6 = piVar6 + 1;
        local_4 = local_4 + -1;
    } while (local_4 != 0);
    return;
}
