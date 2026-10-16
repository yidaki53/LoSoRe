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

void FUN_24dd_3ed3(void) {
    uint16_t bx = __builtin_return_address(0);
    uint16_t dx = __builtin_frame_address(0);
    uint16_t di = *(uint16_t *)(bx + 0xc);
    uint16_t si = *(uint16_t *)(bx + 0x8);
    uint8_t al = *(uint8_t *)si;
    uint8_t ah = 0;
    uint16_t cx = *(uint16_t *)(bx + 0x6);
    if (cx <= 0) {
        cx = 1;
        si += cx;
        al -= cx;
        if (al < 0) {
            al++;
        }
    }
    cx = *(uint16_t *)(bx + 0x4);
    if (cx < 0) {
        cx = 0;
        if (al <= cx) {
            al = cx;
        }
    }
    if (al == 0) {
        *(uint8_t *)di = 0;
        cx = 0;
    } else {
        __asm__ volatile ("rep movsb" : "+D"(di), "+S"(si), "+c"(cx) : : "memory");
    }
    dx = __builtin_frame_address(0);
    __asm__ volatile ("retf $0x8");
}