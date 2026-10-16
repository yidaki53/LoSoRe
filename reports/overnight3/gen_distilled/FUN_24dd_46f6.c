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

void FUN_24dd_46f6(void) {
    int in_AX;
    uint in_DX;
    char *unaff_DI;
    char *unaff_SI;

    if ((int16_t)in_DX < 0) {
        FUN_24dd_4522();
        unaff_DI = (char *)in_AX;
        unaff_SI = (char *)0xa;
        while (true) {
            *unaff_DI = '-';
            unaff_DI++;
            if (in_CX == 0) break;
            in_CX--;
            *unaff_SI = 0;
            unaff_SI++;
        }
    } else {
        unaff_DI = (char *)in_AX;
        unaff_SI = (char *)0xa;
        while (true) {
            *unaff_DI = '-';
            unaff_DI++;
            if (in_CX == 0) break;
            in_CX--;
            *unaff_SI = 0;
            unaff_SI++;
        }
    }
    return;
}