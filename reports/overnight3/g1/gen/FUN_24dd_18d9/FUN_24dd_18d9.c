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

void FUN_24dd_0642(void);
uint16_t FUN_24dd_1190(void);

void FUN_24dd_18d9(int param_1, uint8_t param_2) {
    uint32_t *puVar16;
    uint8_t bVar2;
    int *piVar3;
    uint16_t *puVar4;
    uint32_t *puVar5;
    uint32_t uVar6;
    uint8_t bVar7;
    uint32_t in_CX;
    uint32_t uVar8;
    int iVar9;
    uint32_t uVar10;
    uint32_t uVar11;
    int iVar12;
    uint32_t in_BX;
    int iVar13;
    uint32_t uVar14;
    int iVar15;
    uint32_t *puVar17;
    uint32_t *puVar1;
    uint32_t uVar19;

    FUN_24dd_0642();
    puVar16 = (uint32_t *)((uint32_t)param_2 * 0xc + -0xc + param_1);
    while (true) {
        bVar2 = param_2 - 1;
        if (bVar2 == 0 || (char)param_2 < '\x01') break;
        puVar4 = (uint16_t *)*(int *)0xd8;
        *(uint8_t *)(puVar4 + 5) = *(uint8_t *)(puVar4 + 5) ^ *(uint8_t *)(puVar4 + 0xb);
        uVar19 = FUN_24dd_1190();
        *puVar4 = (int)uVar19;
        puVar4[1] = in_BX;
        puVar4[2] = in_CX;
        puVar4[3] = (int)((uint64_t)uVar19 >> 0x10);
        puVar17 = puVar16 + -6;
        puVar5 = (uint32_t *)*(uint16_t *)0xd8;
        in_BX = *puVar17;
        in_CX = puVar16[-5];
        uVar8 = puVar16[-4];
        uVar11 = puVar16[-3];
        bVar7 = (uint8_t)puVar16[-1];
        puVar16 = puVar17;
        param_2 = bVar2;
        if (bVar7 == (uint8_t)puVar5[5]) {
            puVar1 = puVar5;
            uVar6 = *puVar1;
            *puVar1 = *puVar1 + in_BX;
            puVar1 = puVar5 + 1;
            uVar14 = *puVar1;
            uVar10 = *puVar1;
            *puVar1 = uVar10 + in_CX + (uint32_t)((uVar6 + in_BX) > 0xffffffff);
            puVar1 = puVar5 + 2;
            uVar10 = (uint32_t)(((uVar14 + in_CX) > 0xffffffff) || ((uVar10 + in_CX) > 0xffffffff));
            uVar14 = *puVar1;
            uVar6 = *puVar1;
            *puVar1 = uVar6 + uVar8 + uVar10;
            puVar5[3] = puVar5[3] + uVar11 + (uint32_t)(((uVar14 + uVar8) > 0xffffffff) || ((uVar6 + uVar8) > 0xffffffff));
        } else {
            int bVar18 = in_BX < *puVar5;
            in_BX = in_BX - *puVar5;
            uVar6 = (uint32_t)bVar18;
            bVar18 = in_CX < puVar5[1];
            uVar14 = in_CX - puVar5[1];
            in_CX = uVar14 - uVar6;
            uVar6 = (uint32_t)(bVar18 || uVar14 < uVar6);
            uVar14 = uVar8 - puVar5[2];
            uVar10 = uVar14 - uVar6;
            uVar8 = (uint32_t)(uVar8 < puVar5[2]