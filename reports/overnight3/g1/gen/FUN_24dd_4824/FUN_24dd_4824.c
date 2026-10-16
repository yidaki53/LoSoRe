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

uint16_t __stdcall16far FUN_24dd_4824(int *param_1, byte *param_2) {
    uint16_t uVar1;
    uint32_t uVar2;
    int iVar3;
    byte *pbVar4;
    bool bVar5;

    bVar5 = false;
    uVar2 = (uint32_t)*param_2;
    pbVar4 = (byte *)param_2;
    while ((pbVar4 = pbVar4 + 1, uVar2 != 0 && (bVar5 = *pbVar4 < 0x20, *pbVar4 == 0x20))) {
        uVar2 = uVar2 - 1;
    }
    uVar1 = FUN_24dd_4732();
    if ((bVar5) || (iVar3 = 0, uVar2 != 0)) {
        iVar3 = (int)pbVar4 - (int)(byte *)param_2;
        uVar1 = 0;
    }
    *param_1 = iVar3;
    return uVar1;
}