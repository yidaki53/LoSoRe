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

void __stdcall16far FUN_1ec2_12ad(uint32_t param_1, uint8_t param_2, int param_3, uint32_t param_4, int param_5) {
    uint16_t *puVar1;
    uint32_t uVar2;
    uint16_t *puVar3;
    uint16_t uVar4;

    uVar4 = (uint16_t)(param_1 >> 16);
    puVar3 = (uint16_t *)((uint32_t)param_1 + param_3 * 0x140 + param_5);
    uVar2 = param_4 >> 1;
    if ((param_4 & 1) != 0) {
        puVar1 = puVar3;
        puVar3 = (uint16_t *)((uint32_t)puVar3 + 1);
        *(uint8_t *)puVar1 = param_2;
    }
    for (; uVar2 != 0; uVar2--) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar1 = ((uint16_t)param_2 << 8) | param_2;
    }
    puVar3 = (uint16_t *)((uint32_t)puVar3 + (0x140 - param_4));
    uVar2 = param_4 >> 1;
    if ((param_4 & 1) != 0) {
        puVar1 = puVar3;
        puVar3 = (uint16_t *)((uint32_t)puVar3 + 1);
        *(uint8_t *)puVar1 = param_2;
    }
    for (; uVar2 != 0; uVar2--) {
        puVar1 = puVar3;
        puVar3 = puVar3 + 1;
        *puVar1 = ((uint16_t)param_2 << 8) | param_2;
    }
    return;
}