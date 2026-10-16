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

void __stdcall16far FUN_1ec2_00a5(int param_1, int param_2, undefined1 *param_3, undefined1 *param_4) {
    undefined1 *puVar1;
    undefined1 *puVar2;
    int iVar3;
    undefined1 *puVar4;
    undefined1 *puVar5;

    puVar5 = param_3;
    puVar4 = param_4;
    iVar3 = param_2;
    do {
        for (; iVar3 != 0; iVar3--) {
            puVar2 = puVar5;
            puVar5 = puVar5 + 1;
            puVar1 = puVar4;
            puVar4 = puVar4 + 1;
            *puVar2 = *puVar1;
        }
        puVar5 = puVar5 + (0x140 - param_2);
        puVar4 = puVar4 + (0x140 - param_2);
        param_1 = param_1 - 1;
        iVar3 = param_2;
    } while (param_1 != 0);
    return;
}