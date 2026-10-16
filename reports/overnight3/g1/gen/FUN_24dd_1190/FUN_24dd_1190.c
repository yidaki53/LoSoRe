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

uint16_t FUN_24dd_1190(void) {
    uint32_t *puVar1;
    uint32_t uVar4, uVar8, uVar11, uVar12, uVar13, uVar14;
    uint32_t uVar3, uVar5, uVar6, uVar7, uVar9, uVar10;
    uint32_t lVar2;
    uint8_t bVar15;

    puVar1 = (uint32_t *)*(int *)0xd8;
    uVar11 = 0;
    uVar4 = 0;
    uVar8 = 0;
    if ((*(uint8_t *)((int)puVar1 + 0xf) & 0x80) != 0) {
        uVar4 = *puVar1;
        uVar8 = puVar1[1];
    }
    if ((*(uint8_t *)((int)puVar1 + 3) & 0x80) != 0) {
        bVar15 = (uVar4 + puVar1[6]) < uVar4;
        uVar4 += puVar1[6];
        uVar11 = bVar15;
        bVar15 = (uVar8 + puVar1[7]) < uVar8;
        uVar6 = uVar8 + puVar1[7];
        uVar8 = uVar6 + uVar11;
        uVar11 = bVar15 || (uVar6 + uVar11) < uVar6;
        if ((*(uint8_t *)((int)puVar1 + 0xf) & 0x80) != 0) {
            uVar11--;
        }
    }
    uVar7 = 0;
    uVar5 = (uint32_t)((uint64_t)puVar1[6] * (uint64_t)puVar1[2] >> 0x10);
    uVar3 = (uint32_t)((uint64_t)puVar1[6] * (uint64_t)puVar1[2]);
    uVar6 = (uVar4 + uVar3) < uVar4;
    uVar12 = uVar8 + uVar5;
    uVar9 = uVar12 + uVar6;
    uVar11 += uVar11 || (uVar8 + uVar5) < uVar8 || (uVar12 + uVar6) < uVar12;
    if (puVar1[8] != 0) {
        lVar2 = (uint64_t)puVar1[8] * (uint64_t)*puVar1;
        uVar6 = (uint32_t)(lVar2 >> 0x10);
        uVar4 += uVar3;
        uVar4 += lVar2;
        uVar8 = uVar9 + uVar6;
        uVar7 = uVar8 + (uVar4 < uVar8);
        uVar12 += uVar11 || (uVar9 + uVar6) < uVar9 || (uVar8 + (uVar4 < uVar8)) < uVar8;
        uVar6 = (uint32_t)((uint64_t)puVar1[8] * (uint64_t)puVar1[1] >> 0x10);
        uVar4 = (uint32_t)((uint64_t)puVar1[8] * (uint64_t)puVar1[1]);
        uVar9 = uVar7 + uVar4;
        uVar4 = (uVar7 + uVar4) < uVar7;
        uVar8 = uVar12 + uVar6;
        uVar11 = uVar8 + (uVar4 < uVar8);
        uVar7 += uVar7 || (uVar12 + uVar6) < uVar12 || (uVar8 + (uVar4 < uVar8)) < uVar8;
    }
    uVar5 = (uint32_t)((uint64_t)puVar1[6] * (uint64_t)puVar1[3] >> 0x10);
    uVar4 = (uint32_t)((uint64_t)puVar1[6] * (uint64_t)puVar1[3]);
    uVar10 = uVar9 + uVar4;
    uVar4 = (uVar9 + uVar4)