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

void FUN_24dd_2361();
void FUN_24dd_0628();
void FUN_24dd_0e57();
void FUN_24dd_060f();
void FUN_24dd_05fd();
long FUN_24dd_1190();

void FUN_24dd_10a7(int *param_1, int param_2, int param_3) {
    uint16_t uVar1;
    uint16_t uVar2;
    uint32_t uVar3;
    uint32_t uVar4;
    uint16_t uVar5;
    int iVar6;
    uint8_t bVar7;
    uint16_t in_CX;
    uint16_t uVar8;
    uint16_t uVar9;
    int iVar10;
    uint16_t uVar11;
    bool bVar12;
    bool bVar13;
    long lVar14;

    bVar7 = *(uint8_t *)(param_3 + 10) ^ *(uint8_t *)(param_2 + 10);
    uVar8 = ((uint16_t)in_CX >> 8) | bVar7;
    uVar11 = *(uint16_t *)(param_2 + 8);
    uVar1 = *(uint16_t *)(param_3 + 8);
    bVar12 = uVar1 < 0x4001;
    if ((int)uVar1 < 0x4001) {
        bVar12 = uVar11 < 0x4001;
        if ((int)uVar11 < 0x4001) {
            uVar5 = uVar1;
            if ((int)uVar11 <= (int)uVar1) {
                uVar5 = uVar11;
                uVar11 = uVar1;
            }
            if (-0x3fff < (int)uVar5) {
                iVar6 = uVar5 + uVar11;
                if (iVar6 + -1 < 0x4001) {
                    if (iVar6 < -0x3ffe) {
                        FUN_24dd_2361();
                        goto LAB_24dd_112d;
                    }
                    FUN_24dd_0628();
                    FUN_24dd_0628();
                    lVar14 = FUN_24dd_1190();
                    *(int *)0xd8 = *(int *)0xd8 + 0x18;
                    if (-1 < lVar14) {
                        iVar6 = iVar6 + -1;
                        bVar13 = param_2 < 0;
                        param_2 = param_2 << 1;
                        uVar3 = ((uint32_t)bVar13 << 16) | (uint32_t)lVar14;
                        bVar12 = (uVar3 & 0x10000) != 0;
                        uVar4 = ((uint32_t)bVar12 << 16) | (uint32_t)uVar11;
                        uVar11 = (uint16_t)uVar4 | (uint16_t)bVar12;
                        bVar12 = (uVar4 & 0x10000) != 0;
                        uVar4 = ((uint32_t)bVar12 << 16) | (uint32_t)uVar8;
                        uVar8 = (uint16_t)uVar4 | (uint16_t)bVar12;
                        lVar14 = ((uint32_t)((uint16_t)(lVar14 >> 16) << 1) | (uint32_t)bVar12) << 16 |
                                  ((uint32_t)uVar3 | (uint32_t)bVar13);
                    }
                    uVar9 = (uint16_t)(lVar14 >> 16);
                    uVar1 = (uint16_t)CARRY2((uint16_t)lVar14, (uint16_t)(param_2 < 0));
                    uVar5 = (uint16_t)CARRY2(uVar11, uVar1);
                    uVar2 = (uint16_t)CARRY2(uVar8, uVar5);
                    iVar10 = uVar9 + uVar2;
                    if (CARRY2(uVar9