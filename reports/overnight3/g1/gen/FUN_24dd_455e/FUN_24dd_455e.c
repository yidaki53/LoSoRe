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

void FUN_24dd_455e(uint16_t in_AX, uint16_t in_DX) {
    uint16_t uVar1;
    bool bVar2;

    if (in_AX != 0 || in_DX != 0) {
        if ((int16_t)in_DX < 0) {
            bVar2 = in_AX != 0;
            in_AX = -in_AX;
            in_DX = -(uint16_t)bVar2 - in_DX;
        }
        uVar1 = in_AX;
        if ((in_DX == 0) && (uVar1 = 0, in_DX = in_AX, (char)(in_AX >> 8) == '\0')) {
            in_DX = in_AX << 8;
        }
        while (-1 < (int16_t)in_DX) {
            in_DX = in_DX * 2 + (uint16_t)((uVar1 & 0x8000) != 0);
            uVar1 = uVar1 * 2;
        }
    }
    return;
}