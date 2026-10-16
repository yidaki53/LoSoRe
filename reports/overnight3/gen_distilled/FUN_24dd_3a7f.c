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

void __stdcall16far FUN_24dd_3a7f(uint16_t param_1) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    uint16_t uVar9;
    uint16_t uVar10;

    uVar10 = (uint16_t)((uintptr_t)param_1 >> 16);
    puVar3 = (uint16_t *)0xffae;
    uVar9 = 0x40;
    puVar1 = (uint16_t *)0xff94;
    uVar6 = puVar3 - puVar1;
    uVar7 = 0;

    while (uVar7 < uVar6) {
        uVar8 = uVar7 * -0x10 + 0xff94;
        puVar2 = (uint16_t *)0xffae;
        uVar5 = puVar2 - puVar1;
        uVar1 = uVar5 * -0x10 + 0xff94;
        uVar4 = uVar1 - puVar1;
        uVar8 = uVar4 * -0x10 + 0xff94;
        puVar1 = puVar1 + 1;
        uVar7 = uVar7 + 1;
    }

    uVar10 = (uint16_t)((uintptr_t)param_1 >> 16);
    puVar3 = (uint16_t *)0xffae;
    uVar9 = 0x40;
    puVar1 = (uint16_t *)0xff94;
    uVar6 = puVar3 - puVar1;
    uVar7 = 0;

    while (uVar7 < uVar6) {
        uVar8 = uVar7 * -0x10 + 0xff94;
        puVar2 = (uint16_t *)0xffae;
        uVar5 = puVar2 - puVar1;
        uVar1 = uVar5 * -0x10 + 0xff94;
        uVar4 = uVar1 - puVar1;
        uVar8 = uVar4 * -0x10 + 0xff94;
        puVar1 = puVar1 + 1;
        uVar7 = uVar7 + 1;
    }

    return;
}