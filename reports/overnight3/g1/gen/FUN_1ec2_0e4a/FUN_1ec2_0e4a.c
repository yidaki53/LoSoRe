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

void __stdcall16far FUN_1ec2_0e4a(uint32_t param_1, int param_2, int param_3) {
    uint8_t bVar1;
    uint8_t *pbVar2;
    uint16_t uVar3;

    if (((-1 < param_3) && (param_3 < 0x9e)) && (-1 < param_2) && (param_2 < 0x9e)) {
        uVar3 = (uint16_t)(param_1 >> 16);
        pbVar2 = (uint8_t *)((param_1 & 0xFFFF) + param_2 * 0x140 + param_3);
        bVar1 = *pbVar2;
        if ((0x9f < bVar1) && (bVar1 < 0xa4)) {
            *pbVar2 = bVar1 + 4;
        }
    }
    return;
}