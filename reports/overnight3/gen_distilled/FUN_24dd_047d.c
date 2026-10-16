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

void FUN_24dd_047d(uint16_t in_AX, uint16_t in_DX, uint16_t *unaff_DI, uint16_t *unaff_ES) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t *puVar6;
    uint16_t uVar7;
    uint16_t uVar8;
    uint16_t uVar9;
    uint16_t uVar10;

    uVar10 = (uint16_t)((uint8_t)(in_DX >> 8));
    uVar9 = (uint16_t)((uint8_t)in_DX);
    uVar8 = (uint16_t)((uint8_t)(in_AX >> 8));
    uVar7 = (uint16_t)((uint8_t)in_AX);
    puVar5 = (uint16_t *)unaff_DI;
    puVar6 = (uint16_t *)unaff_ES;

    if ((in_DX == *(uint16_t *)0x63f0) && (in_AX == *(uint16_t *)0x63ee)) {
        *(uint16_t *)0x63ee = uVar10;
        *(uint16_t *)0x63f0 = uVar8;
        return;
    }

    uVar3 = *puVar5;
    uVar4 = *puVar6;
    uVar2 = uVar10;
    uVar1 = uVar9;
    uVar6 = uVar8;
    uVar5 = uVar7;

    if ((uVar2 < uVar1) || ((uVar2 == uVar1) && (uVar3 < uVar5))) {
        uVar6 = uVar5;
        uVar4 = uVar3;
    }

    uVar1 = ((uint16_t)(uVar6 >> 8) << 16) | uVar6;
    uVar8 = ((uint16_t)(uVar8 >> 8) << 16) | uVar8;
    uVar3 = ((uint16_t)(uVar4 >> 8) << 16) | uVar4;
    uVar2 = ((uint16_t)(uVar3 >> 8) << 16) | uVar3;

    *(uint16_t *)puVar5 = uVar1;
    *(uint16_t *)puVar6 = uVar2;

    uVar1 = ((uint16_t)(uVar9 >> 8) << 16) | uVar9;
    uVar2 = ((uint16_t)(uVar8 >> 8) << 16) | uVar8;

    *(uint16_t *)puVar5 = uVar1;
    *(uint16_t *)puVar6 = uVar2;

    return;
}