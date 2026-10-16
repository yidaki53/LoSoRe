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
void FUN_24dd_37ec(void);
void FUN_24dd_3a7f(void);
void FUN_24dd_39(void);

// Placeholder for the swi function
typedef void (*swi_func_t)(void);

// Placeholder for the out function
void out(uint16_t port, uint8_t value);

uint16_t FUN_24dd_3a7f(void) {
    swi_func_t swi_35 = (swi_func_t)(0x35 * 16);
    swi_func_t swi_3d = (swi_func_t)(0x3d * 16);
    swi_func_t swi_39 = (swi_func_t)(0x39 * 16);

    FUN_24dd_37ec();
    uint8_t uVar2 = swi_35();
    out(0x6410, uVar2);
    swi_3d();
    *(uint16_t *)0x6410 = 0x6a;
    uint16_t uVar3 = swi_39();
    return uVar3 ^ 0xcdee;
}