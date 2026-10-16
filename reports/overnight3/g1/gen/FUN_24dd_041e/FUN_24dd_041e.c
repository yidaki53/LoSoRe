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

void FUN_24dd_041e(uint16_t in_AX, void *in_CX, uint16_t in_BX) {
    uint32_t *puVar1;
    uint32_t *puVar2;
    uint32_t *puVar3;
    uint16_t uVar4;
    uint32_t uVar5;

    if ((((in_AX != 0) && (((uint32_t)in_CX & 0xfff7) == 0)) &&
        ((*(uint32_t *)0x63ec < in_BX ||
         ((*(uint32_t *)0x63ec <= in_BX && ((uint32_t *)*(uint32_t *)0x63ea <= in_CX)))))) &&
       ((in_BX < *(uint32_t *)0x63f0 ||
        ((in_BX <= *(uint32_t *)0x63f0 && (in_CX < (uint32_t *)*(uint32_t *)0x63ee)))))) {
        uVar5 = FUN_24dd_04dc();
        *(int *)(in_CX + 1) = (int)uVar5;
        *(uint16_t *)((int)in_CX + 6) = (uint16_t)((uVar5 >> 0x10) & 0xFFFF);
        puVar3 = (uint32_t *)0x63f6;
        do {
            do {
                uVar4 = *(uint16_t *)puVar3;
                puVar2 = puVar3;
                puVar1 = (uint32_t *)*(uint32_t *)puVar2;
                puVar3 = (uint32_t *)puVar1;
            } while (uVar4 < in_BX);
            if (in_BX < uVar4) goto LAB_24dd_046f;
        } while (puVar3 < in_CX);
        if (in_CX != puVar3) {
LAB_24dd_046f:
            FUN_24dd_047d(puVar2, uVar4);
            FUN_24dd_047d();
            return;
        }
    }
    return;
}