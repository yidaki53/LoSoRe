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

void FUN_24dd_35d4(void) {
    uint16_t ax = __AX;
    uint16_t bx;
    uint16_t cx;
    uint16_t dx;
    uint16_t si;
    uint16_t di;
    uint16_t bp;
    uint16_t sp;
    uint16_t ds;
    uint16_t es;
    uint16_t ss;

    if (0x1000 < ax) {
        bx = 0x3c;
        __asm__("int 0x21" : "=a"(ax) : "a"(bx));
        ax = ax - 0xfff;
    }
    if (ax < -0x1000) {
        bx = 0x3c;
        __asm__("int 0x21" : "=a"(ax) : "a"(bx));
        ax = ax + 0x1001;
    }
    if (ax != 0) {
        bx = 0x3c;
        __asm__("int 0x21" : "=a"(ax) : "a"(bx));
        cx = FUN_24dd_1ee4();
        cx = cx >> 1;
        while (cx != 0) {
            bx = cx & 1;
            cx = cx >> 1;
            if (bx != 0) {
                bx = 0x3c;
                __asm__("int 0x21" : "=a"(dx) : "a"(bx));
                bx = ((uint16_t)(dx >> 8) << 8) | ((uint16_t)dx + '3');
            }
        }
        if (-1 < ax) {
            bx = 0x3a;
            __asm__("int 0x21" : "=a"(ax) : "a"(bx));
            return;
        }
        bx = 0x3a;
        __asm__("int 0x21" : "=a"(ax) : "a"(bx));
    }
    return;
}