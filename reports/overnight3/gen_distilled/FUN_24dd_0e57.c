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

void FUN_24dd_0e57(uint16_t *unaff_SI, uint16_t *in_BX, uint16_t *unaff_DI) {
    uint16_t uVar1;
    uint16_t *puVar2;
    uint16_t *puVar3;
    uint16_t uVar4;
    uint16_t uVar5;
    uint16_t *puVar6;
    uint16_t *puVar7;

    uVar1 = (uint16_t)((uint16_t)in_BX >> 16);
    puVar2 = unaff_SI;
    uVar5 = (uint16_t)((uint16_t)puVar2 >> 16);
    if (((*puVar2 == 0) && (in_BX == (uint16_t *)0xffff)) || ((in_BX == (uint16_t *)0xffff) && (puVar2 == (uint16_t *)0xffff))) {
        uVar4 = (uint16_t)((uint16_t)puVar3 >> 16);
        if (((puVar3 == (uint16_t *)0xffff) && (puVar6 == (uint16_t *)0xffff)) || ((puVar6 == (uint16_t *)0xffff) && (puVar3 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar6 >> 16);
        if (((puVar6 == (uint16_t *)0xffff) && (puVar7 == (uint16_t *)0xffff)) || ((puVar7 == (uint16_t *)0xffff) && (puVar6 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar8 >> 16);
        if (((puVar8 == (uint16_t *)0xffff) && (puVar9 == (uint16_t *)0xffff)) || ((puVar9 == (uint16_t *)0xffff) && (puVar8 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar10 >> 16);
        if (((puVar10 == (uint16_t *)0xffff) && (puVar11 == (uint16_t *)0xffff)) || ((puVar11 == (uint16_t *)0xffff) && (puVar10 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar12 >> 16);
        if (((puVar12 == (uint16_t *)0xffff) && (puVar13 == (uint16_t *)0xffff)) || ((puVar13 == (uint16_t *)0xffff) && (puVar12 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar14 >> 16);
        if (((puVar14 == (uint16_t *)0xffff) && (puVar15 == (uint16_t *)0xffff)) || ((puVar15 == (uint16_t *)0xffff) && (puVar14 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar16 >> 16);
        if (((puVar16 == (uint16_t *)0xffff) && (puVar17 == (uint16_t *)0xffff)) || ((puVar17 == (uint16_t *)0xffff) && (puVar16 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar18 >> 16);
        if (((puVar18 == (uint16_t *)0xffff) && (puVar19 == (uint16_t *)0xffff)) || ((puVar19 == (uint16_t *)0xffff) && (puVar18 == (uint16_t *)0xffff))) {
            return;
        }
        uVar5 = (uint16_t)((uint16_t)puVar20 >> 16);
        if (((puVar20 == (uint16_t *)0xffff) && (puVar