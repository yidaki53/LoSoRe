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

void __stdcall16far FUN_1ec2_0810(uint16_t param_1, uint8_t *param_2) {
    uint8_t local_302[768];
    uint8_t *pbVar1;
    uint8_t *pbVar3;
    uint16_t uVar4;
    uint16_t uVar6;
    uint16_t uVar8;
    uint16_t uVar10;

    uVar10 = (uint16_t)((uintptr_t)param_2 >> 16);
    uVar8 = (uint16_t)((uintptr_t)param_2 & 0xFFFF);
    pbVar3 = local_302;
    for (uVar6 = 0x300; uVar6 != 0; uVar6--) {
        pbVar1 = param_2;
        param_2 = param_2 + 1;
        *pbVar3 = *pbVar1;
        pbVar3 = pbVar3 + 1;
    }

    uVar4 = (uint16_t)((uintptr_t)local_302 >> 16);
    uVar6 = (uint16_t)((uintptr_t)local_302 & 0xFFFF);
    pbVar1 = param_2;
    param_2 = param_2 + 1;
    uVar10 = uVar10 * 16 + (uint16_t)((uint8_t)*param_1 >> 8);
    uVar8 = uVar8 * 16 + (uint16_t)((uint8_t)*param_1 & 0xFF);
    ((void (*)(uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t, uint16_t))0x1000)(uVar10, uVar8, uVar6, uVar4, (uint16_t)((uint8_t)*param_2 >> 8), (uint16_t)((uint8_t)*param_2 & 0xFF), 0, 0);
    return;
}