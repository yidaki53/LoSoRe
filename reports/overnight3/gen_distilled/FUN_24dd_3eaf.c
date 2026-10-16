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

void __stdcall16far FUN_24dd_3eaf(uint8_t param_1, uint8_t *param_2, uint8_t *param_3) {
    uint8_t bVar1;
    uint16_t uVar2;
    uint8_t *pbVar3;
    uint8_t *pbVar4;

    pbVar3 = param_3;
    pbVar4 = param_2;
    bVar1 = *param_3 < param_1;
    if (bVar1) {
        param_1 = *param_2;
    }
    *param_4 = param_1;
    uVar2 = (uint16_t)param_1;
    while (true) {
        pbVar3 = pbVar3 + 1;
        pbVar4 = pbVar4 + 1;
        if (uVar2 == 0) break;
        uVar2 = uVar2 - 1;
        *pbVar3 = *pbVar4;
    }
    return;
}