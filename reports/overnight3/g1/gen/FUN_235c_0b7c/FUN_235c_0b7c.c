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

void FUN_235c_0b7c(void) {
    int16_t local_4 = -0x400;
    while (true) {
        int16_t local_6 = local_4;
        if (local_4 < -0x80) {
            local_6 = -0x80;
        }
        if (0x7f < local_6) {
            local_6 = 0x7f;
        }
        *((char *)(0x235c * 16 + 0x7286 + local_4)) = (char)local_6 + -0x80;
        if (local_4 == 0x400) break;
        local_4 = local_4 + 1;
    }
    return;
}