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

void FUN_24dd_4712(void) {
    uint16_t ax = __AX;
    uint16_t bx = __BX;
    uint16_t si = __SI;
    uint16_t di = __DI;
    uint32_t uVar1;
    uint8_t bVar2;
    char cVar3;

    do {
        uVar1 = (uint32_t)bx;
        bx = bx / si;
        uVar1 = uVar1 % (uint32_t)si << 16 | (uint32_t)ax;
        ax = (uint16_t)(uVar1 / si);
        cVar3 = (char)(uVar1 % (uint32_t)si);
        bVar2 = cVar3 + 0x30;
        if (0x39 < bVar2) {
            bVar2 = cVar3 + 0x37;
        }
        di = di - 1;
        *((uint8_t *)di) = bVar2;
    } while (ax != 0 || bx != 0);
}