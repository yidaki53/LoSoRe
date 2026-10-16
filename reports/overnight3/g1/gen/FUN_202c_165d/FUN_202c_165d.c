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

extern uint16_t FUN_24dd_4654(uint16_t);
extern void FUN_24dd_3d80(void);
extern uint16_t FUN_24dd_3dbd(void);

void __stdcall16far FUN_202c_165d(uint16_t param_1, uint32_t param_2, int32_t param_3, uint32_t param_4, int32_t param_5,
                                  uint16_t param_6, uint16_t param_7, int32_t param_8, uint8_t param_9) {
    uint32_t *puVar1;
    int32_t *piVar2;
    uint32_t uVar3;
    uint8_t bVar4;
    uint16_t uVar5;
    int32_t iVar6;
    uint32_t uVar7;
    uint32_t uVar8;
    uint32_t uVar9;
    int32_t iVar10;
    int32_t iVar11;
    uint32_t *puVar12;
    uint16_t uVar13;
    int32_t local_4;

    for (local_4 = 0; (*(char *)((int)*(uint32_t *)0x6694 + local_4 * 0x14 + 0x12) != '\0' && (local_4 < 600)); local_4++) {
    }
    bVar4 = param_9 & 0x7f;
    *(uint8_t *)((int)*(uint32_t *)0x6694 + local_4 * 0x14 + 0x12) = param_9;
    *(uint16_t *)((int)*(uint32_t *)0x6694 + local_4 * 0x14 + 2) = param_7;
    *(uint16_t *)((int)*(uint32_t *)0x6694 + local_4 * 0x14 + 6) = param_6;
    iVar6 = FUN_24dd_4654(*(uint16_t *)((uint32_t)bVar4 * 2 + 0x53c));
    iVar11 = *(int32_t *)((uint32_t)bVar4 * 2 + 0x50c);
    uVar7 = FUN_24dd_4654(*(int32_t *)((uint32_t)bVar4 * 2 + 0x56c) << 1);
    iVar14 = 0;
    uVar3 = *(uint32_t *)((uint32_t)bVar4 * 2 + 0x56c);
    iVar6 = (iVar11 - iVar6) >> 0xf;
    iVar11 = iVar6;
    FUN_24dd_3d80();
    uVar8 = FUN_24dd_3dbd();
    uVar9 = (uVar8 + param_4) - uVar3;
    uVar13 = (uint16_t)((*(uint32_t *)0x6694 >> 0x10) & 0xFFFF);
    int32_t iVar10 = (int)*(uint32_t *)0x6694 + local_4 * 0x14;
    *(int32_t *)(iVar10 + 8) = uVar9 + uVar7;
    *(int32_t *)(iVar10 + 10) =
        (((iVar11 + param_5 + (uint32_t)((uVar8 + param_4) < uVar3)) - ((int32_t)uVar3 >> 0xf)) -
         (uint32_t)(uVar8 + param_4 < uVar3)) + iVar14 + (uint32_t)((uVar9 + uVar7) < uVar9);
    uVar7 = FUN_24dd_4654(*(int32_t *)((uint32_t)bVar4 * 2 + 0x56c) << 1);
    iVar10 = 0;
    uVar3 = *(uint32_t *)((uint32_t)bVar4 * 2 + 0x56c);
    FUN_24dd_3d80();
    uVar8 = FUN_24dd_3dbd();
    uVar9 = (uVar8 + param_2) - uVar3;
    uVar13 = (