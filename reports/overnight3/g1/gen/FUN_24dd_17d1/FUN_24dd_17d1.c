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

void FUN_24dd_17d1(void) {
    uint32_t *puVar1;
    int32_t lVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    uint32_t uVar7;
    uint32_t uVar8;
    uint32_t uVar9;
    uint32_t uVar10;
    uint32_t uVar11;
    uint32_t uVar12;
    uint32_t uVar13;
    uint32_t uVar14;
    uint32_t uVar15;
    uint32_t uVar16;
    uint32_t uVar17;
    uint32_t uVar18;
    uint32_t uVar19;

    puVar1 = (uint32_t *)*(int *)0xd8;
    uVar4 = *puVar1;
    uVar14 = puVar1[1];
    uVar15 = puVar1[2];
    uVar16 = puVar1[3];
    uVar19 = 0;
    uVar3 = puVar1[4];
    uVar5 = uVar4;
    uVar11 = uVar15;
    uVar10 = uVar16;
    if (uVar3 != 0xc001) {
        if ((int)uVar3 < -0xf) {
            uVar10 = 0;
            uVar5 = uVar14;
            uVar11 = uVar16;
            uVar14 = uVar15;
            uVar3 = uVar3 + 0x10;
            uVar19 = uVar4;
        }
        while (uVar3 + 1 == 0 || (int)uVar3 < -1) {
            uVar4 = uVar10 & 1;
            uVar10 = uVar10 >> 1;
            uVar15 = uVar11 & 1;
            uVar19 = (uint32_t)((uVar5 & 1) != 0) >> 1;
            uVar5 = (uint32_t)((uVar14 & 1) != 0) >> 1;
            uVar11 = (uint32_t)(uVar4 != 0) >> 1;
            uVar14 = (uint32_t)(uVar15 != 0) >> 1;
            uVar3 = uVar3 + 1;
        }
    }
    uVar4 = (uint32_t)((uVar5 & 1) != 0) >> 1;
    uVar15 = (uint32_t)((uVar14 & 1) != 0) >> 1;
    *puVar1 = uVar5 + ((int)uVar19 < 0);
    puVar1[1] = uVar14 + uVar4;
    puVar1[2] = uVar11 + uVar15;
    puVar1[3] = uVar10 + (uint32_t)((uVar11 & 1) != 0) >> 1;
    uVar14 = 0;
    uVar4 = 0;
    if ((*(uint8_t *)((int)puVar1 + 3) & 0x80) != 0) {
        uVar14 = *puVar1 << 1;
        uVar4 = puVar1[1] << 1 | (uint32_t)((int)*puVar1 < 0);
    }
    uVar11 = (uint32_t)((uint64_t)*puVar1 * (uint64_t)puVar1[2] >> 0x10);
    uVar3 = (uint32_t)((uint64_t)*puVar1 * (uint64_t)puVar1[2]);
    uVar19 = uVar4 + uVar11 + (uint32_t)((uVar14 & 1) != 0) >> 1;
    uVar15 = (uint32_t)((uVar14 & 1) != 0) >> 1;
    uVar16 = uVar19 + uVar11;
    uVar5 = uVar16 + uVar15;
    uVar18 = (uint32_t)((uVar4 & 1) !=