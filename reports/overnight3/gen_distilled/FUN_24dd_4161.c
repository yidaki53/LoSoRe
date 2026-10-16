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

uint16_t FUN_24dd_4161(uint16_t in_AX, uint16_t in_DX) {
    uint16_t uVar1;
    uint8_t bVar2;
    uint8_t bVar3;
    uint8_t bVar4;

    bVar4 = (uint8_t)(in_DX >> 8);
    uVar1 = in_DX;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar3 = (uint8_t)(in_DX >> 8);
    if ((in_DX & 0x8000) != 0) {
        bVar4 = ~bVar4;
    }
    uVar1 = ((uint16_t)(bVar2 >> 8) << 16) | bVar3;
    bVar3 = (uint8_t)(in_DX >> 8);
    bVar4 = ((uint16_t)bVar4 << 8) | bVar3;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar4 << 8) | bVar2;
    bVar3 = (uint8_t)(in_DX >> 8);
    bVar2 = ((uint16_t)bVar1 << 8) | bVar3;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar2 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (uint8_t)(in_DX >> 8);
    bVar1 = ((uint16_t)bVar3 << 8) | bVar2;
    bVar4 = (uint8_t)(in_DX >> 8);
    bVar3 = ((uint16_t)bVar1 << 8) | bVar4;
    bVar2 = (