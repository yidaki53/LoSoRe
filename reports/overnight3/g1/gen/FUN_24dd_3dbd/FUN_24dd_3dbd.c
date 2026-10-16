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

int16_t FUN_24dd_3dbd(uint16_t in_EAX, uint16_t in_CX, uint16_t in_DX, int16_t in_BX) {
    uint16_t uVar1;
    uint16_t uVar2;
    int16_t iVar3;
    int16_t iVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    int16_t iVar7;
    uint16_t uVar8;
    uint16_t uVar9;
    int16_t iVar10;
    bool bVar11;
    bool bVar12;
    bool bVar13;

    if (1 < *(uint8_t *)0x6420) {
        if ((in_BX << 16 | in_CX) != 0) {
            return (int16_t)((uint32_t)(in_EAX | (uint32_t)in_DX << 16) / (uint32_t)(in_BX << 16 | in_CX));
        }
        iVar4 = FUN_24dd_010f();
        return iVar4;
    }
    bVar13 = (int16_t)in_DX < 0;
    if (bVar13) {
        iVar4 = (int16_t)in_EAX;
        in_EAX = (uint32_t)(uint16_t)-iVar4;
        in_DX = -(in_DX + (iVar4 != 0));
    }
    uVar9 = (uint16_t)bVar13;
    if (in_BX == 0) {
        if (in_CX == 0) goto LAB_24dd_3e36;
LAB_24dd_3e3e:
        iVar4 = (int16_t)(((uint32_t)in_DX % (uint32_t)in_CX << 16 | in_EAX & 0xffff) / (uint32_t)in_CX);
    } else {
        if ((int16_t)in_BX < 0) {
            uVar9 = uVar9 + 2;
            bVar11 = in_CX != 0;
            in_CX = -in_CX;
            in_BX = -(in_BX + bVar11);
            if (in_BX == 0) goto LAB_24dd_3e3e;
        }
        iVar7 = 0;
        iVar4 = 0;
        iVar10 = 0x10;
        do {
            bVar11 = iVar4 < 0;
            iVar3 = iVar4 * 2;
            uVar2 = in_DX << 1 | (uint16_t)((in_EAX & 0x8000) != 0);
            uVar6 = iVar7 << 1 | (uint16_t)((in_DX & 0x8000) != 0);
            in_DX = uVar2 - in_CX;
            uVar2 = (uint16_t)(uVar2 < in_CX);
            uVar1 = uVar6 - in_BX;
            iVar7 = uVar1 - uVar2;
            iVar4 = iVar3 + 1;
            if (uVar6 < in_BX || uVar1 < uVar2) {
                bVar12 = (in_DX < in_CX);
                in_DX = in_DX + in_CX;
                iVar7 = iVar7 + in_BX + (uint16_t)bVar12;
                iVar4 = iVar3;
            }
            iVar10 = iVar10 + -1;
            in_EAX = (in_EAX & 0xffff) << 1 | (uint32_t)bVar11;
        } while (iVar10 != 0);
    }
    uVar9 = uVar9 >> 1;
    if (bVar13) {
        uVar9 = uVar9 + 1;
    }
    if (uVar9 == 1) {
        iVar4 = -iVar4;
    }
    return iVar4;
}