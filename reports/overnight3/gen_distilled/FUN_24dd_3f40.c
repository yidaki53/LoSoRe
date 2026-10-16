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

uint16_t FUN_24dd_3f40(uint16_t param_1, uint8_t *param_2) {
    uint8_t bVar1;
    uint32_t uVar2;
    uint8_t *pbVar3;
    uint8_t *pbVar4;
    int iVar5;
    uint16_t uVar6;

    uVar6 = (uint16_t)((uintptr_t)param_2 >> 16);
    param_2 = (uint8_t *)((uintptr_t)param_2 & 0xFFFF);

    bVar1 = *param_2 != 0;
    if (bVar1) {
        uVar2 = (uint32_t)*param_2;
        pbVar3 = param_2;
        do {
            for (iVar5 = (int)(char)*param_2 - (char)*pbVar3; iVar5 != 0; iVar5--) {
                pbVar4 = pbVar3;
                pbVar3 = pbVar3 + 1;
            }
            pbVar3 = pbVar3 - 1;
            uVar2 = uVar2 - (uint32_t)*param_2 + (uint32_t)*pbVar4;
            param_2 = param_2 + 1;
        } while (param_2 != (uint8_t *)0);
        uVar6 = ((uint16_t)(uint32_t)uVar6 << 16) | ((uint16_t)uVar2 >> 16);
        uVar1 = ((uint16_t)uVar2 & 0xFFFF) + (param_1 >> 16);
        return ((uint16_t)uVar1 << 16) | uVar6;
    }
    return 0;
}