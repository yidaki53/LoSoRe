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

uint16_t FUN_24dd_455e(uint16_t in_AX, uint16_t in_DX) {
    uint16_t uVar1;
    uint8_t bVar2;
    int iVar3;
    uint16_t uVar4;
    uint16_t uVar5;

    if (in_AX != 0 || in_DX != 0) {
        if ((int16_t)in_DX < 0) {
            uVar4 = -in_AX;
            uVar5 = -in_DX;
            bVar2 = (uint8_t)(uVar5 >> 8);
            uVar1 = uVar4 ^ uVar5;
            iVar3 = (int16_t)uVar5;
            if (bVar2 != 0) {
                iVar3 = -iVar3;
            }
            return ((uint16_t)(iVar3 >> 8) << 16) | iVar3;
        }
        uVar1 = 0;
        bVar2 = (uint8_t)(in_DX >> 8);
        while (true) {
            uVar5 = in_DX;
            in_DX = in_DX / 10;
            uVar4 = in_AX;
            in_AX = uVar5 - (in_AX * 10);
            if (bVar2 != 0) {
                iVar3 = -uVar4;
            } else {
                iVar3 = uVar4;
            }
            if (in_AX == 0 && in_DX == 0) break;
            uVar1 = ((uint16_t)(iVar3 >> 8) << 16) | iVar3;
        }
        return uVar1;
    }
    return 0;
}