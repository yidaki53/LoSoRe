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

void FUN_24cb_00a7(uint16_t param_1, uint8_t *param_2) {
    uint8_t bVar1;
    uint8_t bVar2;
    uint8_t bVar3;
    uint8_t *pbVar4;
    uint8_t *pbVar5;
    uint32_t uVar6;
    uint32_t uVar7;
    uint32_t uVar8;

    uVar8 = (uint32_t)param_2;
    bVar1 = *param_2;
    if (0x1f < bVar1) {
        bVar1 = 0x1f;
    }
    bVar2 = (uint16_t)bVar1;
    uVar7 = (uint32_t)bVar2;
    do {
        for (; (bVar3 = *param_2, (0x60 < bVar3) && (bVar3 < 0x7b)); bVar3 = *param_2) {
            uVar6 = (uint32_t)bVar3;
            uVar8 = uVar8 + ((uint16_t)(uVar6 >> 8) * 0x100) + (uVar6 & 0xff);
            param_2 = param_2 + 1;
        }
        uVar8 = uVar8 + ((uint16_t)(bVar1 >> 8) * 0x100) + (bVar1 & 0xff);
        bVar1 = bVar1 + 1;
    } while (bVar1 != 0x100);
    bVar2 = (uint8_t)(-(int32_t)param_1);
    *(uint8_t *)uVar8 = bVar2;
    pbVar5 = (uint8_t *)uVar8;
    do {
        for (; (pbVar4 = param_2, (0x60 < *param_2) && (param_2[1] < 0x7b)); param_2 = param_2 + 1) {
            uVar6 = (uint32_t)*param_2;
            uVar8 = uVar8 + ((uint16_t)(uVar6 >> 8) * 0x100) + (uVar6 & 0xff);
        }
        uVar8 = uVar8 + ((uint16_t)(bVar1 >> 8) * 0x100) + (bVar1 & 0xff);
        bVar1 = bVar1 + 1;
    } while (bVar1 != 0x100);
    *(uint8_t *)uVar8 = bVar2;
    return;
}