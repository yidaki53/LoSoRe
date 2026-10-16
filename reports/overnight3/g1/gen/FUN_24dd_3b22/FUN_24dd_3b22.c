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

void __stdcall16far FUN_24dd_3b22(uint16_t *param_1, uint16_t *param_2) {
    uint16_t *pbVar1;
    uint16_t *pbVar2;
    int iVar3;
    uint16_t uVar4;
    uint16_t *pbVar5;
    uint16_t *pbVar6;
    uint16_t uVar7;

    uVar7 = (uint16_t)((uint32_t)param_2 >> 16);
    pbVar6 = (uint16_t *)((uint16_t *)param_2 + 1);
    *param_2 = 0;
    pbVar6[0] = 0xb0;
    pbVar6[1] = 0xd7;
    for (iVar3 = 0x16; pbVar6 = pbVar6 + 2, iVar3 != 0; iVar3 = iVar3 + -1) {
        pbVar6[0] = 0;
        pbVar6[1] = 0;
    }
    uVar4 = 0x4f;
    pbVar5 = (uint16_t *)param_1 + 1;
    if (0x4e < *param_1) goto LAB_24dd_3b4e;
    for (uVar4 = (uint16_t)*param_1; uVar4 != 0; uVar4 = uVar4 - 1) {
LAB_24dd_3b4e:
        pbVar1 = pbVar5;
        pbVar5 = pbVar5 + 1;
        if (*pbVar1 == 0) break;
        pbVar2 = pbVar6;
        pbVar6 = pbVar6 + 1;
        *pbVar2 = *pbVar1;
    }
    *pbVar6 = 0;
    return;
}