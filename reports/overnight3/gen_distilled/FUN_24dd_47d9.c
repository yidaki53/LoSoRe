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

void FUN_24dd_47d9(uint16_t param_1, uint16_t param_2, int param_3, uint16_t param_4, uint8_t *param_5) {
    uint8_t *puVar1;
    uint8_t *puVar2;
    uint8_t *puVar3;
    uint8_t *puVar4;
    uint32_t uVar5;
    uint32_t uVar6;
    uint32_t uVar7;
    uint32_t uVar8;

    uVar8 = (uint32_t)param_5;
    puVar3 = (uint8_t *)param_4;
    uVar7 = (uint32_t)param_3;
    uVar6 = (uint32_t)param_2;
    if ((param_3 < param_4) || ((param_3 < param_4) && (param_3 < param_5))) {
        puVar2 = (uint8_t *)0x20;
        uVar5 = (uint32_t)param_2;
        while (uVar5 != 0) {
            puVar1 = puVar2;
            puVar2 = puVar2 + 1;
            uVar8 = uVar8 + 1;
        }
        return;
    }
    if ((param_3 < param_4) && (param_3 < param_5)) {
        uVar5 = (uint32_t)param_3;
        while (uVar5 != 0) {
            puVar1 = puVar2;
            puVar2 = puVar2 + 1;
            uVar8 = uVar8 + 1;
        }
        return;
    }
    uVar5 = (uint32_t)param_3;
    uVar6 = (uint32_t)param_4;
    if (uVar5 < uVar6) {
        while (uVar5 != 0) {
            puVar1 = puVar2;
            puVar2 = puVar2 + 1;
            uVar8 = uVar8 + 1;
            uVar5 = uVar5 - 1;
        }
        return;
    }
    uVar5 = (uint32_t)param_4;
    uVar6 = (uint32_t)param_3;
    if (uVar6 < uVar5) {
        return;
    }
    uVar5 = (uint32_t)param_3;
    uVar6 = (uint32_t)param_4;
    if (uVar5 < uVar6) {
        while (uVar5 != 0) {
            puVar1 = puVar2;
            puVar2 = puVar2 + 1;
            uVar8 = uVar8 + 1;
            uVar5 = uVar5 - 1;
        }
        return;
    }
    uVar5 = (uint32_t)param_4;
    uVar6 = (uint32_t)param_3;
    if (uVar6 < uVar5) {
        return;
    }
    uVar5 = (uint32_t)param_3;
    uVar6 = (uint32_t)param_4;
    if (uVar5 < uVar6) {
        while (uVar5 != 0) {
            puVar1 = puVar2;
            puVar2 = puVar2 + 1;
            uVar8 = uVar8 + 1;
            uVar5 = uVar5 - 1;
        }
        return;
    }
    uVar5 = (uint32_t)param_4;
    uVar6 = (uint32_t)param_3;
    if (uVar6 < uVar5) {
        return;
    }
    uVar5 = (uint32_t)param_3;
    uVar6 = (uint32_t)param_4;
    if (uVar5 < uVar6) {
        while (uVar5 != 0) {
            puVar1 = puVar2;
            puVar2 = puVar2 + 1;
            uVar8 = uVar8 + 1;
            uVar5 = uVar5 - 1;
        }
        return;
    }
    uVar5 = (uint32_t)param_4;
    uVar6 = (uint32_t)param_3;
    if (uVar6 < uVar5) {
        return;
    }
    uVar5 = (uint32_t)param_3;
    uVar6 = (uint32_t)param_4;