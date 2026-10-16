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

void __stdcall16far FUN_1ea2_01a8(int *param_1, int *param_2, int param_3, int param_4, int param_5) {
    int iVar1;
    int *piVar2;
    int *piVar3;
    uint uVar4;
    uint *puVar5;
    uint *puVar6;

    uVar4 = (uint)param_5 >> 1;
    piVar2 = param_1;
    piVar3 = param_2;
    if ((param_5 & 1) != 0) {
        uVar4 = uVar4 * 2;
        piVar3 = (int *)((int)piVar3 + (param_5 & -2));
    }
    puVar5 = (uint *)((int)piVar2 + uVar4);
    puVar6 = (uint *)((int)piVar3 + uVar4);
    iVar1 = uVar4;
    do {
        for (; iVar1 != 0; iVar1--) {
            *puVar5 = *puVar6;
            puVar5++;
            puVar6++;
        }
        puVar5 = (uint *)((int)puVar5 + (0x140 - uVar4));
        puVar6 = (uint *)((int)puVar6 + (0x140 - uVar4));
        iVar1 = uVar4;
    } while (param_5 != 0);
    return;
}