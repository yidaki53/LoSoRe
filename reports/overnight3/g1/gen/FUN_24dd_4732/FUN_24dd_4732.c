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

uint16_t FUN_24dd_4732(uint16_t in_CX, uint8_t *unaff_DI) {
    uint32_t uVar1;
    int32_t iVar2;
    uint32_t uVar3;
    int32_t iVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    uint32_t uVar7;
    uint8_t bVar8;
    uint8_t bVar9;
    uint32_t uVar10;
    char cVar11;
    uint32_t uVar12;
    bool bVar13;

    iVar2 = 0;
    uVar6 = 0;
    uVar12 = 0;

    if (in_CX == 0) goto LAB_24dd_4797;

    if (*unaff_DI == 0x2b) {
LAB_24dd_4747:
        unaff_DI++;
        in_CX--;
        if (in_CX == 0) goto LAB_24dd_4797;
    } else if (*unaff_DI == 0x2d) {
        uVar12 = 0xffff;
        goto LAB_24dd_4747;
    }

    if (*unaff_DI != 0x24) {
        do {
            uVar10 = (uint32_t)(*unaff_DI - 0x30);
            if ((*unaff_DI - 0x3a) < 0xf6) break;
            if ((uVar6 & 0xf000) != 0) goto LAB_24dd_4797;
            uVar3 = iVar2 * 2;
            uVar7 = (uVar6 << 1) | (uint32_t)(iVar2 < 0);
            iVar4 = iVar2 << 2;
            uVar5 = iVar2 * 8;
            uVar6 = iVar2 * 10;
            iVar2 = uVar6 + uVar10;
            uVar6 = (((uVar7 << 1) | (uint32_t)(uVar3 < 0)) << 1) | (uint32_t)(iVar4 < 0)) + uVar7 +
                    (uint32_t)((uVar5 & 0x80000000) != 0) + (uint32_t)((uVar6 & 0x80000000) != 0);
            unaff_DI++;
            in_CX--;
        } while (in_CX != 0);
LAB_24dd_4781:
        if (iVar2 != 0 || uVar6 != 0) {
            if ((int32_t)uVar12 < 0) {
                bVar13 = iVar2 != 0;
                iVar2 = -iVar2;
                uVar6 = -(uint32_t)bVar13 - uVar6;
            }
            if ((int32_t)(uVar12 ^ uVar6) < 0) goto LAB_24dd_4797;
        }
        return (uint16_t)((uVar6 << 8) | (uint8_t)iVar2);
    }

    iVar4 = in_CX - 1;
    if (iVar4 != 0) {
        do {
            unaff_DI++;
            bVar8 = *unaff_DI;
            if (0x60 < bVar8) {
                bVar8 = bVar8 - 0x20;
            }
            bVar9 = bVar8 - 0x30;
            if ((bVar8 - 0x3a) < 0xf6) {
                if ((bVar8 + 0xb9) < 0xfa) goto LAB_24dd_4781;
                bVar9 = bVar8 - 0x37;
            }
            cVar11 = '\x04';
            do {
                bVar13 = iVar2 < 0;
                iVar2 = iVar2 << 1;
                uVar1 = ((uint64_t)bVar13 << 32) | (uint64_t)uVar6 << 1;
                uVar6 = (uint32_t)uVar1 | (uint32_t)bVar13;
                if ((uVar1 & 0x100000000) != 0) goto LAB_24dd_4797;
                cVar11 =