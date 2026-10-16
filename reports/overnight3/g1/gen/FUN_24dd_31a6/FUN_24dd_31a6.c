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

#include <math.h>

void FUN_24dd_31a6(void) {
    uint uVar1;
    longdouble lVar2;
    longdouble in_ST0;

    lVar2 = (longdouble)0;
    *(uint *)0x7b40 =
        (uint)isnan(in_ST0) << 8 | (uint)(in_ST0 < lVar2) << 9 | (uint)(in_ST0 != lVar2) << 10 |
        (uint)(in_ST0 == lVar2) << 0xe;
    uVar1 = *(uint *)0x7b40;
    if ((((uVar1 & 0x4500) != 0) && ((uVar1 & 0x4000) != 0)) && ((uVar1 & 0x400) != 0)) {
        return;
    }
    return;
}