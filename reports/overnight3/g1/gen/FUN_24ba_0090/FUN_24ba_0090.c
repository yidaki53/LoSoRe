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

void FUN_24dd_4905(uint16_t, uint16_t, uint16_t, uint16_t);
void FUN_24cb_007c(uint16_t, uint16_t, uint16_t);
void FUN_24cb_0094(uint16_t, uint16_t, uint16_t);

void __cdecl16far FUN_24ba_0090(void) {
    *(uint8_t *)0x78ec = 0;
    FUN_24dd_4905(0, 0xab, 0x783c, 0);
    FUN_24cb_007c(0x78e8, 0, 9);
    FUN_24cb_0094(0, 0x24ba, 9);
    return;
}