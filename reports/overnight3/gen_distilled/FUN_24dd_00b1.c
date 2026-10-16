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

void FUN_24dd_00b1(void) {
    uint16_t uVar1;
    uint8_t bVar2;
    uint8_t *pbVar3;

    uVar1 = (uint16_t)((uint8_t)(uint16_t)0x0000 << 16) | 0x0000;
    bVar2 = (uint8_t)(uint16_t)0x0000;
    pbVar3 = (uint8_t *)0x6420;
    if ((bVar2 & 0xf0) != 0xf0) {
        do {
            uVar1 = (uint16_t)((uint8_t)(uint16_t)0x0000 << 16) | 0x0001;
            bVar2 = (uint8_t)(uint16_t)0x0000;
            pbVar3 = (uint8_t *)0x6420;
        } while ((bVar2 & 0xf0) != 0xf0);
    }
    do {
        uVar1 = (uint16_t)((uint8_t)(uint16_t)0x0000 << 16) | 0x0001;
        bVar2 = (uint8_t)(uint16_t)0x0000;
        pbVar3 = (uint8_t *)0x6420;
    } while ((bVar2 & 0xf0) != 0xf0);
    *pbVar3 = (uint8_t)0x00;
    return;
}