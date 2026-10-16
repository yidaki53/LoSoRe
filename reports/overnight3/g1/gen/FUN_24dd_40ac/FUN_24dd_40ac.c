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

void __stdcall16far FUN_24dd_40ac(uint param_1, uint16_t *param_2, uint16_t *param_3) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    uint uVar3;
    uint8_t bVar4;
    uint16_t *puVar5;
    uint16_t *puVar6;
    uint16_t uVar7;

    uVar7 = (uint16_t)(param_3 >> 16);
    puVar6 = (uint16_t *)param_3;
    puVar5 = (uint16_t *)param_2;
    bVar4 = (uint8_t)(param_1 >> 8);
    for (uVar3 = (uint)bVar4; uVar3 != 0; uVar3 = uVar3 - 1) {
        puVar1 = puVar6;
        puVar6 = puVar6 + 1;
        *puVar1 = 0;
    }
    for (uVar3 = param_1 & 0xff; uVar3 != 0; uVar3 = uVar3 - 1) {
        puVar2 = puVar6;
        puVar6 = puVar6 + 1;
        puVar1 = puVar5;
        puVar5 = puVar5 + 1;
        *puVar2 = *puVar1;
    }
    for (uVar3 = (uint)(uint8_t)(' ' - (char)param_1 - bVar4); uVar3 != 0; uVar3 = uVar3 - 1) {
        puVar1 = puVar6;
        puVar6 = puVar6 + 1;
        *puVar1 = 0;
    }
    return;
}