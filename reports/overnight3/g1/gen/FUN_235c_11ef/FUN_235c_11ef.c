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

void out(uint16_t port, uint8_t value);

void FUN_235c_11ef(void) {
    out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ee));
    out(*(uint16_t *)(0x67e0), 0);
    out(*(uint16_t *)(0x67e2), *(uint8_t *)(0x67ef));
    out(*(uint16_t *)(0x67e4), *(uint8_t *)((uint16_t)*(uint8_t *)(0x6854) * 2 + 0x6e80));
    out(*(uint16_t *)(0x67e4), *(uint8_t *)((uint16_t)*(uint8_t *)(0x6854) * 2 + 0x6e81));
    out(*(uint16_t *)(0x67e6), (char)*(uint16_t *)(0x67f0) - 1);
    out(*(uint16_t *)(0x67e6), (char)(((uint16_t)*(uint16_t *)(0x67f0) - 1) >> 8));
    out(*(uint16_t *)(0x67e8), *(uint8_t *)(*(uint8_t *)(0x6854) + 0x6e7f));
    out(*(uint16_t *)(0x67de), *(uint8_t *)(0x67ed));
    FUN_235c_0000(0x14);
    FUN_235c_0000(0xffff);
    FUN_235c_0000(1);
    return;
}