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

uint16_t __cdecl16far FUN_24dd_3e63(void) {
    uint16_t ax = __AX;
    uint16_t cx = __CX;
    uint16_t dx = __DX;
    uint8_t bVar1;
    uint16_t uVar2;
    uint16_t uVar3;

    if (*(uint8_t *)(0x6420) < 2) {
        for (uVar3 = cx & 0x1f; uVar3 != 0; uVar3--) {
            uVar2 = dx & 1;
            dx = dx >> 1;
            ax = (uint16_t)(((uVar2 != 0) << 15) | (ax >> 1));
        }
        return ax;
    }
    bVar1 = (uint8_t)cx & 0x1f;
    return (uint16_t)((ax >> bVar1) | (dx << (0x10 - bVar1)));
}