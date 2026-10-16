#include <stdint.h>
#include <stddef.h>
typedef unsigned char undefined1, byte, uchar;
typedef unsigned short undefined2, ushort, word;
typedef unsigned int undefined4;
typedef unsigned long undefined8;
typedef long long longlong;
typedef unsigned long long ulonglong;
typedef unsigned int uint;
typedef short int16;
#define __cdecl16near
#define __cdecl16far
#define __stdcall16near
#define __stdcall16far
#define __cdecl
#define __stdcall
#define __fastcall
#define __pascal
#define __near
#define __far
#define __interrupt
#define __declspec(x)
/* BSD/kernel types some models assume (not Ghidra, but harmless to accept) */
typedef unsigned char u_char;
typedef unsigned short u_short, u_int16;
typedef unsigned int u_int, u32, uint32;
typedef unsigned short uint16, ushort_t;
typedef unsigned char uint8;
#ifndef true
#define true 1
#define false 0
#endif

#include <stdint.h>

void __stdcall16far FUN_24dd_3639(uint16_t *param_1, uint16_t *param_2) {
    uint16_t *puVar6;
    uint16_t uVar8;
    uint16_t iVar3;
    uint16_t uVar4;
    uint8_t *pbVar1;
    uint8_t *pbVar2;
    uint8_t *pbVar5;
    uint8_t *pbVar7;

    uVar8 = (uint16_t)((uint32_t)param_2 >> 16);
    puVar6 = param_2;
    *param_2 = 0;
    puVar6[1] = 0xd7b0;
    puVar6[2] = 0x80;
    puVar6[3] = 0;
    puVar6[4] = 0;
    puVar6[5] = 0;
    puVar6[6] = (uint16_t)((uint32_t)puVar6 + 0x40);
    puVar6[7] = uVar8;
    pbVar7 = (uint8_t *)(puVar6 + 9);
    puVar6[8] = 0x420c;
    pbVar7[0] = 0xdd;
    pbVar7[1] = 0x24;
    for (iVar3 = 0xe; pbVar7 = pbVar7 + 2, iVar3 != 0; iVar3 = iVar3 + -1) {
        pbVar7[0] = 0;
        pbVar7[1] = 0;
    }
    uVar4 = 0x4f;
    pbVar5 = (uint8_t *)param_1 + 1;
    if (0x4e < *param_1) goto LAB_24dd_367d;
    for (uVar4 = *param_1; uVar4 != 0; uVar4 = uVar4 - 1) {
LAB_24dd_367d:
        pbVar1 = pbVar5;
        pbVar5 = pbVar5 + 1;
        if (*pbVar1 == 0) break;
        pbVar2 = pbVar7;
        pbVar7 = pbVar7 + 1;
        *pbVar2 = *pbVar1;
    }
    *pbVar7 = 0;
    return;
}