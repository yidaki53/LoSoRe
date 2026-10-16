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
#include <stdbool.h>

void __stdcall16far FUN_24cb_00a7(uint8_t *param_1, uint8_t *param_2) {
    uint8_t local_22[32];
    uint8_t *pbVar7 = param_1;
    uint8_t *pbVar8 = local_22;
    uint8_t bVar4 = *param_1;
    int iVar5;
    int iVar6;
    bool bVar9;

    if (0x1f < bVar4) {
        bVar4 = 0x1f;
    }
    iVar5 = (int)bVar4;
    iVar6 = iVar5 + 1;
    for (; iVar5 != 0; iVar5--) {
        pbVar7++;
        bVar4 = *pbVar7;
        if ((0x60 < bVar4) && (bVar4 < 0x7b)) {
            bVar4 -= 0x20;
        }
        *pbVar8++ = bVar4;
    }
    *pbVar8 = 0x3d;
    uint16_t uVar1 = *(uint16_t *)0x2c;
    pbVar8 = (uint8_t *)0x0;
    while (bVar9 = *pbVar8 == 0, !bVar9) {
        pbVar7 = local_22;
        iVar5 = iVar6;
        do {
            if (iVar5 == 0) break;
            iVar5--;
            bVar9 = *pbVar8 == *pbVar7;
            pbVar7++;
            pbVar8++;
        } while (bVar9);
        if (bVar9) break;
        pbVar8--;
        while (*pbVar8 != 0) {
            pbVar8++;
        }
    }
    iVar5 = 0x100;
    pbVar7 = pbVar8;
    while (iVar5 != 0 && *pbVar2 != 0) {
        iVar5--;
        pbVar7++;
    }
    *param_2 = ~(uint8_t)iVar5;
    for (iVar5 = ((uint8_t)(iVar5 >> 8) << 8) | ~(uint8_t)iVar5; pbVar7 = pbVar7 + 1, iVar5 != 0; iVar5--) {
        *pbVar7 = *pbVar8++;
    }
}