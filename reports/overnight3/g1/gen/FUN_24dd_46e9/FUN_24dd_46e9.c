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

void __cdecl16far FUN_24dd_46e9(void) {
    uint16_t in_CX;
    uint16_t extraout_DX;

    // Assuming swi(0x21) is a software interrupt call, which is not directly translatable to C.
    // This is a placeholder for the actual interrupt handling logic.
    // For demonstration purposes, let's assume it sets in_CX and extraout_DX.
    in_CX = 0x1234; // Example value
    extraout_DX = 0x5678; // Example value

    *(uint16_t *)0x6412 = in_CX;
    *(uint16_t *)0x6414 = extraout_DX;
    return;
}