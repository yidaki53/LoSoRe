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

void FUN_24dd_4905(uint16_t param1, uint16_t param2, uint8_t param3) {
    uint16_t bx = param1;
    uint16_t cx = param2;
    uint8_t al = param3;
    uint16_t es_di = *(uint16_t *)(bx + 8);
    uint16_t es = es_di >> 16;
    uint16_t di = es_di & 0xFFFF;

    __asm__ volatile (
        "cld\n\t"
        "rep stosb\n\t"
        : "+D" (di), "+c" (cx)
        : "a" (al), "m" (es)
        : "memory"
    );

    __asm__ volatile (
        "retf $0x8\n\t"
    );
}