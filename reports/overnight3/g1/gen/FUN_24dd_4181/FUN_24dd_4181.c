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

void __stdcall16far FUN_24dd_4181(uint *param_1, uint *param_2) {
    uint *puVar1;
    uint *puVar2;
    uint *puVar3;
    int iVar4;
    uint *puVar5;
    uint *puVar6;
    uint uVar7;

    uVar7 = (uint)((ulong)param_2 >> 0x10);
    puVar6 = (uint *)param_2;
    puVar5 = (uint *)param_1;
    iVar4 = 0x10;
    do {
        puVar2 = puVar5;
        puVar5 = puVar5 + 1;
        puVar1 = puVar6;
        puVar3 = puVar6;
        puVar6 = puVar6 + 1;
        *puVar3 = *puVar2 | *puVar1;
        iVar4 = iVar4 + -1;
    } while (iVar4 != 0);
    return;
}