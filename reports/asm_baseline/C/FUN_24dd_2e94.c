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

uint16_t FUN_24dd_2e94(uint32_t stack_param) {
    uint8_t bVar1;
    uint16_t in_AX;
    uint8_t uVar3;
    uint32_t uVar2;
    int32_t iVar4;
    uint16_t uVar5;

    uVar5 = (uint16_t)(stack_param >> 16);
    iVar4 = (int32_t)stack_param;
    uVar2 = *(uint32_t *)(iVar4 - 1);
    uVar3 = (uint8_t)(uVar2 >> 8);
    bVar1 = (char)uVar2 - 0x34;
    if (bVar1 < 8) {
        *(int32_t *)(iVar4 - 2) = *(int32_t *)(iVar4 - 2) - 0x5c32;
    } else if (bVar1 < 9) {
        if ((uVar2 & 0x2000) == 0) {
            *(uint8_t *)(iVar4 - 2) = 0x9b;
            uVar2 = (uVar3 << 8) | uVar3;
            uVar2 &= 0x7c0;
            *(int32_t *)(iVar4 - 1) = (((char)(uVar2 >> 8) << 8) | (uVar2 >> 3)) ^ 0x18 + 0xd826;
        }
    } else if (bVar1 < 10) {
        *(uint16_t *)(iVar4 - 2) = 0x9b90;
    }
    return in_AX;
}