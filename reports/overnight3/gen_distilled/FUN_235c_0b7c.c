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
    int *memory = (int *)0x7286; // Assuming 0x7286 is the offset in the segment
    int *base = (int *)0xfc00; // Assuming 0xfc00 is the base address

    for (int i = -0x400; i < 0x400; i++) {
        if (i < -0x80) {
            i = -0x80;
        }
        if (0x7f < i) {
            i = 0x7f;
        }
        memory[i + 0x80] = base[i] + 0x80;
    }
}