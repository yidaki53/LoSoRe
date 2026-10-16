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

void __stdcall16far FUN_24dd_0303(void) {
    uint16_t *puVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    uint16_t uVar9;
    uint16_t uVar10;

    uVar10 = *(uint16_t *)0x63f0;
    uVar9 = *(uint16_t *)0x63f6;
    uVar8 = *(uint16_t *)0x63f4;
    uVar7 = *(uint16_t *)0x63ee;
    uVar6 = *(uint16_t *)0x63f2;

    uVar3 = uVar8;
    if ((uVar6 & 0xf) != 0) {
        uVar3 = uVar9;
    }

    uVar1 = uVar6;
    if ((uVar6 & 0xf0) != 0) {
        uVar1 = uVar7;
    }

    uVar2 = uVar6;
    if ((uVar6 & 0xf0) != 0) {
        uVar2 = uVar8;
    }

    uVar5 = uVar6;
    if ((uVar6 & 0xf0) != 0) {
        uVar5 = uVar9;
    }

    uVar4 = uVar6;
    if ((uVar6 & 0xf0) != 0) {
        uVar4 = uVar10;
    }

    ((void (*)(uint16_t, uint16_t))uVar6)(uVar3, uVar4);
    uVar2 = uVar6;
    if ((uVar6 & 0xf0) != 0) {
        uVar2 = uVar8;
    }

    uVar1 = uVar6;
    if ((uVar6 & 0xf0) != 0) {
        uVar1 = uVar9;
    }

    ((void (*)(uint16_t, uint16_t))uVar6)(uVar5, uVar6);
    ((void (*)(uint16_t, uint16_t))uVar6)(uVar6, uVar7);
    ((void (*)(uint16_t, uint16_t))uVar6)(uVar8, uVar9);
    ((void (*)(uint16_t, uint16_t))uVar6)(uVar9, uVar10);
    return;
}