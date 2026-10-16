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

void __stdcall16far FUN_1ea2_01a8(uint16_t *param_1, int param_2, uint32_t param_3, int param_4, uint16_t *param_5) {
    uint16_t *puVar1;
    uint16_t *puVar2;
    uint16_t *puVar3;
    uint16_t *puVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    uint16_t *puVar7;
    uint16_t *puVar8;
    uint16_t uVar9;
    uint16_t uVar10;

    uVar10 = (uint16_t)((uint32_t)param_5 >> 16);
    puVar7 = (uint16_t *)param_5;
    uVar9 = (uint16_t)((uint32_t)param_1 >> 16);
    puVar8 = (uint16_t *)param_1;
    uVar5 = param_3 >> 1;
    uVar6 = uVar5;
    if ((param_3 & 1) == 0) {
        do {
            for (; uVar6 != 0; uVar6--) {
                puVar4 = puVar8;
                puVar8 = puVar8 + 1;
                puVar2 = puVar7;
                puVar7 = puVar7 + 1;
                *puVar4 = *puVar2;
            }
            puVar8 = (uint16_t *)((int)puVar8 + (0x140 - param_3));
            puVar7 = (uint16_t *)((int)puVar7 + (param_4 - param_3));
            param_2--;
            uVar6 = uVar5;
        } while (param_2 != 0);
    } else {
        do {
            puVar3 = (uint16_t *)((int)puVar8 + 1);
            puVar1 = (uint16_t *)((int)puVar7 + 1);
            *(uint8_t *)puVar8 = *(uint8_t *)puVar7;
            for (uVar6 = uVar5; uVar6 != 0; uVar6--) {
                puVar4 = puVar3;
                puVar3 = puVar3 + 1;
                puVar2 = puVar1;
                puVar1 = puVar1 + 1;
                *puVar4 = *puVar2;
            }
            puVar8 = (uint16_t *)((int)puVar3 + (0x140 - param_3));
            puVar7 = (uint16_t *)((int)puVar1 + (param_4 - param_3));
            param_2--;
        } while (param_2 != 0);
    }
    return;
}