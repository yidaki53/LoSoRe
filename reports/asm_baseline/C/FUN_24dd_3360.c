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

void FUN_24dd_3360(uint16_t *param_1) {
    uint16_t *puVar1;
    void (*pcVar2)();
    uint8_t uVar3;
    uint8_t bVar4;
    uint32_t uVar5;
    uint8_t extraout_AH;
    uint32_t uVar6;
    uint32_t in_CX;
    int iVar7;
    uint16_t extraout_DX;
    uint32_t extraout_DX_00;
    uint32_t extraout_DX_01;
    int extraout_DX_02;
    int extraout_DX_03;
    uint32_t *puVar8;
    uint8_t *unaff_BP;
    uint8_t *puVar9;
    uint8_t *puVar10;
    uint16_t *unaff_DI;
    uint16_t *puVar11;
    uint16_t unaff_ES;
    uint16_t unaff_SS;
    uint16_t unaff_DS;
    int bVar12;
    int bVar13;
    char cVar14;
    char cVar15;
    uint8_t bStack_2b;
    uint32_t local_2a[9];
    uint8_t abStack_17[7];
    int local_10;
    uint32_t local_e;
    uint32_t local_c;
    uint32_t local_a;
    uint32_t local_8;
    uint32_t local_6;

    do {
        puVar9 = unaff_BP;
        cVar15 = SBORROW2((int)&stack0xfffe, 0x28);
        cVar14 = (int)local_2a < 0;
        bVar13 = &stack0x0000 == (uint8_t *)0x2a;
        pcVar2 = (void (*)())swi(0x35);
        (*pcVar2)();
        do {
        } while (bVar13 || cVar15 != cVar14);
        pcVar2 = (void (*)())swi(0x3c);
        (*pcVar2)();
        in_CX = in_CX ^ (uint32_t)&stack0xfffe;
        unaff_BP = &stack0xfffe;
    } while ((int)in_CX < 1);
    if (0x12 < (int)in_CX) {
        in_CX = 0x12;
    }
    if ((int)in_CX < -0x12) {
        in_CX = 0xffee;
    }
    pcVar2 = (void (*)())swi(0x3d);
    local_8 = in_CX;
    (*pcVar2)();
    local_c = local_e;
    uVar5 = local_e & 0x7fff;
    if (uVar5 == 0) {
        local_2a[0] = local_2a[0] & 0xff00;
        local_a = 0;
    } else {
        if (uVar5 == 0x7fff) {
            if (local_10 == -0x8000) {
                if ((int)local_e < 0) {
                    puVar1 = unaff_DI;
                    unaff_DI = (uint16_t *)((int)unaff_DI + 1);
                    *(uint8_t *)puVar1 = 0x2d;
                }
                puVar11 = unaff_DI + 1;
                *unaff_DI = 0x4e49;
                unaff_DI = (uint16_t *)((int)unaff_DI + 3);
                *(uint8_t *)puVar11 = 0x46;
            } else {
                puVar11 = unaff_DI + 1;
                *unaff_DI = 0x414e;
                unaff_DI = (uint16_t *)((int)unaff_DI + 3);
                *(uint8_t *)puVar11 = 0x4e;
            }
            goto LAB_24dd_34fc;
        }
        pcVar2 = (void (*)())swi(0x37);
        local_e = uVar5;
        (*pcVar2)();
        puVar10 = puVar9 + 1;
        out(*puVar9, extraout_DX);
        uVar3 = in(extraout_DX);
        local_a = (uint32_t)((ulong)((long)(CONCAT11(extraout_AH, uVar