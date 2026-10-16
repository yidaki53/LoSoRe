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

void FUN_24dd_1519(void) {
    uint16_t *puVar1;
    uint32_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    int32_t iVar7;
    uint32_t uVar8;
    uint32_t uVar9;
    int32_t iVar10;
    int32_t iVar11;
    uint32_t uVar12;

    puVar1 = (uint16_t *)*(uint16_t *)0xd8;
    uVar9 = puVar1[3];
    uVar6 = puVar1[2];
    uVar8 = puVar1[1];
    iVar11 = (int32_t)puVar1[4] >> 1;
    uVar3 = uVar6;
    if ((puVar1[4] & 1) != 0) {
        iVar11 = iVar11 + 1;
        uVar3 = uVar9 & 1;
        uVar9 = uVar9 >> 1;
        uVar3 = (uint32_t)(((uVar3 != 0) << 15) | (uVar6 >> 1));
        uVar8 = (uint32_t)(((uVar6 & 1) != 0) << 15) | (uVar8 >> 1);
    }
    if (uVar9 < 0xfffe) {
        uVar6 = (uint32_t)(((uint32_t)uVar9 | 0x10000) >> 1);
        while (true) {
            uVar4 = (uint32_t)(((uint32_t)uVar9 << 16) | uVar3) / (uint32_t)uVar6;
            if (uVar6 - 1 <= uVar4) break;
            uVar6 = (uint32_t)(((uint32_t)uVar6 + uVar4) >> 1);
            if (((uint32_t)uVar6 + uVar4) < uVar6) uVar6 |= 0x8000;
        }
        uVar5 = uVar4;
        uVar12 = uVar6;
        if (uVar6 < uVar4) {
            uVar5 = uVar6;
            uVar12 = uVar4;
        }
        uVar2 = (((uint32_t)uVar9 << 16) | uVar3) % (uint32_t)uVar6;
        uVar2 = (uVar2 << 16) | uVar8;
        uVar2 /= (uint32_t)uVar12;
        uVar6 = (uint32_t)(((uint32_t)uVar12 + uVar5 & 1) << 15) | (uVar2 & 0xffff);
        uVar6 >>= 1;
        uVar9 = (uint32_t)(uVar2 & 1);
        iVar7 = uVar6 + uVar9;
        iVar10 = (int32_t)(((uint32_t)uVar12 + uVar5) >> 1);
        if (((uint32_t)uVar12 + uVar5) < uVar12) iVar10 |= 0x8000;
        if (((uint32_t)uVar6 + uVar9) < uVar6) iVar10++;
    } else {
        iVar10 = (int32_t)(((uint32_t)uVar9 | 0x10000) >> 1);
        iVar7 = (int32_t)(((uint32_t)uVar9 & 1) << 15) | (uVar3 >> 1);
    }
    puVar1[0] = 0;
    puVar1[1] = 0;
    puVar1[2] = (uint16_t)iVar7;
    puVar1[3] = (uint16_t)iVar10;
    puVar1[4] = (uint16_t)iVar11;
    puVar1[5] = 0;
    return;
}