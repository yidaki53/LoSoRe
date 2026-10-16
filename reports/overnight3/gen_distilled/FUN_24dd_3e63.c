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

uint16_t FUN_24dd_3e63(uint16_t in_AX, uint16_t in_CX, uint16_t in_DX) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint16_t uVar3;
    uint16_t uVar4;

    if (*(char *)(0x6420) < 2) {
        for (uVar3 = in_CX & 0x1f; uVar3 != 0; uVar3--) {
            uVar2 = in_DX & 1;
            in_DX >>= 1;
            in_AX = ((uint16_t)(uVar2 != 0) << 15) | (in_AX >> 1);
        }
        return in_AX;
    }
    uVar4 = in_CX & 0x1f;
    in_DX = in_DX >> uVar4;
    in_AX = in_AX >> uVar4;
    return in_AX;
}