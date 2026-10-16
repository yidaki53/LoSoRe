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

void FUN_24dd_3f14(byte *param_1, byte *param_2) {
    byte bVar1;
    byte bVar2;
    byte *pbVar3;
    byte *pbVar4;

    bVar2 = *param_2;
    *param_1 = bVar2 + *param_1;
    if ((bVar2 & 0x80) != 0) {
        *param_1 = 0xff;
        bVar1 = ~bVar2;
        pbVar3 = (byte *)((int)param_2 + (int)param_1);
        pbVar4 = (byte *)((int)param_1 + (int)param_2);
        while (true) {
            *pbVar3 = *pbVar4;
            if (bVar1 == 0) break;
            bVar1--;
            pbVar3++;
            pbVar4++;
        }
    }
    return;
}