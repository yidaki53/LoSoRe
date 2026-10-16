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

extern uint16_t FUN_24dd_345e(void);

uint16_t FUN_24dd_35b3(uint16_t in_AX, uint16_t *unaff_DI, uint16_t *unaff_SI, uint16_t *unaff_BX, uint16_t *unaff_CX) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t *puVar6;
    uint16_t uVar7;
    uint16_t uVar8;

    uVar8 = (uint16_t)((uint16_t)in_AX >> 16);
    uVar3 = (uint16_t)in_AX;
    uVar4 = (uint16_t)unaff_DI;
    uVar6 = (uint16_t)unaff_SI;
    uVar5 = (uint16_t)unaff_BX;
    uVar2 = (uint16_t)unaff_CX;

    while (true) {
        uVar1 = *puVar5;
        if (uVar1 == 0) break;
        uVar7 = uVar1;
        if ((0x39 < uVar7) && (uVar7 < 0x40)) {
            uVar8 = 0x3c;
            FUN_24dd_345e();
            uVar8 = 0x3a;
            continue;
        }
        uVar8 = 0x3a;
        break;
    }

    return uVar8;
}