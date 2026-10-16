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

void FUN_235c_0711(uint16_t ds, uint16_t ss, uint16_t es, uint16_t fs, uint16_t gs, uint16_t sp, uint16_t bp, uint16_t si, uint16_t di, uint16_t ip, uint16_t cs, uint16_t ax, uint16_t bx, uint16_t cx, uint16_t dx, uint16_t *param_1, uint32_t *param_2) {
    uint32_t local_90a;
    int local_908;
    uint8_t local_906[2052];
    uint8_t local_102;
    uint8_t abStack_101[255];
    uint8_t *pbVar7;
    uint8_t *pbVar4;
    uint8_t *pbVar3;
    uint32_t uVar6;
    uint32_t uVar2;
    int iVar5;
    int iVar8;
    uint16_t uVar9;
    uint16_t uVar10;
    uint16_t uVar11;
    uint32_t uVar13;
    bool bVar12;

    pbVar7 = (uint8_t *)param_1;
    local_102 = *param_1;
    pbVar4 = abStack_101;
    for (uVar6 = (uint32_t)local_102; pbVar7 = pbVar7 + 1, uVar6 != 0; uVar6 = uVar6 - 1) {
        pbVar3 = pbVar4;
        pbVar4 = pbVar4 + 1;
        *pbVar3 = *pbVar7;
    }
    FUN_235c_056f(&local_102, ss);
    uVar13 = FUN_24dd_028a(10);
    *param_2 = (uint32_t)uVar13;
    *(uint16_t *)((uint32_t)param_2 + 2) = (uint16_t)((uint64_t)uVar13 >> 16);
    uVar10 = *(uint16_t *)(ds * 16 + 0x7814);
    uVar9 = (uint16_t)((uint64_t)*param_2 >> 16);
    iVar8 = (int)*param_2;
    *(uint16_t *)(iVar8 + 6) = *(uint16_t *)(ds * 16 + 0x7812);
    *(uint16_t *)(iVar8 + 8) = uVar10;
    if (*(char *)(ds * 16 + 0x7688) == '\0') {
        uVar10 = (uint16_t)((uint64_t)*param_2 >> 16);
        iVar8 = (int)*param_2;
        *(uint16_t *)(iVar8 + 2) = 0;
        *(uint16_t *)(iVar8 + 4) = 0;
        uVar11 = (uint16_t)((uint64_t)*param_2 >> 16);
        uVar9 = (uint16_t)*param_2;
        uVar10 = FUN_24dd_3dbd(uVar9, uVar11);
        FUN_2494_0027(uVar10, uVar9, uVar11);
    } else {
        uVar10 = *(uint16_t *)(ds * 16 + 0x768e);
        uVar9 = (uint16_t)((uint64_t)*param_2 >> 16);
        iVar8 = (int)*param_2;
        *(uint16_t *)(iVar8 + 2) = *(uint16_t *)(ds * 16 + 0x768c);
        *(uint16_t *)(iVar8 + 4) = uVar10;
        *(uint16_t *)*param_2 = *(uint16_t *)(ds * 16 + 0x768a);
        uVar6 = *(uint32_t *)(ds * 16 + 0x768c);
        iVar8 = *(int *)(ds * 16 + 0x768e);
        uVar2 = *(uint32_t *)(ds * 16 + 0x78