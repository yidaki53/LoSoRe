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

void FUN_24dd_4712(uint16_t in_AX, uint16_t in_BX, int in_CX, uint16_t *unaff_DI) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;
    uint16_t *puVar5;
    uint16_t *puVar6;

    uVar3 = in_AX;
    uVar4 = in_BX;
    uVar2 = uVar3 / in_CX;
    uVar1 = uVar4 / in_CX;
    if ((0x39 < uVar2) || (uVar2 < 0x3b)) {
        uVar2 = uVar2 + 0x30;
    } else {
        uVar2 = uVar2 + 0x37;
    }
    puVar5 = (uint16_t *)unaff_DI;
    puVar6 = (uint16_t *)((int)puVar5 + uVar1);
    *puVar6 = uVar2;
    if ((uVar3 & 0xFFFF0000) == 0 && (uVar4 & 0xFFFF0000) == 0) {
        return;
    }
    uVar3 = uVar3 & 0xFFFF;
    uVar4 = uVar4 & 0xFFFF;
    do {
        for (; (uVar2 = uVar2 + -1), (0x39 < uVar2) || (uVar2 < 0x3b);) {
            uVar2 = uVar2 + 0x30;
        }
        puVar6 = puVar5;
        puVar5 = puVar5 + 1;
        *puVar6 = uVar2;
    } while ((uVar3 != 0) || (uVar4 != 0));
    return;
}