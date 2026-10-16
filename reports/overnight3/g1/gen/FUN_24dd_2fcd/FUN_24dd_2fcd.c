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

#include <stdbool.h>
#include <math.h>

void FUN_24dd_2fcd(void) {
    int *piVar1;
    bool bVar6;
    long double lVar7;
    long double lVar8;
    int iVar3 = 0x7fff;
    int *piVar5 = (int *)0x0;
    uint16_t uVar4 = *(uint16_t *)0x2c;

    do {
        if ((char)*piVar5 == '\0') break;
        if ((*piVar5 == 0x3738) && ((char)piVar5[1] == '=')) {
            bVar6 = ((uint8_t)((uint)piVar5[1] >> 8) & 0xdf) == 0x59;
            goto LAB_24dd_3018;
        }
        bVar6 = true;
        do {
            if (iVar3 == 0) break;
            iVar3--;
            piVar1 = piVar5;
            piVar5 = (int *)((int)piVar5 + 1);
            bVar6 = (char)*piVar1 == '\0';
        } while (!bVar6);
    } while (bVar6);

    out(0xf0, 0);
    *(uint16_t *)0x7b40 = 0;
    *(uint16_t *)0x7b40 = 0x37f;
    iVar3 = 0x14;
    do {
        iVar3--;
    } while (iVar3 != 0);

    bVar6 = (*(uint *)0x7b40 & 0xf3f) == 0x33f;
LAB_24dd_3018:
    uVar4 = 0x1330;
    uint8_t uVar2 = 0;
    if (bVar6) {
        lVar8 = 1.0L / 0.0L;
        lVar7 = -lVar8;
        *(uint *)0x7b40 =
            (uint)(lVar7 < lVar8) << 8 | (uint)(isnan(lVar7) || isnan(lVar8)) << 10 |
            (uint)(lVar7 == lVar8) << 0xe;
        uVar2 = 2;
        if ((*(uint *)0x7b40 & 0x4000) == 0) {
            uVar4 = 0x1332;
            uVar2 = 3;
        }
    }
    *(uint8_t *)0x6421 = uVar2;
    *(uint16_t *)0x7b3e = uVar4;
    return;
}