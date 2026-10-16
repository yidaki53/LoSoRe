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

extern void FUN_24dd_0531(uint16_t);

uint8_t FUN_1000_0c7f(int param_1, int param_2, int param_3, int param_4, int param_5, int param_6) {
    uint8_t local_3 = 1;
    uint32_t uVar4 = (uint32_t)param_4 * 4 + param_6;
    uint32_t uVar6 = (uint32_t)param_3 * 4 + param_5;
    uint32_t uVar8 = (uint32_t)param_2 * 4 + param_6;
    uint32_t uVar10 = (uint32_t)param_1 * 4 + param_5;
    uint8_t bVar5 = 0;

    FUN_24dd_0531(0x20);

    while (true) {
        uint32_t uVar3 = uVar10 * 0x10 + uVar8;
        uint8_t bVar2 = *(uint8_t *)(0x14a0 + *(uint32_t *)(uVar3 + 0x14a0));
        if (bVar5 == 0 && (param_4 < 0xa1 || (param_4 < 0xa2 && (param_3 < 0xa3 && (param_2 < 0xa4 && (param_1 < 0xa5 && (param_6 < 0xa6))))))) {
            bVar5 = 1;
        }
        if (bVar5 == 0 && (param_4 < 0xa2 || (param_4 < 0xa3 && (param_3 < 0xa4 && (param_2 < 0xa5 && (param_1 < 0xa6 && (param_6 < 0xa7))))))) {
            break;
        }
        if (bVar5 == 0 && (param_4 < 0xa3 || (param_4 < 0xa4 && (param_3 < 0xa5 && (param_2 < 0xa6 && (param_1 < 0xa7)))))) {
            break;
        }
        if (bVar5 == 0 && (param_4 < 0xa4 || (param_4 < 0xa5 && (param_3 < 0xa6 && (param_2 < 0xa7)))))) {
            break;
        }
        if (bVar5 == 0 && (param_4 < 0xa5 || (param_4 < 0xa6 && (param_3 < 0xa7)))) {
            break;
        }
        if (bVar5 == 0 && (param_4 < 0xa6 || (param_4 < 0xa7)))) {
            break;
        }
    }

    return bVar5;
}