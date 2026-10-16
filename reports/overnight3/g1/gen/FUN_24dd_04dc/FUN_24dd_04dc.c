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

uint32_t FUN_24dd_04dc(uint16_t in_AX) {
    uint32_t result;
    uint16_t temp1 = (0xfff8 < in_AX) ? 1 : 0;
    uint16_t temp2 = (in_AX + 7) >> 1;
    uint16_t temp3 = temp2 >> 3;
    result = ((uint32_t)temp1 << 16) | ((uint32_t)temp3 << 8) | (in_AX + 7);
    return result & 0xffff0008;
}