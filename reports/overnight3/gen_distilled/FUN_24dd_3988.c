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

void __stdcall16far FUN_24dd_3988(int param_1, undefined4 *param_2, int param_3, int param_4) {
    undefined4 uVar1;
    undefined4 *puVar2;
    undefined4 uVar3;
    undefined4 uVar4;

    uVar1 = *param_2;
    puVar2 = param_2;
    uVar4 = (undefined4)((int)puVar2 >> 16);
    puVar2 = puVar2 + param_3;
    uVar3 = (undefined4)((int)puVar2 >> 16);
    *puVar2 = (char)(puVar2 - puVar4 - 1);
    return;
}