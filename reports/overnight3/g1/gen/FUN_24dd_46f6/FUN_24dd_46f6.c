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

void FUN_24dd_4712(void);

void FUN_24dd_46f6(uint16_t in_AX, uint16_t in_DX, char *unaff_DI) {
    uint32_t uVar1;
    char cVar3;
    char bVar2;

    if ((int16_t)in_DX < 0) {
        FUN_24dd_4712();
        unaff_DI[-1] = '-';
        return;
    }

    do {
        uVar1 = (uint32_t)in_DX;
        in_DX = in_DX / 10;
        uVar1 = uVar1 % 10 << 16 | (uint32_t)in_AX;
        in_AX = (uint16_t)(uVar1 / 10);
        cVar3 = (char)(uVar1 % 10);
        bVar2 = cVar3 + '0';
        if (bVar2 > '9') {
            bVar2 = cVar3 + '7';
        }
        unaff_DI = unaff_DI - 1;
        *unaff_DI = bVar2;
    } while (in_AX != 0 || in_DX != 0);
}