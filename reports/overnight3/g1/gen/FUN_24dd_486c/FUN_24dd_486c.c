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

// External function declarations
uint16_t FUN_24dd_489c(void);
uint16_t FUN_24dd_3dbd(void);

// Function implementation
uint16_t __stdcall16far FUN_24dd_486c(void) {
    uint16_t uVar1;
    uint16_t in_CX;
    int unaff_DI;
    uint16_t unaff_ES;
    uint8_t in_CF;

    uVar1 = FUN_24dd_489c();
    if (!(bool)in_CF && (uVar1 = in_CX, *((int*)(unaff_DI + 4)) != 1)) {
        uVar1 = FUN_24dd_3dbd();
    }
    return uVar1;
}