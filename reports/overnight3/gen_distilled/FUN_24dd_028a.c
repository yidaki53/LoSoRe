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

void __stdcall16far FUN_24dd_028a(void) {
    // Assuming 0x24dd:0283 is a function call with parameter 0x6.
    FUN_24dd_0233(0x6);

    // If the carry flag is set after the call, perform the following:
    if (carry_flag) {
        // Assuming 0x24dd:029f is a jump to 0x24dd:0293.
        goto 0x24dd:0293;
    }

    // If the carry flag is not set, perform the following:
    // Assuming 0x24dd:029c is a jump to 0x24dd:0299.
    goto 0x24dd:0299;
}