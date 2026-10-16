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

void __stdcall16far FUN_24dd_3ed3(uint param_1, uint param_2, byte *param_3, byte *param_4) {
    byte *pbVar1;
    uint uVar2;
    byte *pbVar3;
    byte *pbVar4;

    pbVar4 = param_4;
    if ((int)param_2 < 1) {
        param_2 = 1;
    }
    pbVar3 = param_3 + param_2;
    if (*param_3 < param_2) {
        uVar2 = 0;
    } else {
        uVar2 = (*param_3 - param_2) + 1;
        if ((int)param_1 < 0) {
            param_1 = 0;
        }
        if (param_1 < uVar2) {
            uVar2 = param_1;
        }
    }
    *param_4 = (byte)uVar2;
    for (; uVar2 != 0; uVar2--) {
        pbVar1 = pbVar3;
        pbVar3 = pbVar3 + 1;
        *pbVar4 = *pbVar1;
        pbVar4 = pbVar4 + 1;
    }
    return;
}