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

void FUN_202c_18c0(char param_1, uint16_t param_2, int16_t param_3, uint16_t param_4, int16_t param_5, int16_t param_6,
                 uint16_t param_7, uint16_t param_8, uint16_t param_9, uint16_t param_10,
                 uint8_t param_11) {
    uint16_t uVar1;
    uint8_t bVar2;
    uint8_t uVar3;
    char cVar4;
    uint16_t uVar5;
    uint16_t uVar6;
    uint16_t uVar7;
    uint16_t *puVar8;
    int16_t iVar9;
    int16_t iVar10;
    uint16_t uVar11;
    int16_t local_6;
    int16_t local_4;

    for (local_4 = 0; (*(char *)((int)*(uint32_t *)0x6688 + local_4 * 0x14 + 0x10) != '\0' && (local_4 < 600)); local_4++) {
    }
    bVar2 = param_11 & 0x7f;
    *(uint8_t *)((int)*(uint32_t *)0x6688 + local_4 * 0x14 + 0x10) = param_11;
    uVar11 = (uint16_t)((uint32_t)*(uint32_t *)0x6688 >> 0x10);
    puVar8 = (uint16_t *)((int)*(uint32_t *)0x6688 + local_4 * 0x14);
    *puVar8 = param_9;
    puVar8[1] = param_10;
    uVar11 = (uint16_t)((uint32_t)*(uint32_t *)0x6688 >> 0x10);
    iVar9 = (int)*(uint32_t *)0x6688 + local_4 * 0x14;
    *(uint16_t *)(iVar9 + 4) = param_7;
    *(uint16_t *)(iVar9 + 6) = param_8;
    uVar5 = FUN_24dd_4654(*(int *)((uint)bVar2 * 2 + 0xc7c) << 1);
    iVar12 = 0;
    uVar1 = *(uint16_t *)((uint)bVar2 * 2 + 0xc7c);
    param_6 = param_6 >> 0xf;
    iVar9 = param_6;
    FUN_24dd_3d80();
    uVar6 = FUN_24dd_3dbd();
    uVar7 = (uVar6 + param_4) - uVar1;
    uVar11 = (uint16_t)((uint32_t)*(uint32_t *)0x6688 >> 0x10);
    iVar10 = (int)*(uint32_t *)0x6688 + local_4 * 0x14;
    *(int *)(iVar10 + 8) = uVar7 + uVar5;
    *(int *)(iVar10 + 10) =
         (((iVar9 + param_5 + (uint16_t)((uVar6 + param_4) < uVar1)) - ((int)uVar1 >> 0xf)) -
         (uint16_t)(uVar6 + param_4 < uVar1)) + iVar12 + (uint16_t)((uVar7 + uVar5) < uVar5);
    uVar5 = FUN_24dd_4654(*(int *)((uint)bVar2 * 2 + 0xc7c) << 1);
    iVar10 = 0;
    uVar1 = *(uint16_t *)((uint)bVar2 * 2 + 0xc7c);
    FUN_24dd_3d80();
    uVar6 = FUN_24dd_3dbd();
    uVar7 = (uVar6 + param_2) - uVar1;
    uVar11 = (uint16_t)((uint32_t)*(uint32_t *)0x6688 >> 0x10);
    iVar9 = (int)*(uint32_t *)0x6688