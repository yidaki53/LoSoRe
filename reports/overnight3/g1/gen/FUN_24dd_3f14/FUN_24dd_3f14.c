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

void __stdcall16far FUN_24dd_3f14(uint16_t seg1, uint16_t off1, uint16_t seg2, uint16_t off2) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t bVar3;
    uint32_t uVar4;
    uint8_t *pbVar5;
    uint8_t *pbVar6;

    pbVar5 = (uint8_t *)(seg1 * 16 + off1);
    bVar2 = *(uint8_t *)(seg2 * 16 + off2);
    bVar3 = *pbVar5;
    bVar1 = *(uint8_t *)(seg2 * 16 + off2);
    *(uint8_t *)(seg2 * 16 + off2) = bVar1 + bVar3;
    if (bVar1 + bVar3 < bVar1) {
        *(uint8_t *)(seg2 * 16 + off2) = 0xff;
        bVar3 = ~bVar2;
    }
    pbVar6 = (uint8_t *)(seg2 * 16 + off2) + bVar2;
    uVar4 = (uint32_t)bVar3;
    while (true) {
        pbVar6 = pbVar6 + 1;
        pbVar5 = pbVar5 + 1;
        if (uVar4 == 0) break;
        uVar4 = uVar4 - 1;
        *pbVar6 = *pbVar5;
    }
    return;
}