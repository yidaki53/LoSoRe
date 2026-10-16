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

extern void swi(uint16_t);

uint16_t FUN_24dd_2361(uint16_t in_AX, uint16_t in_CX, uint16_t in_BX, uint16_t unaff_ES) {
    uint16_t uVar5;
    uint8_t bVar4;
    uint8_t bVar2;
    uint16_t uVar3;
    uint16_t *ptr_d0 = (uint16_t *)0xd0;
    uint16_t *ptr_d2 = (uint16_t *)0xd2;
    uint8_t *ptr_d4 = (uint8_t *)0xd4;
    uint8_t *ptr_d6 = (uint8_t *)0xd6;

    uVar5 = ((uint16_t)((uint8_t)(in_CX >> 8)) << 8) | *ptr_d6;
    bVar4 = (uint8_t)uVar5 ^ 0x3f;
    bVar2 = *ptr_d4 | (uint8_t)(uVar5 >> 8);
    if (((bVar2 & bVar4 ^ bVar2) & 8) != 0) {
        bVar2 = bVar2 | 0x20;
    }
    if ((bVar4 & bVar2) != 0) {
        *ptr_d4 = bVar2 | 0x80;
        if ((bVar2 & bVar4) == 0x20) {
            return in_AX;
        }
        swi(0x21);
        *ptr_d0 = in_BX;
        *ptr_d2 = unaff_ES;
        uVar3 = (*(uint16_t(*)())*ptr_d0)();
        return uVar3;
    }
    *ptr_d4 = bVar2 & 0x7f;
    return in_AX;
}