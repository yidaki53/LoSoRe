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

void FUN_24dd_047d(uint16_t *cx, int bx, uint16_t *di, int es) {
    uint8_t bVar3;
    int iVar1;
    int iVar2;
    int iVar4;

    bVar3 = (uint8_t)((int)cx + cx[2]);
    if ((bx + cx[3] + (0xf < bVar3) != es) ||
        ((uint16_t)(((uint)((int)cx + cx[2]) >> 8) << 8) | (bVar3 - 0x10) & 0xff0f) != di) {
        *cx = di;
        cx[1] = es;
        return;
    }
    if ((es == *(int *)0x63f0) && (di == (uint16_t *)*(uint16_t *)0x63ee)) {
        *(uint16_t *)0x63ee = cx;
        *(int *)0x63f0 = bx;
        return;
    }
    *cx = *di;
    cx[1] = di[1];
    iVar1 = di[3];
    iVar4 = di[2] + cx[2];
    iVar2 = cx[3];
    bVar3 = (uint8_t)iVar4;
    cx[2] = ((uint16_t)(((uint)iVar4 >> 8) << 8) | (bVar3 - 0x10) & 0xff0f);
    cx[3] = iVar1 + iVar2 + (0xf < bVar3);
    return;
}